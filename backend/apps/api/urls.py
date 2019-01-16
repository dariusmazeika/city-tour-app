# pylint: disable=invalid-name
"""
urls.py
API level urls
"""
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]
