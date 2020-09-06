from django.contrib import admin
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin

from apps.home.models import SiteConfiguration, EmailTemplateTranslation, EmailTemplate


@admin.register(SiteConfiguration)
class ConfigAdmin(SingletonModelAdmin):
    readonly_fields = ('manifest_version', 'regenerate_cache')

    fields = ('enabled_languages', 'manifest_version', 'regenerate_cache', 'default_language',
              'password_renewal_template', 'verify_email_template',)

    @staticmethod
    def regenerate_cache(*args):
        return format_html('<a class="button" href="/admin/regenerate_cache/">Regenerate cache</a>', *args)

    # can only ignore here, the issue is known and is still open to this day
    # https://github.com/python/mypy/issues/2087
    regenerate_cache.short_description = 'Regenerate cache'  # type: ignore
    regenerate_cache.allow_tags = True  # type: ignore


class TemplateTranslationInline(admin.TabularInline):
    model = EmailTemplateTranslation
    extra = 0


@admin.register(EmailTemplate)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)

    inlines = [
        TemplateTranslationInline
    ]
