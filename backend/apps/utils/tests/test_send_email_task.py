from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from model_bakery.baker import make

from apps.home.models import EmailTemplate, EmailTemplateTranslation, SiteConfiguration
from apps.translations.models import Language
from apps.utils.tasks import send_email_task


@override_settings(DEFAULT_LANGUAGE='en')
class SendEmailTestCase(TestCase):
    def setUp(self):
        language = Language.objects.create(code='en', name='English')
        self.template_name = 'password_renewal_template'
        template = make(EmailTemplate, name=self.template_name)
        self.subject = 'Password renewal'
        self.content = 'To reset your password, follow this link: {{ password_url }}.'
        make(EmailTemplateTranslation, language=language, template=template, subject=self.subject, content=self.content)

        site_config = SiteConfiguration.get_solo()
        site_config.password_renewal_template = template
        site_config.enabled_languages.add(language)
        site_config.save()

        self.email = 'test@example.com'

    def test_send_email_task(self):
        password_url = 'http://example.com/api/reset'  # noqa: S105
        send_email_task(
            email=self.email,
            template=self.template_name,
            context={'password_url': password_url}
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.email])
        self.assertEqual(mail.outbox[0].subject, self.subject)
        self.assertIn(password_url, mail.outbox[0].body)

    def test_send_email_task_with_cc_and_bcc(self):
        cc = ['test1@example.com', 'test2@example.com']
        bcc = ['test3@example.com']

        password_url = 'http://example.com/api/reset'  # noqa: S105
        send_email_task(
            email=self.email,
            cc=cc,
            bcc=bcc,
            template=self.template_name,
            context={'password_url': password_url}
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.email])
        self.assertEqual(mail.outbox[0].cc, cc)
        self.assertEqual(mail.outbox[0].bcc, bcc)
        self.assertEqual(mail.outbox[0].subject, self.subject)
        self.assertIn(password_url, mail.outbox[0].body)
