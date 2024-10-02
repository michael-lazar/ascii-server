from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from ascii.core.widgets import ImagePreviewWidget
from ascii.mozz.models import ArtPost


@admin.register(ArtPost)
class ArtFileAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "date",
        "title",
        "file_type",
        "font_name",
        "get_public_link",
    ]
    list_filter = [
        "date",
        "file_type",
        "font_name",
    ]
    search_fields = ["slug", "title"]
    readonly_fields = ["get_public_link"]
    formfield_overrides = {
        models.ImageField: {"widget": ImagePreviewWidget},
    }

    @admin.display(description="View")
    def get_public_link(self, obj: ArtPost) -> str:
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)
