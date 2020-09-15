from django.contrib import admin
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from tabbed_admin import TabbedModelAdmin

from apps.home.models import SiteConfiguration, EmailTemplateTranslation, EmailTemplate


@admin.register(SiteConfiguration)
class ConfigAdmin(TabbedModelAdmin, SingletonModelAdmin):
    readonly_fields = ('manifest_version', 'regenerate_cache')

    tab_overview = (
        (None, {
            'fields': (
                ('default_language', 'enabled_languages',),
                ('regenerate_cache', 'manifest_version',),
            )
        }),
    )

    tab_emails = (
        (None, {
            'fields': (
                ('password_renewal_template', 'verify_email_template',),)
        }),
    )

    tabs = [
        ('Overview', tab_overview),
        ('Emails', tab_emails),
    ]

    @staticmethod
    def regenerate_cache(*args):
        hyper = format_html('<a class="button" href="/admin/regenerate_cache/">Regenerate cache</a>', *args)
        hyper.short_description = 'Regenerate cache'
        hyper.allow_tags = True
        return hyper


class TemplateTranslationInline(admin.TabularInline):
    model = EmailTemplateTranslation
    extra = 0


@admin.register(EmailTemplate)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)

    inlines = [
        TemplateTranslationInline
    ]
