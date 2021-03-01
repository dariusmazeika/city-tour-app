import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

from apps.utils.models import BaseModel

LOGGER = logging.getLogger('app')


class TranslatableResourceForeignKey(models.ForeignKey):
    """
    FK should point to BaseTranslatableResourceModel.
    """
    related_name = 'translations'

    def __init__(self, to, on_delete=models.CASCADE, **kwargs):
        kwargs['related_name'] = self.related_name
        super().__init__(to=to, on_delete=on_delete, **kwargs)


class BaseTranslationModel(models.Model):
    """
    Base class for translation models.
    """

    language = models.ForeignKey("translations.Language", default=settings.DEFAULT_LANGUAGE, on_delete=models.CASCADE)
    title = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class BaseTopicTranslationModel(BaseTranslationModel):
    description = RichTextField()

    class Meta:
        abstract = True


class BaseTranslatableResourceModel(BaseModel):
    """
    Base class for models which have related translations.
    Provides prefetch_translations method.
    Should be used together with BaseTranslationModel and  TranslatableResourceForeignKey.
    """

    class TranslatableModelQuerySet(models.QuerySet):
        translations_prefetch_name = 'user_translations'

        def prefetch_translations(self, language: str = settings.DEFAULT_LANGUAGE) -> models.QuerySet:
            translation_model = getattr(self.model, TranslatableResourceForeignKey.related_name).rel.related_model
            translations_prefetch = models.Prefetch(
                lookup=TranslatableResourceForeignKey.related_name,
                queryset=translation_model.objects.filter(language=language),
                to_attr=self.translations_prefetch_name
            )
            return self.prefetch_related(translations_prefetch)

    objects = TranslatableModelQuerySet.as_manager()

    name = models.CharField(help_text='Technical name.', unique=True, max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseTopicModel(BaseTranslationModel):
    class Meta:
        abstract = True
