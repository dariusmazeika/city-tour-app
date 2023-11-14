from rest_framework import serializers

from apps.locations.models import City, Country


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
        fields = fields = [
            "id",
            "name",
            "country",
            "image",
        ]
