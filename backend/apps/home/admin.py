from django.contrib import admin
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin

from apps.home.models import SiteConfiguration


@admin.register(SiteConfiguration)
class ConfigAdmin(SingletonModelAdmin):
    readonly_fields = ('manifest_version', 'regenerate_cache')

    fields = ('enabled_languages', 'manifest_version', 'regenerate_cache', 'default_language')

    @staticmethod
    def regenerate_cache(*args):
        return format_html('<a class="button" href="/admin/regenerate_cache/">Regenerate cache</a>', *args)

    regenerate_cache.short_description = 'Regenerate cache'
    regenerate_cache.allow_tags = True
