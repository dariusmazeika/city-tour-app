from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from apps.locations.models import Country
from apps.locations.serializers import CountrySerializer


class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
