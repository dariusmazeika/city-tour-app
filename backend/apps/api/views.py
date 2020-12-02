from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class BuildVersionView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        version = settings.BUILD_VERSION
        return Response(int(version) if version else 0)
