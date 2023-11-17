from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.reviews.views import ReviewView

router = DefaultRouter()

router.register(r"reviews", ReviewView, basename="review")

urlpatterns = [
    path("", include(router.urls)),
]
