from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms.utils import pretty_name
from django.utils.html import format_html

from ascii.core.utils import reverse


# https://stackoverflow.com/a/53092940
def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    @admin.display(description=pretty_name(field_name), ordering=field_name)
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return "-"
        c = ContentType.objects.get_for_model(linked_obj)
        view_name = f"admin:{c.app_label}_{c.model}_change"
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    return _linkify


class ReadOnlyModelAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyTabularInline(admin.TabularInline):

    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
