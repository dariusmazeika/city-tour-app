from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.sites.models import Site
from apps.tours.models import Tour, UserTour
from apps.tours.serializers import (
    TourSerializer,
    BuyTourSerializer,
    UserTourSerializer,
    CreateTourSerializer,
    SharePrivateTourSerializer,
)


class ToursViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TourSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTourSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        current_user = self.request.user
        queryset = (
            Tour.objects.prefetch_related(
                Prefetch("sites", queryset=Site.objects.order_by("toursite__order")), "sites__base_site"
            )
            .annotate(is_owned=Exists(UserTour.objects.filter(user_id=current_user.id, tour=OuterRef("pk"))))
            .filter(is_enabled=True, is_approved=True)
        )
        return queryset

    @transaction.atomic
    @action(detail=True, methods=["post"], serializer_class=BuyTourSerializer)
    def buy(self, request, pk):
        serializer = BuyTourSerializer(data={}, context={"request": request, "tour_id": pk})

        serializer.is_valid(raise_exception=True)
        created_user_tour = serializer.save()

        return Response(
            data=UserTourSerializer(created_user_tour, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    @action(detail=True, methods=["post"], serializer_class=SharePrivateTourSerializer)
    def share(self, request, pk):
        serializer = SharePrivateTourSerializer(data=request.data, context={"request": request, "tour_id": pk})

        serializer.is_valid(raise_exception=True)
        shared = serializer.save()

        return Response(data=SharePrivateTourSerializer(shared).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], serializer_class=ReviewSerializer, url_path="reviews")
    def reviews(self, request, pk):
        tour = get_object_or_404(Tour, id=pk)

        queryset = Review.objects.filter(is_approved=True, tour=tour).select_related("reviewers")

        paginated_queryset = self.paginate_queryset(queryset=queryset)
        serializer_data = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer_data.data)
