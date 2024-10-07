from __future__ import annotations

import os
from datetime import date

from django.db import models
from django.db.models import Manager

from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.mozz.choices import ArtPostFileType, ArtPostFontName


class ArtPostQuerySet(models.QuerySet):

    def visible(self) -> ArtPostQuerySet:
        return self.filter(image_x1__isnull=False, visible=True)


ArtPostManager = Manager.from_queryset(ArtPostQuerySet)  # noqa


def upload_to(instance: ArtPost, filename: str) -> str:
    return f"mozz/{instance.date.year}/{instance.slug}/{filename}"


class ArtPost(BaseModel):
    slug = models.SlugField(db_index=True)
    date = models.DateField(default=date.today, db_index=True)
    visible = models.BooleanField(default=True)

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    file = models.FileField(upload_to=upload_to)
    file_type = models.CharField(max_length=16, choices=ArtPostFileType.choices)
    font_name = models.CharField(max_length=16, choices=ArtPostFontName.choices, blank=True)

    image_x1 = models.ImageField(
        upload_to=upload_to,
        verbose_name="Image (x1)",
        blank=True,
        null=True,
    )

    # TODO: Add thumbnail generation

    objects = ArtPostManager()

    class Meta:
        ordering = ["-date", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "date"],
                name="artpost_slug_date",
            )
        ]

    def __str__(self):
        return self.title

    @property
    def public_url(self) -> str:
        return reverse("mozz-art-post", args=[self.date, self.slug])

    @property
    def file_extension(self) -> str:
        _, ext = os.path.splitext(self.file.name)
        return ext.lower() if ext else ""

    @property
    def image_x1_extension(self) -> str:
        if not self.image_x1:
            return ""

        _, ext = os.path.splitext(self.image_x1.name)
        return ext.lower() if ext else ""
