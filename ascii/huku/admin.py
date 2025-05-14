import html
from typing import cast

from django.contrib import admin
from django.utils.html import format_html

from ascii.core.admin import linkify
from ascii.core.utils import reverse
from ascii.huku.models import MLTDirectory, MLTDirectoryQuerySet, MLTFile, MLTFileQuerySet, MLTItem


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
        "get_item_count",
    ]
    search_fields = ["id", "path"]
    list_filter = ["nsfw", "decoding_error"]
    readonly_fields = ["get_public_link", "get_item_count", "get_data"]

    def get_queryset(self, request):
        qs = cast(MLTFileQuerySet, super().get_queryset(request))
        qs = qs.select_related("parent")
        qs = qs.annotate_item_count()
        return qs

    @admin.display(description="Items", ordering="item_count")
    def get_item_count(self, obj: MLTFile) -> str:
        link_url = reverse("admin:huku_mltitem_changelist", qs={"mlt_file": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.item_count)

    @admin.display(description="Data")
    def get_data(self, obj: MLTFile) -> str:
        text = obj.data.decode("cp932", errors="backslashreplace")
        text = html.unescape(text)
        return format_html("<pre class='huku-raw'>{}</pre>", text)

    @admin.display(description="View")
    def get_public_link(self, obj: MLTFile) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)


@admin.register(MLTItem)
class MLTItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ["mlt_file"]
    list_display = ["id", linkify("mlt_file"), "order", "heading", "line_count"]
    search_fields = ["id", "heading", "text"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("mlt_file")
        return qs
