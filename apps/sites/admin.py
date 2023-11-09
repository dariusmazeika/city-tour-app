from django.contrib import admin

from apps.sites.models import Site, BaseSite, SiteImage, SiteAudio, SiteTag


class RelatedSites(admin.StackedInline):
    model = Site
    extra = 0


class BaseSiteAdmin(admin.ModelAdmin):
    inlines = [RelatedSites]


admin.site.register(BaseSite, BaseSiteAdmin)
admin.site.register(Site)
admin.site.register(SiteImage)
admin.site.register(SiteAudio)
admin.site.register(SiteTag)
