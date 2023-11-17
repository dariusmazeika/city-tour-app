from django.db.models import Exists, OuterRef
from rest_framework import serializers

from apps.reviews.models import Review
from apps.tours.models import UserTour


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "text", "rating", "reviewer", "tour"]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = self.context["request"].user
        tour = attrs["tour"]

        user_tour = (
            UserTour.objects.annotate(review_exists=Exists(Review.objects.filter(reviewer=user, tour=OuterRef("tour"))))
            .filter(user=user, tour=tour)
            .values("status", "review_exists")
            .first()
        )

        if not user_tour:
            raise serializers.ValidationError("error_tour_not_purchased")
        elif user_tour["review_exists"]:
            raise serializers.ValidationError("error_tour_already_reviewed")
        elif user_tour["status"] != UserTour.FINISHED:
            raise serializers.ValidationError("error_tour_not_finished")

        return validated_data
