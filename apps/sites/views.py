from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.permissions import IsAuthenticated

from apps.sites.models import BaseSite, Site, SiteImage
from apps.sites.serializers import CreateSiteSerializer, CreateBaseSiteSerializer, CreateSiteImageSerializer


class SiteViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Site.objects.all()
    serializer_class = CreateSiteSerializer


class BaseSiteViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = BaseSite.objects.all()
    serializer_class = CreateBaseSiteSerializer

    parser_classes = (FormParser, MultiPartParser, FileUploadParser)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UploadImageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = SiteImage.objects.all()
    serializer_class = CreateSiteImageSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser)
