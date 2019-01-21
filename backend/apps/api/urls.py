# pylint: disable=invalid-name
"""
urls.py
API level urls
"""
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users.views import LoginView, LogoutView

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]


