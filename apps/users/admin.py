from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.tours.models import Tour, UserTours
from apps.users.models import User


class CreatedTourInline(admin.StackedInline):
    model = Tour
    verbose_name = _("Created Tour")
    extra = 0


class BoughtTourInline(admin.StackedInline):
    model = UserTours
    verbose_name = _("Bought Tour")
    extra = 0


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "password_last_change", "balance")},
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_verified", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    ]
    ordering = ("-id",)
    search_fields = ("first_name", "last_name", "email")
    exclude = []

    inlines = [CreatedTourInline, BoughtTourInline]


admin.site.register(User, CustomUserAdmin)
