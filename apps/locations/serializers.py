from rest_framework import serializers

from apps.locations.models import City, Country
from apps.tours.models import Tour


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "code",
        ]


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "country",
            "image",
        ]


class CityTourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        exclude = ("sites",)
