from __future__ import annotations

from django.db import models

from ascii.core.models import BaseModel
from ascii.translations.choices import TranslationLanguages
from ascii.translations.clients import GoogleTranslateClient


class Translation(BaseModel):
    """
    Simple backend for caching results from a translation API.
    """

    language = models.CharField(choices=TranslationLanguages.choices, max_length=10)
    original = models.TextField(db_index=True)
    translated = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["original", "language"],
                name="translation_unique_text",
            )
        ]

    def __str__(self) -> str:
        return f"Translation: {self.pk}"

    @classmethod
    def get_or_translate(
        cls,
        text: str,
        language: TranslationLanguages = TranslationLanguages.CHINESE_SIMPLIFIED,
    ) -> tuple[Translation, bool]:
        try:
            obj = cls.objects.filter(original=text, language=language).get()
            created = False
        except cls.DoesNotExist:
            client = GoogleTranslateClient()
            if text == "":
                translated = text
            else:
                translated = client.translate(text, language)
            obj = cls.objects.create(original=text, translated=translated, language=language)
            created = True

        return obj, created

    def populate_translation(self) -> None:
        client = GoogleTranslateClient()
        self.translated = client.translate(self.original, self.language)  # noqa
        self.save(update_fields=["translated"])
