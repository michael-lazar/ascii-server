from django.contrib import admin
from django.db import models
from django.http import HttpRequest

from ascii.translations.models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ["id", "language", "original", "translated"]
    actions = ["populate_translations"]

    @admin.display(description="Populate translations")
    def populate_translations(self, request: HttpRequest, queryset: models.QuerySet) -> None:
        for translation in queryset.all():
            translation.populate_translation()
