from django import forms
from django.contrib.gis.geos import Point

from apps.sites.models import BaseSite


class LocationForm(forms.ModelForm):
    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=True,
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=True,
    )

    class Meta(object):
        model = BaseSite
        fields = [
            "title",
            "city",
            "location",
            "latitude",
            "longitude",
        ]
        widgets = {"point": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get("location", None)
        if isinstance(coordinates, Point):
            self.initial["longitude"], self.initial["latitude"] = coordinates.coords

    def clean(self):
        data = super().clean()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        location = data.get("location")
        if latitude and longitude and not location:
            data["location"] = Point(longitude, latitude)
        return data

    def save(self, commit=True):
        """On form save update location PointField value"""
        instance = super().save(commit=False)
        latitude = self.cleaned_data.get("latitude")
        longitude = self.cleaned_data.get("longitude")

        if latitude and longitude:
            instance.location = Point(longitude, latitude)

        if commit:
            instance.save()
        return instance
