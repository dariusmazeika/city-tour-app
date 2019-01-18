from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from apps.manifests.views import RegenerateManifest
from apps.users.views import LoginView, LogoutView

urlpatterns = [
    path('admin/regenerate_cache/', RegenerateManifest.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('manifest/', include('apps.manifests.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('apps.home.urls'))
]
