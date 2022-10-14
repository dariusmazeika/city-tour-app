from django.core import mail
from django.urls import reverse
from model_bakery.baker import make
import pytest
from rest_framework import status

from apps.home.models import EmailTemplate, EmailTemplateTranslation, SiteConfiguration
from apps.translations.models import Language
from apps.users.models import ActivationKey, PasswordKey
from apps.utils.tasks import send_email_task
from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestSendEmail:
    def _add_email_template_and_translation(
        self,
        site_config: SiteConfiguration,
        template_name: str,
        language: Language,
        dynamic_content_fragment: str,
    ) -> None:
        template, _create = EmailTemplate.objects.get_or_create(name=template_name)
        setattr(site_config, template_name, template)
        subject = "Subject"
        content = f"Follow this link: {{{{ {dynamic_content_fragment} }}}}"
        make(EmailTemplateTranslation, language=language, template=template, subject=subject, content=content)

    # @pytest.fixture
    # def default_language(self, settings):
    #     settings.DEFAULT_LANGUAGE = "en"
    #     return Language.objects.get_or_create(code=settings.DEFAULT_LANGUAGE, defaults={"name": "Default Language"})
    #     [0]

    @pytest.fixture
    def unverified_user(self, user):
        user.is_verified = False
        user.save(update_fields=["is_verified"])
        return user

    @pytest.fixture(autouse=True)
    def set_default_language_and_site_configuration(self, default_language, unverified_user):
        site_config = SiteConfiguration.get_solo()
        site_config.enabled_languages.add(default_language)

        self._add_email_template_and_translation(
            site_config, "password_renewal_template", default_language, "passwordUrl"
        )
        self._add_email_template_and_translation(
            site_config, "verify_email_template", default_language, "activationUrl"
        )
        site_config.save()

    def test_send_email_task(self, unverified_user, settings):
        password_url = "http://example.com/api/reset"  # noqa: S105
        send_email_task(
            email=unverified_user.email, template="password_renewal_template", context={"passwordUrl": password_url}
        )
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [unverified_user.email]
        assert mail.outbox[0].subject == "Subject"
        assert password_url in mail.outbox[0].body

    def test_send_email_task_with_cc_and_bcc(self, unverified_user):
        cc = ["test1@example.com", "test2@example.com"]
        bcc = ["test3@example.com"]

        password_url = "http://example.com/api/reset"  # noqa: S105
        send_email_task(
            email=unverified_user.email,
            cc=cc,
            bcc=bcc,
            template="password_renewal_template",
            context={"passwordUrl": password_url},
        )
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [unverified_user.email]
        assert mail.outbox[0].cc == cc
        assert mail.outbox[0].bcc == bcc
        assert mail.outbox[0].subject == "Subject"
        assert password_url in mail.outbox[0].body

    def test_resend_verification_email(self, settings, client, unverified_user):
        data = {"email": unverified_user.email}
        url = reverse("resend-verification")

        response = client.post(url, data=data, format="json", query_limit=6)
        activation_key = ActivationKey.objects.get(user=unverified_user).activation_key
        activation_url = settings.VERIFICATION_BASE_URL.format(settings.APP_HOST, activation_key)

        assert response.status_code, status.HTTP_204_NO_CONTENT
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [unverified_user.email]
        assert mail.outbox[0].subject == "Subject"
        assert activation_url in mail.outbox[0].body

    def test_send_password_renewal_email(self, settings, unverified_user, client: APIClientWithQueryCounter):
        data = {"email": unverified_user.email}
        url = reverse("forgot")

        response = client.post(url, data=data, format="json", query_limit=7)
        password_key = PasswordKey.objects.get(user=unverified_user).password_key
        password_url = settings.RESET_PASSWORD_BASE_URL.format(settings.APP_HOST, password_key)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [unverified_user.email]
        assert mail.outbox[0].subject == "Subject"
        assert password_url in mail.outbox[0].body
