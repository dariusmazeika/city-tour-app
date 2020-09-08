import logging
from typing import Optional


from apps.celery import app
from apps.home.models import SiteConfiguration, EmailTemplateTranslation
from apps.utils.email import send_email, render_email_template_with_base

LOGGER = logging.getLogger('app')


@app.task
def send_email_task(email: str, template: str, category: str = None, context: dict = None, language: str = None):
    """
    Email send task, which firstly collects all the information from SiteConfiguration
    and then calls send_email function.
    Example call:
    send_email_task.delay('some@email.com', VERIFICATION_EMAIL_TEMPLATE, 'Verify Email', {'context': 'value'}, 'en')
    """
    try:
        LOGGER.info('sending email %s to %s ', template, email)
        translation = _get_translation(template, language)
        html_message = render_email_template_with_base(html_content=translation.content, context=context,
                                                       subject=translation.subject)
        send_email(email=email, subject=translation.subject, html_message=html_message, category=category)
    except Exception as e:
        LOGGER.error('Error during sending %s: %s ', translation, e)


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
        return site_config.get_localized_email_template(template, language)
    error_msg = f'No notification template {template}'
    LOGGER.error(error_msg)
    raise Exception(error_msg)
