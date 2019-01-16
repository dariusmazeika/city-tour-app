import json
import logging

from apps.home.models import SiteConfiguration
from apps.translations.models import Language, Translation
from django.conf import settings

logger = logging.getLogger('id.manifest')


def get_translations(language):
    translations = Translation.objects.all().filter(language=language)
    return dict([(trans.message.message_id, trans.text) for trans in translations])


def generate_messages():
    translations = {}
    for language in Language.objects.all():
        translations[language.pk] = get_translations(language)
    return translations


def get_enabled_languages(config):
    return list(
        {
            'code': lang.pk,
            'flag': lang.flag.url if lang.flag else '',
            'name': lang.name
        } for lang in config.enabled_languages.all()
    )


def get_enabled_languages(config):
    return list(
        {
            'code': lang.pk.upper(),
            'name': lang.name
        } for lang in config.enabled_languages.all()
    )


def get_page_translations(page, add_content=False):
    if page is None:
        return ''
    translations = {}
    icon = None
    if page.icon:
        icon = page.icon.url
    for translation in page.page_translations.all():
        translations[translation.language.pk] = {
            'slug': translation.slug,
            'title': translation.title,
            'icon': icon,
            'content': translation.text if add_content else None
        }
    return translations

def generate_const():
    return {}


def generate_manifest():
    site_config = SiteConfiguration.get_solo()
    config = {
        'enabled_languages': get_enabled_languages(site_config),
        'enabled_inform_languages': get_enabled_languages(site_config),
        'default_language': 'lt',
        'default_language': site_config.default_language.code.upper(),
    }

    js = """
    window._id_messages = {};
    window._id_constants = {};
    window._id_conf = {}
    """.format(
        json.dumps(generate_messages()),
        json.dumps(generate_const()),
        json.dumps(config),
    )
    return js
