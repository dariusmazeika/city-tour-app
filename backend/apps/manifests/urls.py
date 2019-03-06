# pylint: disable=invalid-name
from django.conf.urls import url

from apps.manifests.views import ManifestJSView

urlpatterns = [
    url(r'manifest_(?P<manifest_id>.+).js', ManifestJSView.as_view(), name='manifest-js'),
]
