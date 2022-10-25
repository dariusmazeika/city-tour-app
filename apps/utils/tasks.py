import logging
from typing import List, Optional

from django.conf import settings

from apps.home.models import EmailTemplate, EmailTemplateTranslation
from apps.translations.exceptions import MissingTemplateTranslationError
from apps.utils.email import render_email_template_with_base, send_email
from conf.celery import app

LOGGER = logging.getLogger("app")


@app.task
def send_template_email_task(  # noqa: CFQ002
    email: str,
    template_id: int,
    category: Optional[str] = None,
    context: Optional[dict] = None,
    language: Optional[str] = settings.DEFAULT_LANGUAGE,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
):
    """Email send task, use template ant its translations to fill all email content."""
    try:
        LOGGER.info("sending email using template (%s) to %s ", template_id, email)
        template = EmailTemplate.objects.get(id=template_id)
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
        LOGGER.error(f"Error when sending email to {email} with template ({template_id}): {e}")  # noqa: G200


def _get_translation(template: EmailTemplate, language: str = settings.DEFAULT_LANGUAGE) -> EmailTemplateTranslation:
    if translation := template.translations.filter(language=language).first():
        return translation
    else:
        error_msg = f"No email template translation for template ({template}) in {language} language."
        LOGGER.error(error_msg)
        raise MissingTemplateTranslationError(error_msg)
