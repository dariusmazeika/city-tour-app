from django.db import transaction
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.tours.models import Tour
from apps.tours.serializers import TourSerializer, BuyTourSerializer, UserTourSerializer


class ToursViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (AllowAny,)
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    @transaction.atomic
    @action(detail=True, methods=["post"], serializer_class=BuyTourSerializer, permission_classes=(IsAuthenticated,))
    def buy(self, request, pk):
        serializer = BuyTourSerializer(data={}, context={"request": request, "tour_id": pk})

        serializer.is_valid(raise_exception=True)
        created_user_tour = serializer.save()

        return Response(data=UserTourSerializer(created_user_tour).data, status=status.HTTP_201_CREATED)
