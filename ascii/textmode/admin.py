from typing import cast

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.html import format_html

from ascii.core.admin import linkify
from ascii.core.utils import reverse
from ascii.core.widgets import FormattedJSONWidget, ImagePreviewWidget
from ascii.textmode.models import (
    ArtFile,
    ArtistTag,
    ArtistTagQuerySet,
    ArtPack,
    ArtPackQuerySet,
    ContentTag,
    ContentTagQuerySet,
    GroupTag,
    GroupTagQuerySet,
)


@admin.register(ArtPack)
class ArtPackAdmin(admin.ModelAdmin):
    list_display = ["name", linkify("fileid"), "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count"]

    def get_queryset(self, request: HttpRequest) -> ArtPackQuerySet:
        qs = cast(ArtPackQuerySet, super().get_queryset(request))
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
    autocomplete_fields = ["pack", "content_tags", "artist_tags", "group_tags"]
    formfield_overrides = {
        models.JSONField: {"widget": FormattedJSONWidget},
        models.ImageField: {"widget": ImagePreviewWidget},
    }


@admin.register(ContentTag)
class ContentTagAdmin(admin.ModelAdmin):
    list_display = ["name", "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count"]

    def get_queryset(self, request: HttpRequest) -> ContentTagQuerySet:
        qs = cast(ContentTagQuerySet, super().get_queryset(request))
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ContentTag) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"content_tags": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)


@admin.register(ArtistTag)
class ArtistTagAdmin(admin.ModelAdmin):
    list_display = ["name", "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count"]

    def get_queryset(self, request: HttpRequest) -> ArtistTagQuerySet:
        qs = cast(ArtistTagQuerySet, super().get_queryset(request))
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: ArtistTag) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"artist_tags": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)


@admin.register(GroupTag)
class GroupTagAdmin(admin.ModelAdmin):
    list_display = ["name", "get_artfile_count"]
    search_fields = ["name"]
    readonly_fields = ["get_artfile_count"]

    def get_queryset(self, request: HttpRequest) -> GroupTagQuerySet:
        qs = cast(GroupTagQuerySet, super().get_queryset(request))
        qs = qs.annotate_artfile_count()
        return qs

    @admin.display(description="Files", ordering="artfile_count")
    def get_artfile_count(self, obj: GroupTag) -> str:
        link_url = reverse("admin:textmode_artfile_changelist", qs={"group_tags": obj.pk})
        return format_html('<a href="{}">{}</a>', link_url, obj.artfile_count)
