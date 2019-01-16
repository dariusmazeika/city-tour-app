from django.contrib import admin
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from tabbed_admin import TabbedModelAdmin

from apps.home.models import SiteConfiguration

@admin.register(SiteConfiguration)
class ConfigAdmin(TabbedModelAdmin, SingletonModelAdmin):
    readonly_fields = ('manifest_version', 'regenerate_cache')

    tab_general = (
        (None, {
            'fields': ('enabled_languages', 'manifest_version',
                       'regenerate_cache', 'default_language')
        }),
    )


    tabs = [
        ('General', tab_general),
    ]

    def regenerate_cache(self, obj):
        return format_html('<a class="button" href="/admin/regenerate_cache/">Regenerate cache</a>')

    regenerate_cache.short_description = 'Regenerate cache'
    regenerate_cache.allow_tags = True
    