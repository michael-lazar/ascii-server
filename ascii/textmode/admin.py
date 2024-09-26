from typing import cast

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.html import format_html

from ascii.core.admin import ReadOnlyTabularInline, linkify
from ascii.core.utils import reverse
from ascii.core.widgets import FormattedJSONWidget, ImagePreviewWidget
from ascii.textmode.models import (
    ArtCollection,
    ArtCollectionMapping,
    ArtFile,
    ArtFileQuerySet,
    ArtFileTag,
    ArtPack,
    ArtPackQuerySet,
)


class ArtCollectionMappingInline(admin.TabularInline):
    model = ArtCollectionMapping
    fields = ["id", "collection", "artfile", "order", "get_image_preview"]
    readonly_fields = ["get_image_preview", "artfile"]
    autocomplete_fields = ["collection"]
    extra = 0
    show_change_link = False
    list_select_related = ["artfile"]
    formfield_overrides = {
        models.JSONField: {"widget": FormattedJSONWidget},
        models.ImageField: {"widget": ImagePreviewWidget},
    }

    @admin.display(description="Image Preview")
    def get_image_preview(self, obj: ArtCollectionMapping) -> str:
        if not obj.artfile.image_tn:
            return "-"

        return format_html(
            "<a href='{}'><img src='{}' style='object-fit: cover; "
            "max-height: 400px; max-width: 200px'></a>",
            obj.artfile.image_x1.url,
            obj.artfile.image_tn.url,
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
    list_display = ["name", "year", "get_artfile_count", "get_public_link"]
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
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)


@admin.register(ArtFile)
class ArtFileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "is_fileid",
        "name",
        linkify("pack"),
        "get_public_link",
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
    readonly_fields = [
        "created_at",
        "filesize",
        "file_extension",
        "get_public_link",
        "get_sixteencolors_link",
    ]
    formfield_overrides = {
        models.JSONField: {"widget": FormattedJSONWidget},
        models.ImageField: {"widget": ImagePreviewWidget},
    }

    @admin.display(description="View")
    def get_public_link(self, obj: ArtFile) -> str:
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)

    @admin.display(description="Source")
    def get_sixteencolors_link(self, obj: ArtFile) -> str:
        return format_html("<a href={} >{}</a>", obj.sixteencolors_url, obj.sixteencolors_url)

    def get_queryset(self, request: HttpRequest) -> ArtFileQuerySet:
        qs = cast(ArtFileQuerySet, super().get_queryset(request))
        qs = qs.prefetch_related("pack")
        return qs


@admin.register(ArtFileTag)
class ArtFileTagAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_featured", "get_artfile_count", "get_public_link"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count", "get_public_link"]
    list_filter = ["category", "is_featured"]
    list_editable = ["is_featured"]
    exclude = ["artfile_count"]

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ArtFileTag) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"tags": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)

    @admin.display(description="View")
    def get_public_link(self, obj: ArtFileTag) -> str:
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)


@admin.register(ArtCollection)
class ArtCollectionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "visible",
        "is_featured",
        "order",
        "get_artfile_count",
        "get_public_link",
    ]
    list_filter = ["visible", "is_featured"]
    list_editable = ["visible", "is_featured", "order"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count", "get_public_link"]
    inlines = [ArtCollectionMappingInline]

    def get_queryset(self, request: HttpRequest) -> ArtPackQuerySet:
        qs = cast(ArtPackQuerySet, super().get_queryset(request))
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ArtCollection) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"collections": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)

    @admin.display(description="View")
    def get_public_link(self, obj: ArtCollection) -> str:
        return format_html("<a href={} >{}</a>", obj.public_url, obj.public_url)
