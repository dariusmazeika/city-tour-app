from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from watchman.views import bare_status

from apps.home.views import BuildVersionView
from apps.manifests.views import RegenerateManifest

urlpatterns = []

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [path('static/<path>', serve)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    # Admin
    path('admin/regenerate_cache/', RegenerateManifest.as_view(), name="regenerate-cache"),
    path('admin/', admin.site.urls),
    # 3rd party apps
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Local apps
    path("health/", bare_status, name="watchman"),
    path("build-version/", BuildVersionView.as_view(), name="build-version"),
    path('home/', include('apps.home.urls')),
    path('users/', include('apps.users.urls')),
    path('manifests/', include('apps.manifests.urls')),
]

admin.autodiscover()
admin.site.enable_nav_sidebar = False