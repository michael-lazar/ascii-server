from django.contrib import admin

from ascii.core.admin import linkify
from ascii.users.models import AuthToken


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ["key", linkify("user"), "created_at"]
    autocomplete_fields = ["user"]
