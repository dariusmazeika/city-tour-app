from django.contrib import admin

from apps.reviews.models import Review
from apps.sites.admin import ApprovalFilter


class ReviewAdmin(admin.ModelAdmin):
    list_filter = (ApprovalFilter,)
    list_display = ("id", "rating", "is_approved")


admin.site.register(Review, ReviewAdmin)
