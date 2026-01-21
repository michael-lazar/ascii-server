from __future__ import annotations

import os
from datetime import date

from django.core.files.storage import storages
from django.db import models
from django.db.models import Manager, Q
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from ascii.core.models import BaseModel
from ascii.core.sauce import get_sauce
from ascii.mozz.choices import ArtPostFileType, ArtPostFontName


class ArtPostQuerySet(models.QuerySet):
    def visible(self) -> ArtPostQuerySet:
        return self.filter(visible=True)


ArtPostManager = Manager.from_queryset(ArtPostQuerySet)  # noqa


def upload_to(instance: ArtPost, filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.lower() if ext else ""
    return f"mozz/{instance.date.year}/{instance.slug}/{instance.slug}{ext}"


class ArtPost(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(db_index=True)
    date = models.DateField(default=date.today, db_index=True)
    visible = models.BooleanField(default=True)
    favorite = models.BooleanField(default=False)

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    file = models.FileField(upload_to=upload_to, storage=storages["overwrite"])
    file_type = models.CharField(max_length=16, choices=ArtPostFileType.choices)
    font_name = models.CharField(max_length=16, choices=ArtPostFontName.choices, blank=True)

    image_x1 = models.ImageField(
        upload_to=upload_to,
        storage=storages["overwrite"],
        verbose_name="Image (x1)",
        blank=True,
        null=True,
    )
    image_tn = ImageSpecField(
        source="image_x1",
        processors=[ResizeToFit(height=300, width=400)],
        format="PNG",
        cachefile_storage=storages["overwrite"],
    )

    sauce_data = models.JSONField(blank=True, default=dict)

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
        return ext.lower() if ext else "unknown"

    @property
    def image_extension(self) -> str:
        if not self.image_x1:
            return ""

        _, ext = os.path.splitext(self.image_x1.name)
        return ext.lower() if ext else ""

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

    def refresh_sauce(self) -> None:
        """
        Read the file and extract SAUCE metadata, storing it in sauce_data.
        """
        if not self.file:
            self.sauce_data = {}
            return

        with self.file.open("rb") as f:
            file_bytes = f.read()

        self.sauce_data = get_sauce(file_bytes) or {}

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        self.refresh_sauce()
        if self.sauce_data:
            # Save again to update sauce_data without triggering another refresh
            super().save(update_fields=["sauce_data"])

        # Bust the imagekit thumbnail cache after saving, in case
        # a new image was uploaded with the same filename.
        if self.image_x1:
            self.image_tn.generate(force=True)  # noqa


def upload_attachment_to(instance: ArtPostAttachment, filename: str) -> str:
    return f"mozz/{instance.post.date.year}/{instance.post.slug}/attachments/{filename}"


class ArtPostAttachment(BaseModel):
    name = models.CharField(max_length=128)
    post = models.ForeignKey(
        ArtPost,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(upload_to=upload_attachment_to)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name

    @property
    def file_extension(self) -> str:
        _, ext = os.path.splitext(self.file.name)
        return ext.lower() if ext else "unknown"


class ScrollFile(BaseModel):
    slug = models.SlugField(unique=True)
    text = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.slug}.txt"

    @property
    def public_url(self) -> str:
        return reverse("mozz-scroll-file", args=[self.slug])
