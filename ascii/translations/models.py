from __future__ import annotations

from django.db import models

from ascii.core.fields import NonStrippingTextField
from ascii.core.models import BaseModel
from ascii.translations.choices import TranslationLanguages
from ascii.translations.clients import GoogleTranslateClient


class Translation(BaseModel):
    """
    Simple backend for caching results from a translation API.
    """

    language = models.CharField(choices=TranslationLanguages.choices, max_length=10)
    original = NonStrippingTextField(db_index=True)
    translated = NonStrippingTextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["original", "language"],
                name="translation_unique_text",
            )
        ]

    def __str__(self) -> str:
        return f"Translation: {self.pk}"

    def populate_translation(self) -> None:
        client = GoogleTranslateClient()
        self.translated = client.translate(self.original, self.language)  # noqa
