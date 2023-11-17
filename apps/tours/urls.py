from django.urls import path, include
from rest_framework import routers

from apps.tours import views

router = routers.DefaultRouter()
router.register(r"tours", views.ToursViewSet, basename="tours")

urlpatterns = [
    path("", include(router.urls)),
]
