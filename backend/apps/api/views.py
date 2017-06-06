from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PartnerSerializer
from apps.partners.models import Partner
# Create your views here.
class PartnerViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
