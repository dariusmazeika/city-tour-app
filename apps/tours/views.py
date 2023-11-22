from django.db import transaction
from django.db.models import Exists, OuterRef
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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
    queryset = Tour.objects.filter(is_enabled=True, is_approved=True)
    serializer_class = TourSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTourSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        current_user = self.request.user
        queryset = (
            Tour.objects.prefetch_related("sites")
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
