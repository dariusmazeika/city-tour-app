from django.urls import path, include
from rest_framework import routers

from apps.locations import views


router = routers.DefaultRouter()

router.register(r"countries", views.CountryViewSet, basename="country")
router.register(r"cities", views.CityViewSet, basename="city")
router.register(r"cities/(?P<city_id>\d+)/tours", views.CityTourListViewSet, basename="city-tours")

urlpatterns = [
    path("", include(router.urls)),
]
