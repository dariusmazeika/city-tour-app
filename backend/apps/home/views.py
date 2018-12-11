"""
views.py
This controller is dedicated for rendering the index.html template, which is responsible for loading the frontend
bundle.
"""
from django.shortcuts import render


def index(request):
    """
    Renders templates/home/index.html template. Basically in this template should be added the constants, which should
    appear in frontend env.
    """
    return render(request, 'home/index.html')
