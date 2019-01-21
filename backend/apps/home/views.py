"""
views.py
This controller is dedicated for rendering the index.html template, which is responsible for loading the frontend
bundle.
"""
from django.shortcuts import render
from django.urls import reverse

from apps.home.models import SiteConfiguration


def index(request):
    """
    Renders templates/home/index.html template. Basically in this template should be added the constants, which should
    appear in frontend env.
    """
    site_config = SiteConfiguration.get_solo()

    context = {
        'manifest_js_url': reverse('manifest-js', kwargs={'manifest_id': site_config.manifest_version}),
    }

    response = render(request, 'home/index.html', context)

    return response
