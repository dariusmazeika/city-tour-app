from django.urls import path

from apps.home.views import index as index_view

urlpatterns = [
    path('', index_view, name='index')
]
