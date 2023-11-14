from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from apps.locations.models import City, Country
from apps.locations.serializers import CitySerializer, CountrySerializer
from apps.locations.serializers import CityTourListSerializer
from apps.tours.models import Tour


class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityTourListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = CityTourListSerializer

    def get_queryset(self):
        city_id = self.kwargs.get("city_id")
        queryset = Tour.objects.filter(is_enabled=True, is_approved=True)
        city = get_object_or_404(City, id=city_id)
        return queryset.filter(toursite__site__base_site__city__id=city.id).distinct()
