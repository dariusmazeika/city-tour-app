from django.contrib import admin

from apps.sites.models import Site, BaseSite, SiteImage, SiteAudio, SiteTag


class RelatedSites(admin.StackedInline):
    model = Site
    extra = 0


class BaseSiteAdmin(admin.ModelAdmin):
    inlines = [RelatedSites]


class ApprovalFilter(admin.SimpleListFilter):
    title = "Approval Status"
    parameter_name = "is_approved"

    def lookups(self, request, model_admin):
        return (
            ("approved", "Approved"),
            ("not_approved", "Not Approved"),
        )

    def queryset(self, request, queryset):
        if self.value() == "approved":
            return queryset.filter(is_approved=True)
        elif self.value() == "not_approved":
            return queryset.filter(is_approved=False)


class CustomSiteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "base_site",
        "author_email",
        "is_approved",
    )
    list_filter = (ApprovalFilter,)

    def author_email(self, obj):
        return obj.author.email if obj.author else "Unknown"


admin.site.register(BaseSite, BaseSiteAdmin)
admin.site.register(SiteImage)
admin.site.register(SiteAudio)
admin.site.register(SiteTag)
admin.site.register(Site, CustomSiteAdmin)
