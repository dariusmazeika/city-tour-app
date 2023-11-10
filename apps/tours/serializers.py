from django.db.models import F
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from apps.sites.serializers import SiteSerializer
from apps.tours.models import Tour, UserTour


class TourSerializer(serializers.ModelSerializer):
    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = "__all__"


class TourWithoutSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        exclude = ("sites",)


class BuyTourSerializer(serializers.Serializer):
    def validate(self, attrs):
        current_user = self.context['request'].user
        tour_to_buy = Tour.objects.filter(id=self.context["pk"]).first()

        if not tour_to_buy:
            raise NotFound("Tour does not exist.")

        if current_user.owned_tours.filter(id=tour_to_buy.id).exists():
            raise ValidationError("Tour already owned.")

        if current_user.balance < tour_to_buy.price:
            raise ValidationError("Wallet balance is lower than tour price.")

        return attrs

    @staticmethod
    def create_user_tour(tour_to_buy, current_user):
        current_user.balance = F("balance") - tour_to_buy.price
        current_user.save(update_fields=["balance"])
        UserTour.objects.create(tour=tour_to_buy, user=current_user, price=tour_to_buy.price)
