from django.db.models import OuterRef, Exists
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from apps.locations.models import City
from apps.locations.models import Country
from apps.locations.serializers import CitySerializer, CountrySerializer
from apps.sites.models import Site
from apps.sites.serializers import SiteSerializer
from apps.tours.models import Tour, UserTour
from apps.tours.serializers import TourWithoutSitesSerializer
from apps.utils.pagination import CustomPagination


class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=True, methods=["get"], serializer_class=TourWithoutSitesSerializer)
    def tours(self, request, pk):
        city = get_object_or_404(City, id=pk)
        tag_list = self.request.query_params.getlist("tag_id", [])
        current_user = self.request.user
        queryset = (
            Tour.objects.prefetch_related("sites")
            .annotate(is_owned=Exists(UserTour.objects.filter(user_id=current_user.id, tour=OuterRef("pk"))))
            .filter(is_enabled=True, is_approved=True)
        )

        if tag_list:
            queryset = queryset.filter(
                toursite__site__base_site__city=city, toursite__site__tags__id__in=tag_list
            ).distinct()
        else:
            queryset = queryset.filter(toursite__site__base_site__city=city).distinct()

        pagination = CustomPagination()
        paginated_queryset = pagination.paginate_queryset(queryset=queryset, request=request)
        serialized_data = self.get_serializer(paginated_queryset, many=True)
        return pagination.get_paginated_response(serialized_data.data)

    @action(detail=True, methods=["get"], serializer_class=SiteSerializer)
    def sites(self, request, pk):
        get_object_or_404(City, id=pk)

        queryset = Site.objects.filter(is_approved=True, base_site__city_id=pk)
        pagination = CustomPagination()
        paginated_queryset = pagination.paginate_queryset(queryset=queryset, request=request)
        serialized_data = self.get_serializer(paginated_queryset, many=True)
        return pagination.get_paginated_response(serialized_data.data)
