from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.text import Truncator

from ascii.translations.models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ["id", "language", "get_truncated_original", "get_truncated_translated"]
    actions = ["populate_translations"]
    readonly_fields = ["get_truncated_original", "get_truncated_translated"]
    fields = ["language", "original", "translated"]

    @admin.display(description="Original", ordering="original")
    def get_truncated_original(self, obj: Translation) -> str:
        return Truncator(obj.original).chars(40)

    @admin.display(description="Translated", ordering="translated")
    def get_truncated_translated(self, obj: Translation) -> str:
        return Truncator(obj.translated).chars(40)

    @admin.display(description="Populate translations")
    def populate_translations(self, request: HttpRequest, queryset: models.QuerySet) -> None:
        for translation in queryset.all():
            translation.populate_translation()
            translation.save()
