# pylint: disable=invalid-name
"""
Base URL configuration.
This configuration is dedicated for loading static bundle onto the root path of the site.
"""
from django.urls import re_path

from apps.home.views import index as index_view

urlpatterns = [
    re_path('^.*?', index_view, name='index')

]
