# pylint: disable=broad-except
import logging

from apps.celery import app
from apps.home.models import SiteConfiguration
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
        site_config = SiteConfiguration.get_solo()

        template = getattr(site_config, template)(language)
        html_message = render_email_template_with_base(html_content=template.content, context=context,
                                                       subject=template.subject)
        send_email(email=email, subject=template.subject, html_message=html_message, category=category)
    except Exception as e:
        LOGGER.error('Error during sending %s: %s ', template, e)
