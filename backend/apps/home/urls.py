# pylint: disable=invalid-name
"""
Base URL configuration.
This configuration is dedicated for loading frontend bundle onto the root path of the site.
"""
from django.urls import path

from apps.home.views import index as index_view

urlpatterns = [
    path('', index_view, name='index')
]
