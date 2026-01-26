from django.contrib import admin
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import format_html
from imagekit.admin import AdminThumbnail

from ascii.core.admin import linkify
from ascii.core.widgets import FormattedJSONWidget
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
    list_editable = ["name"]
    autocomplete_fields = ["post"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("post")
        return qs


@admin.register(ArtPost)
class ArtPostAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "image_tn",
        "date",
        "visible",
        "favorite",
        linkify("pack"),
        "artfile_name",
        "get_public_link",
    ]
    search_fields = ["slug", "title", "pack__name", "artfile_name"]
    list_editable = ["visible", "favorite"]
    list_filter = [
        "visible",
        "favorite",
        ("pack", admin.RelatedOnlyFieldListFilter),
    ]
    autocomplete_fields = ["pack"]
    readonly_fields = [
        "get_public_link",
        "image_tn",
        "get_sauce_data_html",
        "created_at",
        "updated_at",
        "artfile",
    ]
    fields = [
        "created_at",
        "updated_at",
        "visible",
        "favorite",
        "get_public_link",
        "slug",
        "title",
        "date",
        "file_type",
        "font_name",
        "file",
        "image_x1",
        "description",
        "image_tn",
        "get_sauce_data_html",
        "sauce_data",
        "pack",
        "artfile_name",
        "artfile",
    ]
    inlines = [ArtPostAttachmentAdminInline]
    formfield_overrides = {
        models.JSONField: {"widget": FormattedJSONWidget},
    }

    image_tn = AdminThumbnail(
        image_field="image_tn",
        template="core/fragments/admin_thumbnail.html",
    )

    @admin.display(description="View")
    def get_public_link(self, obj: ArtPost) -> str:
        if not obj.id:
            return "-"
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)

    @admin.display(description="SAUCE Data")
    def get_sauce_data_html(self, obj: ArtPost) -> str:
        if not obj.sauce_data:
            return "-"

        keys = ["Title", "Author", "Group", "Date", "Comments"]
        fields = [{"label": key, "value": obj.sauce_data.get(key)} for key in keys]

        return render_to_string("mozz/admin/sauce_data.html", {"fields": fields})
