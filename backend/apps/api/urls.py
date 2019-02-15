# pylint: disable=invalid-name
"""
urls.py
API level urls
"""
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users.views import LoginView, LogoutView, GetUserView

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('current-user/', GetUserView.as_view(), name='current-user'),
    path('', include(router.urls)),
]
