from __future__ import annotations

import os
from datetime import date

from django.db import models
from django.db.models import Manager, Q
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.mozz.choices import ArtPostFileType, ArtPostFontName


class ArtPostQuerySet(models.QuerySet):

    def visible(self) -> ArtPostQuerySet:
        return self.filter(image_x1__isnull=False, visible=True)


ArtPostManager = Manager.from_queryset(ArtPostQuerySet)  # noqa


def upload_to(instance: ArtPost, filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.lower() if ext else ""
    return f"mozz/{instance.date.year}/{instance.slug}{ext}"


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
    image_tn = ImageSpecField(
        source="image_x1",
        processors=[ResizeToFit(height=300)],
        format="PNG",
    )

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

    @property
    def download_raw_name(self) -> str:
        return f"{self.slug}{self.file_extension}"

    @property
    def download_image_name(self) -> str:
        return f"{self.slug}{self.image_x1_extension}"

    def get_prev(self) -> ArtPost | None:
        qs = ArtPost.objects.visible().filter(
            Q(date__gt=self.date) | Q(date=self.date, id__gt=self.id)
        )
        return qs.last()

    def get_next(self) -> ArtPost | None:
        qs = ArtPost.objects.visible().filter(
            Q(date__lt=self.date) | Q(date=self.date, id__lt=self.id)
        )
        return qs.first()
