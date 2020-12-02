"""
urls.py
API level urls
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from watchman.views import bare_status

from apps.api.views import BuildVersionView

router = DefaultRouter()

urlpatterns = [
    path("health/", bare_status, name="watchman"),
    path("build-version/", BuildVersionView.as_view(), name="build-version"),
]
