from rest_framework import mixins, viewsets

from apps.reviews.serializers import ReviewSerializer


class ReviewView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
