from __future__ import annotations

import os
from datetime import date

from django.core.files.base import ContentFile
from django.core.files.storage import storages
from django.db import models
from django.db.models import Manager, Q
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from ascii.core.models import BaseModel, DirtyFieldsMixin
from ascii.core.sauce import get_sauce_data, write_sauce_data
from ascii.mozz.choices import ArtPostFileType, ArtPostFontName
from ascii.textmode.models import ArtFile
from ascii.textmode.sauce import Sauce


class ArtPostQuerySet(models.QuerySet):
    def visible(self) -> ArtPostQuerySet:
        return self.filter(visible=True)


ArtPostManager = Manager.from_queryset(ArtPostQuerySet)  # noqa


def upload_to(instance: ArtPost, filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.lower() if ext else ""
    return f"mozz/{instance.date.year}/{instance.slug}/{instance.slug}{ext}"


class ArtPost(DirtyFieldsMixin, BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(unique=True)
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

    pack = models.ForeignKey(
        "textmode.ArtPack",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    artfile_name = models.CharField(max_length=130, blank=True)
    artfile = models.ForeignKey(
        "textmode.ArtFile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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

        with self.file.open("rb") as fp:
            file_bytes = fp.read()

        self.sauce_data = get_sauce_data(file_bytes) or {}

    def refresh_textmode_artfile(self) -> None:
        """
        Create a pseudo artfile object based on the art post.
        """
        if not self.pack:
            if self.artfile:
                self.artfile.delete()
                self.artfile = None
            return

        if not self.artfile:
            self.artfile = ArtFile(pack=self.pack, is_internal=True)

        filename = os.path.basename(self.file.name)
        _, file_extension = os.path.splitext(filename)

        self.artfile.name = self.artfile_name or filename
        self.artfile.file_extension = file_extension
        self.artfile.raw_file = self.file.name
        self.artfile.image_x1 = self.image_x1.name
        self.artfile.image_tn = self.image_tn.name  # noqa

        sauce = Sauce(self.sauce_data)
        for name, value in sauce.as_artfile_fields().items():
            setattr(self.artfile, name, value)

        self.artfile.save()

    def save(self, *args, **kwargs) -> None:
        # If sauce_data was edited, write it back to the file
        dirty_fields = self.get_dirty_fields()
        if "sauce_data" in dirty_fields and self.file:
            with self.file.open("rb") as fp:
                file_bytes = fp.read()

            updated_bytes = write_sauce_data(file_bytes, self.sauce_data)
            self.file.save(self.file.name, ContentFile(updated_bytes), save=False)

        super().save(*args, **kwargs)

        # Bust the imagekit thumbnail cache after saving, in case
        # a new image was uploaded with the same filename.
        if self.image_x1:
            self.image_tn.generate(force=True)  # noqa

        self.refresh_sauce()
        super().save(update_fields=["sauce_data"])  # noqa

        self.refresh_textmode_artfile()
        super().save(update_fields=["artfile"])  # noqa

        # Reset dirty fields tracking
        self._original_state = self._as_dict()


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
