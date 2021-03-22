import logging
from typing import List, Optional

from apps.celery import app
from apps.home.models import EmailTemplateTranslation, SiteConfiguration
from apps.translations.exceptions import MissingTemplateException, MissingTemplateTranslationException
from apps.utils.email import render_email_template_with_base, send_email

LOGGER = logging.getLogger('app')


@app.task
def send_email_task(  # noqa: CFQ002
        email: str,
        template: str,
        category: Optional[str] = None,
        context: Optional[dict] = None,
        language: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
):
    """
    Email send task, which firstly collects all the information from SiteConfiguration
    and then calls send_email function.
    Example call:
    send_email_task.delay('some@email.com', VERIFICATION_EMAIL_TEMPLATE, 'Verify Email', {'context': 'value'}, 'en')
    """
    try:
        LOGGER.info('sending email %s to %s ', template, email)
        translation = _get_translation(template, language)
        html_message = render_email_template_with_base(
            html_content=translation.content,
            context=context,
            subject=translation.subject,
        )
        send_email(
            email=email,
            subject=translation.subject,
            html_message=html_message,
            category=category,
            cc=cc,
            bcc=bcc,
        )
    except Exception as e:  # noqa: B902
        LOGGER.error('Error during sending %s: %s ', translation, e)  # noqa: G200


def _get_translation(template: str, language: str) -> Optional[EmailTemplateTranslation]:
    """
    Gets translation for template.
    Accepts template to be a method or a field of site config.
    This "flexibility" is temporary, while refactoring is in progress:
    - Method is accepted for old parts.
    = Field is accepted for new parts (idea: to avoid the need to create
        duplicated "get_" methods in site config)
    """

    site_config = SiteConfiguration.get_solo()
    site_config_member = getattr(site_config, template)

    if callable(site_config_member):
        return site_config_member(language)

    template = site_config_member
    if template:
        if translation := site_config.get_localized_email_template(template, language):
            return translation
        else:
            error_msg = f'No notification translation {translation}'
            LOGGER.error(error_msg)
            raise MissingTemplateTranslationException(error_msg)
    else:
        error_msg = f'No notification template {template}'
        LOGGER.error(error_msg)
        raise MissingTemplateException(error_msg)
