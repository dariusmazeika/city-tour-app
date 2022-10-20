import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from solo.models import SingletonModel

from apps.utils.validation import check_template

LOGGER = logging.getLogger("app")


class SiteConfiguration(SingletonModel):
    enabled_languages = models.ManyToManyField("translations.Language", related_name="enabled_inform_languages")
    default_language = models.ForeignKey(
        "translations.Language",
        related_name="default_inform_language",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    manifest_version = models.CharField(max_length=300, default="1")
    password_renewal_template = models.ForeignKey(
        "home.EmailTemplate", related_name="password_renewal_template", blank=True, null=True, on_delete=models.SET_NULL
    )
    verify_email_template = models.ForeignKey(
        "home.EmailTemplate", related_name="verify_email_template", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Site Configuration"

    def save(self, *args, **kwargs):
        self.manifest_version = uuid.uuid4().hex
        return super(SiteConfiguration, self).save(*args, **kwargs)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class EmailTemplateTranslation(models.Model):
    content = RichTextField()
    language = models.ForeignKey(
        "translations.Language",
        default=settings.DEFAULT_LANGUAGE,
        on_delete=models.SET_DEFAULT,
    )
    subject = models.CharField(max_length=100)
    template = models.ForeignKey(
        "home.EmailTemplate",
        related_name="translations",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("template", "language"),)

    def __str__(self):
        return f"{self.subject} {self.language}"

    def clean(self):
        check_template(self.content)
