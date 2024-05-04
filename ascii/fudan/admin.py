from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from ascii.fudan.models import AssetFile, Document, Menu, MenuLink, ScratchFile


class MenuLinkInline(admin.TabularInline):
    fk_name = "menu"
    verbose_name = "link"
    model = MenuLink
    readonly_fields = ["get_target", "menu", "time"]
    fields = [
        "menu",
        "get_target",
        "type",
        "order",
        "organizer",
        "time",
        "text",
    ]
    can_delete = False
    extra = 0
    show_change_link = True

    @admin.display(description="Target")
    def get_target(self, obj: MenuLink) -> str:
        if obj.target:
            return format_html("<a href='{}'>{}</a>", obj.target.change_url, obj.target)
        else:
            return "-"


class MenuLinkTargetMenuInline(MenuLinkInline):
    fk_name = "target_menu"
    verbose_name = "parent"


class MenuLinkTargetDocumentInline(MenuLinkInline):
    fk_name = "target_document"
    verbose_name = "parent"


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "path", "get_public_link"]
    search_fields = ["id", "path"]
    inlines = [MenuLinkTargetMenuInline, MenuLinkInline]
    readonly_fields = [
        "get_source",
        "get_public_link",
    ]
    fields = [
        "path",
        "get_source",
        "get_public_link",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("links", "parents")
        return qs

    @admin.display(description="Source")
    def get_source(self, obj: Menu) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.source_url, obj.source_url)

    @admin.display(description="View")
    def get_public_link(self, obj: Menu) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "path", "get_public_link"]
    search_fields = ["id", "path", "text"]
    inlines = [MenuLinkTargetDocumentInline]
    readonly_fields = [
        "get_source",
        "get_public_link",
        "get_translation_link",
        "get_data",
    ]
    fields = [
        "path",
        "get_source",
        "get_public_link",
        "get_translation_link",
        "get_data",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("parents")
        return qs

    @admin.display(description="Source")
    def get_source(self, obj: Document) -> str:
        return format_html("<a href={}>{}</a>", obj.source_url, obj.source_url)

    @admin.display(description="View")
    def get_public_link(self, obj: Document) -> str:
        return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)

    @admin.display(description="Translation")
    def get_translation_link(self, obj: Document) -> str:
        if translation := obj.get_translation():
            return format_html(
                "<a href={} target='_blank'>{}</a>",
                translation.change_url,
                translation,
            )

        return "-"

    @admin.display(description="Data")
    def get_data(self, obj: Document) -> str:
        text = obj.data.decode("gb18030", errors="backslashreplace")

        lines: list[str] = []
        for n, line in enumerate(text.splitlines(), start=1):
            lines.append(f"{n:<3} {repr(line)[1:-1]}")

        return format_html("<pre class='bbs-raw'>{}</pre>", "\n".join(lines))


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "menu",
        "target_document",
        "target_menu",
    ]
    list_display = [
        "id",
        "path",
        "order",
        "organizer",
        "time",
        "type",
        "text",
    ]
    search_fields = ["id", "path", "text"]
    fields = [
        "menu",
        "path",
        "target_document",
        "target_menu",
        "order",
        "organizer",
        "time",
        "type",
        "get_translation_link",
        "text",
    ]
    formfield_overrides = {
        models.CharField: {"strip": False},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("menu", "target_document", "target_menu")
        return qs

    @admin.display(description="Translation")
    def get_translation_link(self, obj: MenuLink) -> str:
        if translation := obj.get_translation():
            return format_html(
                "<a href={} target='_blank'>{}</a>",
                translation.change_url,
                translation,
            )

        return "-"


@admin.register(ScratchFile)
class ScratchFileAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "get_public_link"]
    search_fields = ["id", "slug", "text"]
    readonly_fields = ["get_public_link"]
    fields = ["slug", "get_public_link", "text"]

    @admin.display(description="View")
    def get_public_link(self, obj: ScratchFile) -> str:
        if obj.pk:
            return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)

        return "-"


@admin.register(AssetFile)
class AssetFileAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "get_public_link"]
    search_fields = ["id", "slug"]
    readonly_fields = ["get_public_link"]
    fields = ["slug", "get_public_link", "file"]

    @admin.display(description="View")
    def get_public_link(self, obj: ScratchFile) -> str:
        if obj.pk:
            return format_html("<a href={} target='_blank'>{}</a>", obj.public_url, obj.public_url)

        return "-"
