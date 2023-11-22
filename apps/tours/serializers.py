from django.db.models import Avg, Count, Case, When
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.sites.models import Site
from apps.sites.serializers import SiteSerializer
from apps.tours.models import Tour, UserTour, TourSite, SharedPrivateTour
from apps.users.models import User


class TourImageSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self, tour: Tour) -> str | None:
        request = self.context.get("request")
        if site := tour.sites.filter(toursite__order=0).select_related("base_site").first():
            base_site_image = site.base_site.siteimage_set.first()
            if base_site_image:
                return request.build_absolute_uri(base_site_image.image.url)

        return None


class TourSerializer(serializers.ModelSerializer, TourImageSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)
    is_owned = serializers.BooleanField(read_only=True)

    class Meta:
        model = Tour
        fields = (
            "id",
            "created_at",
            "updated_at",
            "author",
            "language",
            "overview",
            "title",
            "source",
            "is_audio",
            "is_enabled",
            "is_approved",
            "is_owned",
            "sites",
            "reviews",
            "image",
            "finished_count",
            "distance",
        )


class TourWithoutSitesSerializer(serializers.ModelSerializer, TourImageSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    is_owned = serializers.BooleanField(read_only=True)

    class Meta:
        model = Tour
        fields = (
            "id",
            "created_at",
            "updated_at",
            "author",
            "language",
            "overview",
            "title",
            "source",
            "is_audio",
            "is_enabled",
            "is_approved",
            "is_owned",
            "rating",
            "image",
            "finished_count",
            "distance",
        )

    def get_rating(self, obj: Tour) -> float | None:
        reviews = Review.objects.filter(tour=obj, is_approved=True)
        return reviews.aggregate(Avg("rating"))["rating__avg"]


class UserTourSerializer(serializers.ModelSerializer):
    tour = TourWithoutSitesSerializer(read_only=True)

    class Meta:
        model = UserTour
        exclude = ("updated_at", "user")


class UserTourUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTour
        fields = ["status"]

    def validate(self, attrs):
        status_transitions = {
            UserTour.NEW: [UserTour.STARTED],
            UserTour.STARTED: [UserTour.FINISHED],
            UserTour.FINISHED: [UserTour.STARTED],
        }
        if attrs["status"].capitalize() not in status_transitions:
            raise serializers.ValidationError("error_tour_status_does_not_exist")

        current_status = self.instance.status if self.instance else None

        if current_status and attrs["status"].capitalize() not in status_transitions.get(current_status, []):
            raise serializers.ValidationError("error_status_transition_is_not_allowed")

        return attrs


class BuyTourSerializer(serializers.Serializer):
    def validate(self, attrs):
        current_user = self.context["request"].user
        tour_to_buy = get_object_or_404(Tour, pk=self.context["tour_id"])

        if current_user.owned_tours.filter(id=tour_to_buy.id).exists():
            raise ValidationError("error_tour_already_owned")

        attrs["tour"] = tour_to_buy

        return attrs

    def create(self, validated_data):
        tour_to_buy = validated_data["tour"]
        current_user = self.context["request"].user
        created_user_tour = UserTour.objects.create(tour=tour_to_buy, user=current_user)

        return created_user_tour


class CreateTourSerializer(serializers.ModelSerializer):
    sites_ids_ordered = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    is_private = serializers.BooleanField(required=False)

    class Meta:
        model = Tour
        fields = (
            "id",
            "sites_ids_ordered",
            "language",
            "overview",
            "title",
            "source",
            "is_audio",
            "sites",
            "is_private",
        )
        read_only_fields = (
            "is_audio",
            "id",
            "sites",
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        sites_ids_ordered = validated_data["sites_ids_ordered"]

        # check site ids are unique
        if len(sites_ids_ordered) != len(set(sites_ids_ordered)):
            raise ValidationError("error_site_ids_non_unique")

        site_field_counts = (
            Site.objects.filter(id__in=sites_ids_ordered)
            .values("language", "base_site__city", "siteaudio")
            .aggregate(
                different_language_count=Count("language", distinct=True),
                different_city_count=Count("base_site__city", distinct=True),
                site_audio_count=Count("siteaudio"),
                all_existing_sites_count=Count("*"),
                approved_sites_count=Count(Case(When(is_approved=True, then=1))),
            )
        )

        # check all sites are approved
        if site_field_counts["approved_sites_count"] != site_field_counts["all_existing_sites_count"]:
            raise ValidationError("error_not_all_sites_are_approved")

        # check all sites exist
        if site_field_counts["all_existing_sites_count"] != len(sites_ids_ordered):
            raise NotFound("error_one_or_more_sites_do_not_exist")

        # check all sites have same language
        if site_field_counts["different_language_count"] != 1:
            raise ValidationError("error_sites_languages_not_same")

        # check all sites are in same city
        if site_field_counts["different_city_count"] != 1:
            raise ValidationError("error_all_sites_not_in_same_city")

        # if at least one site has audio, tour has audio
        if site_field_counts["site_audio_count"]:
            validated_data["is_audio"] = True

        return validated_data

    def create(self, validated_data):
        site_ids_ordered = validated_data.pop("sites_ids_ordered")
        validated_data["author"] = self.context["request"].user
        created_tour = super().create(validated_data)

        tour_sites_to_create = [
            TourSite(site_id=site_id, tour=created_tour, order=order) for order, site_id in enumerate(site_ids_ordered)
        ]

        TourSite.objects.bulk_create(tour_sites_to_create)

        return created_tour


class SharePrivateTourSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ("receiver_email",)

    def validate(self, attrs):
        super().validate(attrs)
        user_to_share_with_email = attrs["receiver_email"]
        user_to_share_with = get_object_or_404(User, email=user_to_share_with_email)
        attrs["user_to_share_with"] = user_to_share_with

        tour_to_share = get_object_or_404(Tour, pk=self.context["tour_id"])
        attrs["tour"] = tour_to_share

        if not tour_to_share.is_private:
            raise serializers.ValidationError("error_can_share_only_private_tour")

        current_user = self.context["request"].user
        if tour_to_share.author != current_user:
            raise serializers.ValidationError("error_current_user_does_not_own_this_tour")

        if user_to_share_with == current_user:
            raise serializers.ValidationError("error_can_not_share_a_tour_to_yourself")

        if UserTour.objects.filter(user=user_to_share_with, tour=tour_to_share).exists():
            raise serializers.ValidationError("error_tour_is_already_owned_by_user")

        return attrs

    def create(self, validated_data):
        current_user = self.context["request"].user
        tour = validated_data.pop("tour")
        user_to_share_with = validated_data.pop("user_to_share_with")

        user_tour = UserTour.objects.create(tour=tour, user=user_to_share_with, status=UserTour.NEW)
        SharedPrivateTour.objects.create(shared_by=current_user, user_tour=user_tour)

        return validated_data
