from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.users.models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser',
                    'date_joined',
                    'last_login']
    ordering = ('-id',)
    search_fields = ('first_name', 'last_name', 'email')
    exclude = []


admin.site.register(User, UserAdmin)
