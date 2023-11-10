from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from apps.tours.models import Tour
from apps.tours.serializers import TourSerializer


class ToursViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (AllowAny,)
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
