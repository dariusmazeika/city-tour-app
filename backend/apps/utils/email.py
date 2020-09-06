import json
import logging
import mimetypes

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from premailer import transform

from apps.utils.templates import render_template_message

LOGGER = logging.getLogger('app')


PASSWORD_RESET_EMAIL_TEMPLATE = 'get_password_renewal_template'
PASSWORD_RESET_EMAIL_CATEGORY = 'Password Reset Email'

VERIFICATION_EMAIL_TEMPLATE = 'get_verification_template'
VERIFICATION_EMAIL_CATEGORY = 'Verify Email'


def send_email(email: str, subject: str, html_message: str, attachments: list = None, category: str = None) -> None:
    if attachments is None:
        attachments = []
    try:
        email_msg = EmailMessage(
            subject=subject,
            body=html_message,
            to=[email],
            attachments=[
                (filename, content, mimetypes.guess_type(filename)[0] or 'application/octet-stream')
                for filename, content in attachments
            ],
            headers={'X-SMTPAPI': json.dumps({'category': category or 'Email'})}
        )
        email_msg.content_subtype = 'html'
        email_msg.send()
        LOGGER.info('email sent to %s with subject %s', email, subject)
    except Exception as e:
        LOGGER.error('failed to send email to %s error %s', email, e)


def render_email_template_with_base(html_content: str, context: dict = None, subject: str = '') -> str:
    if not context:
        context = {}
    context['subject'] = subject
    context['custom_email_html'] = render_template_message(html_content, context)
    return transform(render_to_string('emails/base-email-template.html', context))
