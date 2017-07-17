from django.conf.urls import url, include
from apps.api.views import PartnerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'partners', PartnerViewSet)



urlpatterns = [
    url(r'^', include(router.urls))
]
