import secrets

from django.conf import settings
from django.db import models

from ascii.core.models import BaseModel


def generate_key():
    return secrets.token_hex(20)


class AuthToken(BaseModel):
    key = models.CharField(max_length=40, primary_key=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="auth_token",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key()
        return super().save(*args, **kwargs)
