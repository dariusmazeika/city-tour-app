from django.contrib import admin

from apps.tours.models import Tour, TourSite, UserTour, SharedPrivateTour


class TourSiteInline(admin.StackedInline):
    model = TourSite
    extra = 0


class TourAdmin(admin.ModelAdmin):
    inlines = [TourSiteInline]


admin.site.register(Tour, TourAdmin)
admin.site.register(TourSite)
admin.site.register(UserTour)
admin.site.register(SharedPrivateTour)
