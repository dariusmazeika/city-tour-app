from rest_framework import serializers

from apps.sites.serializers import SiteSerializer
from apps.tours.models import Tour


class TourSerializer(serializers.ModelSerializer):
    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = "__all__"


class TourWithoutSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        exclude = ("sites",)
