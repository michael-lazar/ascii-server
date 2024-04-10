from django.contrib import admin
from django.utils.html import format_html

from ascii.core.utils import reverse
from ascii.fudan.models import Document, Menu, MenuLink


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 0
    fields = ["menu", "get_admin_url", "order", "organizer", "time", "type", "text"]
    readonly_fields = ["get_admin_url"]

    @admin.display(description="path")
    def get_admin_url(self, obj: MenuLink) -> str | None:
        url = obj.get_admin_url()
        if url:
            return format_html("<a href={}>{}</a>", url, obj.path)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "path"]
    search_fields = ["id", "path"]
    inlines = [MenuLinkInline]
    readonly_fields = ["get_data", "get_source_url"]
    fields = [
        "get_source_url",
        "path",
        "get_data",
    ]

    @admin.display(description="Data")
    def get_data(self, obj: Menu) -> str:
        return obj.get_data().decode("gb18030", errors="replace")

    @admin.display(description="Source")
    def get_source_url(self, obj: Menu) -> str:
        return format_html("<a href={}>{}</a>", obj.source_url, obj.source_url)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "path"]
    readonly_fields = ["get_data", "get_source_url", "get_preview_url"]
    fields = [
        "get_source_url",
        "get_preview_url",
        "path",
        "get_data",
        "html",
    ]

    @admin.display(description="Data")
    def get_data(self, obj: Document) -> str:
        return obj.data.decode("gb18030", errors="replace")

    @admin.display(description="Source")
    def get_source_url(self, obj: Document) -> str:
        return format_html("<a href={}>{}</a>", obj.source_url, obj.source_url)

    @admin.display(description="Preview")
    def get_preview_url(self, obj: Document) -> str:
        url = reverse("fudan-documents", args=[obj.path])
        return format_html("<iframe class='fudan-ansi' src={}></a>", url)


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ["path", "menu", "order", "organizer", "time", "type", "text"]
    list_filter = ["type"]
    autocomplete_fields = ["menu"]
    readonly_fields = ["get_source_url", "get_admin_url"]
    fields = [
        "menu",
        "get_source_url",
        "path",
        "get_admin_url",
        "order",
        "organizer",
        "time",
        "type",
        "text",
    ]

    @admin.display(description="Source")
    def get_source_url(self, obj: MenuLink) -> str | None:
        url = obj.get_source_url()
        if url:
            return format_html("<a href={}>{}</a>", url, url)

    @admin.display(description="Admin URL")
    def get_admin_url(self, obj: MenuLink) -> str | None:
        url = obj.get_admin_url()
        if url:
            return format_html("<a href={}>{}</a>", url, obj.path)
