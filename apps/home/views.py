from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@extend_schema(responses={status.HTTP_200_OK: OpenApiTypes.INT})
class BuildVersionView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        version = settings.BUILD_VERSION
        return Response(int(version) if version else 0)
