from typing import cast

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.html import format_html

from ascii.core.admin import ReadOnlyTabularInline, linkify
from ascii.core.utils import reverse
from ascii.core.widgets import FormattedJSONWidget, ImagePreviewWidget
from ascii.textmode.models import ArtFile, ArtFileTag, ArtFileTagQuerySet, ArtPack, ArtPackQuerySet


class ArtFileInline(ReadOnlyTabularInline):
    model = ArtFile
    readonly_fields = ["get_name"]
    fields = [
        "id",
        "pack",
        "get_name",
        "is_fileid",
    ]
    extra = 0
    show_change_link = False
    can_add = False

    @admin.display(description="Name")
    def get_name(self, obj: ArtFile) -> str:
        return format_html("<a href='{}'>{}</a>", obj.change_url, obj.name)


@admin.register(ArtPack)
class ArtPackAdmin(admin.ModelAdmin):
    list_display = ["name", "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count"]
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


@admin.register(ArtFile)
class ArtFileAdmin(admin.ModelAdmin):
    list_display = ["id", "name", linkify("pack"), "is_fileid"]
    list_filter = ["pack"]
    search_fields = ["name", "pack__name"]
    autocomplete_fields = ["pack", "tags"]
    formfield_overrides = {
        models.JSONField: {"widget": FormattedJSONWidget},
        models.ImageField: {"widget": ImagePreviewWidget},
    }


@admin.register(ArtFileTag)
class ArtFileTagAdmin(admin.ModelAdmin):
    list_display = ["category", "name", "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count"]
    list_filter = ["category"]

    def get_queryset(self, request: HttpRequest) -> ArtFileTagQuerySet:
        qs = cast(ArtFileTagQuerySet, super().get_queryset(request))
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ArtFileTag) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"tags": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)
