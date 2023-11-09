from django.contrib import admin

from apps.locations.models import City, Country

admin.site.register(City)
admin.site.register(Country)
