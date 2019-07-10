# pylint: disable=invalid-name
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path

from apps.manifests.views import RegenerateManifest

urlpatterns = list()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [path('static/<path>', serve)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('admin/regenerate_cache/', RegenerateManifest.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('manifest/', include('apps.manifests.urls')),

    path('', include('apps.home.urls'))
]
