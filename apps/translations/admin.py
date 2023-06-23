from django.contrib import admin
from django.forms import ValidationError, ModelForm, Textarea
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html_join

from apps.translations.models import Language, Message, Translation

admin.site.register(Language)


class BaseTranslationFormSet(BaseInlineFormSet):
    """Validate that there's no duplicate translation"""

    def clean(self):
        if any(self.errors):
            return
        uniq = set()
        has_default = False
        for form in self.forms:
            if form.cleaned_data.get("text"):
                language = form.cleaned_data.get("language")

                key = language.pk
                if key in uniq:
                    raise ValidationError("Cannot have multiple default {} messages".format(language))
                uniq.add(key)

                if language and form.cleaned_data.get("text"):
                    has_default = True

        if not has_default:
            raise ValidationError("Default translation must exist.")


class TranslationForm(ModelForm):
    class Meta:
        fields = ("language", "text")
        model = Translation
        widgets = {
            "text": Textarea(attrs={"cols": 40, "rows": 2}),
        }


class TranslationInline(admin.TabularInline):
    model = Translation
    formset = BaseTranslationFormSet  # type: ignore
    form = TranslationForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields = ("message_id", "translation__text")
    list_display = ("message_id", "trans")
    inlines = [TranslationInline]

    @admin.display(description="Translations")  # type: ignore [attr-defined]
    def trans(self, obj):
        return format_html_join(
            "\n",
            '<b>{}:</b> "{}"<br/>',
            (tuple(t) for t in obj.translation_set.prefetch_related("language").values_list("language__code", "text")),
        )
