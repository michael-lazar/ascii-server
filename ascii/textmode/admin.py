from typing import cast

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.html import format_html

from ascii.core.admin import ReadOnlyTabularInline, linkify
from ascii.core.utils import reverse
from ascii.core.widgets import FormattedJSONWidget, ImagePreviewWidget
from ascii.textmode.models import (
    ArtFile,
    ArtFileQuerySet,
    ArtFileTag,
    ArtFileTagQuerySet,
    ArtPack,
    ArtPackQuerySet,
)


class ArtFileInline(ReadOnlyTabularInline):
    model = ArtFile
    readonly_fields = ["get_name"]
    fields = [
        "id",
        "pack",
        "get_name",
        "is_fileid",
        "author",
        "group",
        "date",
        "datatype",
        "filetype",
    ]
    extra = 0
    show_change_link = False
    can_add = False

    @admin.display(description="Name")
    def get_name(self, obj: ArtFile) -> str:
        return format_html("<a href='{}'>{}</a>", obj.change_url, obj.name)


@admin.register(ArtPack)
class ArtPackAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "get_artfile_count"]
    search_fields = ["name"]
    list_filter = ["year"]
    readonly_fields = ["get_artfile_count", "created_at", "get_public_link"]
    inlines = [ArtFileInline]

    def get_queryset(self, request: HttpRequest) -> ArtPackQuerySet:
        qs = cast(ArtPackQuerySet, super().get_queryset(request))
        qs = qs.prefetch_related("artfiles")
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ArtPack) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"pack": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)

    @admin.display(description="View")
    def get_public_link(self, obj: ArtPack) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)


@admin.register(ArtFile)
class ArtFileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "is_fileid",
        "name",
        linkify("pack"),
        "author",
        "group",
        "date",
        "datatype",
        "filetype",
    ]
    list_filter = [
        "pack",
        "is_fileid",
        "file_extension",
        "filetype",
        "datatype",
        "ice_colors",
        "letter_spacing",
    ]
    search_fields = ["name", "pack__name", "title", "author", "group"]
    autocomplete_fields = ["pack", "tags"]
    readonly_fields = ["created_at", "filesize", "file_extension", "get_public_link"]
    formfield_overrides = {
        models.JSONField: {"widget": FormattedJSONWidget},
        models.ImageField: {"widget": ImagePreviewWidget},
    }

    @admin.display(description="View")
    def get_public_link(self, obj: ArtFile) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)

    def get_queryset(self, request: HttpRequest) -> ArtFileQuerySet:
        qs = cast(ArtFileQuerySet, super().get_queryset(request))
        qs = qs.prefetch_related("pack")
        return qs


@admin.register(ArtFileTag)
class ArtFileTagAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count", "get_public_link"]
    list_filter = ["category"]

    def get_queryset(self, request: HttpRequest) -> ArtFileTagQuerySet:
        qs = cast(ArtFileTagQuerySet, super().get_queryset(request))
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ArtFileTag) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"tags": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)

    @admin.display(description="View")
    def get_public_link(self, obj: ArtFileTag) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)
