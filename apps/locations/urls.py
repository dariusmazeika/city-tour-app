from django.urls import path, include
from rest_framework import routers

from apps.locations import views


router = routers.DefaultRouter()
router.register(r"countries", views.CountryViewSet, basename="country")

urlpatterns = [
    path("", include(router.urls)),
]
