from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from apps.locations.models import City, Country
from apps.locations.serializers import CitySerializer, CountrySerializer


class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer
