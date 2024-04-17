from __future__ import annotations

from django.db import models


class TranslationLanguages(models.TextChoices):
    CHINESE_SIMPLIFIED = "zh-cn", "zh-cn"
    ENGLISH = "en", "en"
