from django.db import transaction
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.tours.models import Tour
from apps.tours.serializers import (
    TourSerializer,
    BuyTourSerializer,
    UserTourSerializer,
    CreateTourSerializer,
)


class ToursViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tour.objects.filter(is_enabled=True, is_approved=True)
    serializer_class = TourSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTourSerializer
        return super().get_serializer_class()

    @transaction.atomic
    @action(detail=True, methods=["post"], serializer_class=BuyTourSerializer)
    def buy(self, request, pk):
        serializer = BuyTourSerializer(data={}, context={"request": request, "tour_id": pk})

        serializer.is_valid(raise_exception=True)
        created_user_tour = serializer.save()

        return Response(data=UserTourSerializer(created_user_tour).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
