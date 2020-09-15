from django.conf import settings
from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    flag = models.ImageField(upload_to='languages', blank=True, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super(Language, self).save(*args, **kwargs)


class Message(models.Model):
    message_id = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.message_id


class TranslationManager(models.Manager):
    def get_by_natural_key(self, message_pk, language_pk):
        return self.get(message=message_pk, language=language_pk)


class Translation(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, default=settings.TRANSLATIONS_BASE_LANGUAGE[0], on_delete=models.CASCADE)
    text = models.TextField()

    objects = TranslationManager()

    def __str__(self):
        return '{}'.format(self.language)

    def natural_key(self):
        return self.message.pk, self.language.pk

    class Meta:
        unique_together = (('message', 'language'),)
