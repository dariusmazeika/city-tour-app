import json
import logging
import mimetypes
from typing import List, Optional

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from premailer import transform

from apps.utils.templates import render_template_message

LOGGER = logging.getLogger("app")


def send_email(  # noqa: CFQ002
    email: str,
    subject: str,
    html_message: str,
    attachments: Optional[list] = None,
    category: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
) -> None:
    attachments = attachments or []
    email_msg = EmailMessage(
        subject=subject,
        body=html_message,
        to=[email],
        cc=cc,
        bcc=bcc,
        attachments=[
            (filename, content, mimetypes.guess_type(filename)[0] or "application/octet-stream")
            for filename, content in attachments
        ],
        headers={"X-SMTPAPI": json.dumps({"category": category or "Email"})},
    )
    email_msg.content_subtype = "html"
    email_msg.send()
    LOGGER.info("email sent to %s with subject %s", email, subject)


def render_email_template_with_base(html_content: str, context: dict = None, subject: str = "") -> str:
    if not context:
        context = {}
    context["subject"] = subject
    context["custom_email_html"] = render_template_message(html_content, context)
    return transform(render_to_string("emails/base-email-template.html", context))
