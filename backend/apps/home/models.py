from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    enabled_languages = models.ManyToManyField('translations.Language', related_name='enabled_inform_languages')
    default_language = models.ForeignKey(
        'translations.Language',
        related_name='default_inform_language',
        null=True,
        blank=True, on_delete=models.CASCADE
    )
    manifest_version = models.CharField(max_length=300, default='1')

    class Meta:
        verbose_name = "Site Configuration"
