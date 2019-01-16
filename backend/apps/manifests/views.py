import uuid

from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect

from apps.home.models import SiteConfiguration
from apps.manifests.generator import generate_manifest


class ManifestJSView(View):

    def get(self, request, manifest_id):
        response = HttpResponse(content_type='application/javascript; charset=utf-8')
        response['Cache-Control'] = 'max-age={}'.format(settings.MANIFEST_JS_MAX_AGE)
        response.write(generate_manifest())
        return response


class RegenerateManifest(View):
    def get(self, request):
        if request.user.is_authenticated:
            site_config = SiteConfiguration.get_solo()
            site_config.manifest_version = uuid.uuid4().hex
            site_config.save()
        return redirect(request.META['HTTP_REFERER'])