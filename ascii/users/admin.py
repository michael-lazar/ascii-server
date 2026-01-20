from django.contrib import admin

from ascii.users.models import AuthToken


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ["key", "user", "created"]
    autocomplete_fields = ["user"]
