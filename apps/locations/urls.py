from django.urls import path, include
from rest_framework import routers

from apps.locations import views


class OptionalTrailingSlashRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = "/?"


router = OptionalTrailingSlashRouter()

router.register(r"countries", views.CountryViewSet, basename="country")
router.register(r"cities", views.CityViewSet, basename="city")
router.register(r"cities/(?P<city_id>\d+)/tours", views.CityTourListViewSet, basename="city-tours")

urlpatterns = [
    path("", include(router.urls)),
]
