from django.db import transaction
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.tours.models import Tour
from apps.tours.serializers import TourSerializer, TourWithoutSitesSerializer, BuyTourSerializer


class ToursViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (AllowAny,)
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    @action(detail=True, methods=["post"], serializer_class=BuyTourSerializer, permission_classes=(IsAuthenticated,))
    def buy(self, request, pk):
        with transaction.atomic():
            serializer = BuyTourSerializer(data={}, context={"request": request, "pk": pk})

            if serializer.is_valid():
                tour_to_buy = self.get_queryset().filter(id=pk).first()
                serializer.create_user_tour(tour_to_buy, request.user)

                return Response(data=TourWithoutSitesSerializer(tour_to_buy).data,
                                status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
