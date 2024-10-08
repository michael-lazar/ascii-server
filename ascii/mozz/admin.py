from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from imagekit.admin import AdminThumbnail

from ascii.core.admin import linkify
from ascii.core.widgets import ImagePreviewWidget
from ascii.mozz.models import ArtPost, ArtPostAttachment, ScrollFile


class ArtPostAttachmentAdminInline(admin.TabularInline):
    model = ArtPostAttachment
    fields = ["post", "name", "file"]
    autocomplete_fields = ["post"]
    extra = 0
    show_change_link = False


@admin.register(ScrollFile)
class ScrollFileAdmin(admin.ModelAdmin):
    list_display = ["slug", "get_public_link"]
    readonly_fields = ["get_public_link"]

    @admin.display(description="View")
    def get_public_link(self, obj: ScrollFile) -> str:
        if not obj.id:
            return "-"
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)


@admin.register(ArtPostAttachment)
class ArtPostAttachmentAdmin(admin.ModelAdmin):
    list_display = ["id", linkify("post"), "name", "file"]
    autocomplete_fields = ["post"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("post")
        return qs


@admin.register(ArtPost)
class ArtFileAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "date",
        "visible",
        "title",
        "file_type",
        "font_name",
        "get_public_link",
    ]
    search_fields = ["slug", "title"]
    list_editable = ["visible"]
    list_filter = ["visible"]
    readonly_fields = ["get_public_link", "image_tn"]
    formfield_overrides = {
        models.ImageField: {"widget": ImagePreviewWidget},
    }
    inlines = [ArtPostAttachmentAdminInline]

    image_tn = AdminThumbnail(image_field="image_tn")

    @admin.display(description="View")
    def get_public_link(self, obj: ArtPost) -> str:
        if not obj.id:
            return "-"
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)
