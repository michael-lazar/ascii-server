from django.contrib import admin
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import format_html
from stransi import Ansi

from ascii.core.admin import ReadOnlyModelAdmin, ReadOnlyTabularInline
from ascii.fudan.models import Document, Menu, MenuLink


class MenuLinkInline(ReadOnlyTabularInline):
    model = MenuLink
    readonly_fields = [
        "get_target",
    ]
    fields = [
        "menu",
        "get_target",
        "type",
        "order",
        "organizer",
        "time",
        "text",
    ]

    @admin.display(description="Target")
    def get_target(self, obj: MenuLink) -> str:
        if obj.target:
            return format_html("<a href='{}'>{}</a>", obj.target.change_url, obj.target)
        else:
            return "-"


class MenuLinkMenuInline(MenuLinkInline):
    fk_name = "menu"
    verbose_name = "link"


class MenuLinkTargetMenuInline(MenuLinkMenuInline):
    fk_name = "target_menu"
    verbose_name = "parent"


class MenuLinkTargetDocumentInline(MenuLinkMenuInline):
    fk_name = "target_document"
    verbose_name = "parent"


@admin.register(Menu)
class MenuAdmin(ReadOnlyModelAdmin):
    list_display = ["id", "path"]
    search_fields = ["id", "path"]
    inlines = [MenuLinkTargetMenuInline, MenuLinkMenuInline]
    readonly_fields = [
        "get_title",
        "get_source",
        "get_bbs_preview",
        "get_text",
    ]
    fields = [
        "path",
        "get_title",
        "get_source",
        "get_bbs_preview",
        "get_text",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("links", "parents")
        return qs

    @admin.display(description="Title")
    def get_title(self, obj: Menu) -> str:
        return obj.title

    @admin.display(description="Source")
    def get_source(self, obj: Menu) -> str:
        return format_html("<a href={}>{}</a>", obj.source_url, obj.source_url)

    @admin.display(description="Preview")
    def get_bbs_preview(self, obj: Menu) -> str:
        return render_to_string("admin/fragments/bbs_preview.html", {"url": obj.bbs_url})

    @admin.display(description="Text")
    def get_text(self, obj: Menu) -> str:
        return format_html("<pre class='bbs-raw'>{}</pre>", obj.get_text())


@admin.register(Document)
class DocumentAdmin(ReadOnlyModelAdmin):
    list_display = ["id", "path"]
    search_fields = ["id", "path", "text"]
    inlines = [MenuLinkTargetDocumentInline]
    readonly_fields = [
        "get_title",
        "get_source",
        "get_bbs_preview",
        "get_data",
        "get_instructions",
    ]
    fields = [
        "path",
        "get_title",
        "get_source",
        "get_bbs_preview",
        "get_data",
        "get_instructions",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("parents")
        return qs

    @admin.display(description="Title")
    def get_title(self, obj: Menu) -> str:
        return obj.title

    @admin.display(description="Source")
    def get_source(self, obj: Document) -> str:
        return format_html("<a href={}>{}</a>", obj.source_url, obj.source_url)

    @admin.display(description="Preview")
    def get_bbs_preview(self, obj: Document) -> str:
        return render_to_string("admin/fragments/bbs_preview.html", {"url": obj.bbs_url})

    @admin.display(description="Data")
    def get_data(self, obj: Document) -> str:
        lines: list[str] = []
        for n, line in enumerate(obj.escaped_text.splitlines(), start=1):
            lines.append(f"{n:<3} {repr(line)[1:-1]}")

        return format_html("<pre class='bbs-raw'>{}</pre>", "\n".join(lines))

    @admin.display(description="Instructions")
    def get_instructions(self, obj: Document) -> str:
        text = "".join(str(part) for part in Ansi(obj.escaped_text).instructions())

        lines: list[str] = []
        for n, line in enumerate(text.splitlines(), start=1):
            lines.append(f"{n:>4} {repr(line)[1:-1]}")

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
        "text",
    ]
    formfield_overrides = {
        models.CharField: {"strip": False},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("menu", "target_document", "target_menu")
        return qs
