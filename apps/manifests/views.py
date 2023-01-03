import uuid

from django.shortcuts import redirect
from django.views import View
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home.models import SiteConfiguration
from apps.manifests.generator import generate_config


@extend_schema(responses={status.HTTP_200_OK: None})
class AppConfigView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(generate_config())


class RegenerateManifest(View):
    def get(self, request):
        if request.user.is_authenticated:
            site_config = SiteConfiguration.get_solo()
            site_config.manifest_version = uuid.uuid4().hex
            site_config.save()
        return redirect(request.META["HTTP_REFERER"])
