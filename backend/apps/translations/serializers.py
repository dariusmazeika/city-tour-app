from typing import Optional

from rest_framework import serializers

from apps.translations.utils import BaseTopicTranslationModel, BaseTranslatableResourceModel


class BaseTranslatableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = BaseTranslatableResourceModel
        fields = ['id', 'title']

    @staticmethod
    def _get_user_translation(instance: BaseTranslatableResourceModel) -> Optional[BaseTopicTranslationModel]:
        translations_prefetch_name = BaseTranslatableResourceModel.TranslatableModelQuerySet.translations_prefetch_name
        user_translations = getattr(instance, translations_prefetch_name, None)
        return user_translations[0] if user_translations else None

    def get_title(self, instance: BaseTranslatableResourceModel) -> str:
        translation = self._get_user_translation(instance)
        return translation.title if translation else instance.name


class BaseTranslatableTopicSerializer(BaseTranslatableSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = BaseTranslatableResourceModel
        fields = BaseTranslatableSerializer.Meta.fields + ['description']

    def get_description(self, instance: BaseTranslatableResourceModel) -> str:
        translation = self._get_user_translation(instance)
        return translation.description if translation else ''
