from django.db.models import F, Avg, Count, Case, When
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.sites.models import Site
from apps.sites.serializers import SiteSerializer
from apps.tours.models import Tour, UserTour, TourSite


class TourImageSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, tour: Tour) -> str | None:
        request = self.context.get("request")
        if site := tour.sites.filter(toursite__order=0).select_related("base_site").first():
            base_site_image = site.base_site.siteimage_set.first()
            if base_site_image:
                return request.build_absolute_uri(base_site_image.image.url)

        return None


class TourSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)
    image = TourImageSerializer(source="*", read_only=True)

    class Meta:
        model = Tour
        fields = "__all__"


class TourWithoutSitesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    image = TourImageSerializer(source="*", read_only=True)

    class Meta:
        model = Tour
        exclude = ("sites",)

    def get_rating(self, obj):
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
            raise serializers.ValidationError("error_tour_status_does_not_exist.")

        current_status = self.instance.status if self.instance else None

        if current_status and attrs["status"].capitalize() not in status_transitions.get(current_status, []):
            raise serializers.ValidationError("error_status_transition_is_not_allowed.")

        return attrs


class BuyTourSerializer(serializers.Serializer):
    def validate(self, attrs):
        current_user = self.context["request"].user
        tour_to_buy = get_object_or_404(Tour, pk=self.context["tour_id"])

        if current_user.owned_tours.filter(id=tour_to_buy.id).exists():
            raise ValidationError("error_tour_already_owned")

        if current_user.balance < tour_to_buy.price:
            raise ValidationError("error_wallet_balance_less_than_tour_price")

        attrs["tour"] = tour_to_buy

        return attrs

    def create(self, validated_data):
        tour_to_buy = validated_data["tour"]
        current_user = self.context["request"].user
        current_user.balance = F("balance") - tour_to_buy.price
        current_user.save(update_fields=["balance"])
        created_user_tour = UserTour.objects.create(tour=tour_to_buy, user=current_user, price=tour_to_buy.price)

        return created_user_tour


class CreateTourSerializer(serializers.ModelSerializer):
    sites_ids_ordered = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Tour
        fields = (
            "id",
            "sites_ids_ordered",
            "language",
            "overview",
            "title",
            "price",
            "source",
            "is_audio",
            "sites",
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
