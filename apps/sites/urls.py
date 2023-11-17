from django.urls import path, include
from rest_framework import routers

from apps.sites import views


router = routers.DefaultRouter()

router.register(r"sites", views.SiteViewSet, basename="sites")
router.register(r"basesites", views.BaseSiteViewSet, basename="base-sites")
router.register(r"images", views.UploadImageViewSet, basename="images")

urlpatterns = [
    path("", include(router.urls)),
]
