from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.utils.html import escape, format_html
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


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = [f.name for f in LogEntry._meta.fields]

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'get_change_message',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @staticmethod
    def object_link(obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            link = '<a href="%s">%s</a>' % (
                obj.get_admin_url(),
                escape(obj.object_repr),
            )
        link = format_html(link)
        link.allow_tags = True
        link.admin_order_field = 'object_repr'
        link.short_description = 'object'
        return link

    @staticmethod
    def action_flag(obj):
        action_map = {
            DELETION: 'Deletion',
            CHANGE: 'Change',
            ADDITION: 'Addition',
        }
        return action_map.get(obj.action_flag, obj.action_flag)
