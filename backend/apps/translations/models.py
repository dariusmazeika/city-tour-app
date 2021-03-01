from django.core.exceptions import ValidationError
from django.db import models

from apps.translations.utils import BaseTranslatableResourceModel, BaseTranslationModel, TranslatableResourceForeignKey


class Language(models.Model):
    code = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    flag = models.ImageField(upload_to='languages', blank=True, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super(Language, self).save(*args, **kwargs)


class Message(BaseTranslatableResourceModel):
    message_id = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.message_id

    def save(self, *args, **kwargs):
        self.message_id = self.message_id.lower()
        return super().save(*args, **kwargs)

    def clean(self):
        if not self.message_id.startswith('msg_'):
            raise ValidationError('Translation key must start with `msg_` prefix')


class TranslationManager(models.Manager):
    def get_by_natural_key(self, message_pk, language_pk):
        return self.get(message=message_pk, language=language_pk)


class Translation(BaseTranslationModel):
    message = TranslatableResourceForeignKey(Message)

    objects = TranslationManager()

    class Meta:
        unique_together = (('message', 'language'),)

    def __str__(self):
        return '{}'.format(self.language)

    def natural_key(self):
        return self.message.pk, self.language.pk
