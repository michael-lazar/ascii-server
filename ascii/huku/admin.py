import html
from typing import cast

from django.contrib import admin
from django.utils.html import format_html

from ascii.core.admin import linkify
from ascii.core.utils import reverse
from ascii.huku.models import (
    MLTArtwork,
    MLTDirectory,
    MLTDirectoryQuerySet,
    MLTFile,
    MLTFileQuerySet,
    MLTSection,
)


class MLTFileInline(admin.TabularInline):
    model = MLTFile
    fields = ["parent", "name"]
    can_delete = False
    extra = 0
    show_change_link = True


class MLTDirectoryInline(admin.TabularInline):
    model = MLTDirectory
    fields = ["parent", "name"]
    can_delete = False
    extra = 0
    show_change_link = True


@admin.register(MLTDirectory)
class MLTDirectoryAdmin(admin.ModelAdmin):
    list_display = ["id", "path", "get_file_count", "get_subdirectory_count"]
    search_fields = ["id", "path"]
    readonly_fields = ["get_file_count", "get_subdirectory_count", "get_public_link"]
    autocomplete_fields = ["parent"]
    inlines = [MLTDirectoryInline, MLTFileInline]

    def get_queryset(self, request):
        qs = cast(MLTDirectoryQuerySet, super().get_queryset(request))
        qs = qs.annotate_file_count()
        qs = qs.annotate_subdirectory_count()
        return qs

    @admin.display(description="Files", ordering="file_count")
    def get_file_count(self, obj: MLTDirectory) -> str:
        link_url = reverse("admin:huku_mltfile_changelist", qs={"parent": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.file_count)

    @admin.display(description="Subdirectories", ordering="subdirectory_count")
    def get_subdirectory_count(self, obj: MLTDirectory) -> str:
        link_url = reverse("admin:huku_mltdirectory_changelist", qs={"parent": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.subdirectory_count)

    @admin.display(description="View")
    def get_public_link(self, obj: MLTFile) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)


@admin.register(MLTFile)
class MLTFileAdmin(admin.ModelAdmin):
    autocomplete_fields = ["parent"]
    list_display = [
        "id",
        linkify("parent"),
        "path",
        "last_update",
        "nsfw",
        "decoding_error",
        "artwork_count",
    ]
    search_fields = ["id", "path"]
    list_filter = ["nsfw", "decoding_error"]
    readonly_fields = ["get_public_link", "get_data"]

    def get_queryset(self, request):
        qs = cast(MLTFileQuerySet, super().get_queryset(request))
        qs = qs.select_related("parent")
        return qs

    @admin.display(description="Data")
    def get_data(self, obj: MLTFile) -> str:
        text = obj.data.decode("cp932", errors="backslashreplace")
        text = html.unescape(text)
        return format_html("<pre class='huku-raw'>{}</pre>", text)

    @admin.display(description="View")
    def get_public_link(self, obj: MLTFile) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)


@admin.register(MLTSection)
class MLTSectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ["mlt_file"]
    list_display = ["name", "slug", linkify("mlt_file"), "order", "get_artwork_count"]
    search_fields = ["slug", "name"]
    readonly_fields = ["get_artwork_count"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("mlt_file")
        return qs

    @admin.display(description="Artwork", ordering="artwork_count")
    def get_artwork_count(self, obj: MLTFile) -> str:
        link_url = reverse("admin:huku_mltartwork_changelist", qs={"section": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artwork_count)


@admin.register(MLTArtwork)
class MLTArtworkAdmin(admin.ModelAdmin):
    autocomplete_fields = ["section"]
    list_display = ["slug", linkify("section"), "order", "line_count"]
    search_fields = ["slug", "text"]
    readonly_fields = ["get_public_link"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("section")
        return qs

    @admin.display(description="View")
    def get_public_link(self, obj: MLTArtwork) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)
