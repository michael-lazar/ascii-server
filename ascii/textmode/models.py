from __future__ import annotations

import json

from django.db import models
from django.db.models import Count, Manager, Prefetch

from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.textmode.choices import TagCategory


class ArtFileTagQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> ArtFileTagQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))

    def visible(self) -> ArtFileTagQuerySet:
        return self.filter(artfiles__isnull=False)


ArtFileTagManager = Manager.from_queryset(ArtFileTagQuerySet)  # noqa


class ArtFileTag(BaseModel):
    category = models.CharField(choices=TagCategory.choices, db_index=True, max_length=20)
    name = models.CharField(max_length=100, db_index=True)

    objects = ArtFileTagManager()

    # Annotated fields
    artfile_count: int

    class Meta:
        ordering = ["category", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_artfiletag_category_name"
            ),
        ]

    def __str__(self):
        return f"{self.category}: {self.name}"


class ArtPackQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> ArtPackQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))

    def prefetch_fileid(self) -> ArtPackQuerySet:
        return self.prefetch_related(
            Prefetch(
                "artfiles",
                queryset=ArtFile.objects.filter(is_fileid=True),
                to_attr="fileid",
            )
        )


ArtPackManager = Manager.from_queryset(ArtPackQuerySet)  # noqa


class ArtPack(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    objects = ArtPackManager()

    # Annotated fields
    artfile_count: int
    fileid: list[ArtFile]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ArtFileQuerySet(models.QuerySet):
    pass


ArtFileManager = Manager.from_queryset(ArtFileQuerySet)  # noqa


def upload_to_raw(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.name}/raw/{filename}"


def upload_to_tn(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.name}/tn/{filename}"


def upload_to_x1(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.name}/x1/{filename}"


def upload_to_x2(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.name}/x2/{filename}"


class ArtFile(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    pack = models.ForeignKey(ArtPack, on_delete=models.CASCADE, related_name="artfiles")

    is_fileid = models.BooleanField(default=False)

    raw = models.FileField(upload_to=upload_to_raw)

    image_tn = models.ImageField(verbose_name="Image (thumbnail)", upload_to=upload_to_tn)
    image_x1 = models.ImageField(verbose_name="Image (x1)", upload_to=upload_to_x1)
    image_x2 = models.ImageField(
        verbose_name="Image (x2)",
        upload_to=upload_to_x2,
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(ArtFileTag, blank=True, related_name="artfiles")

    sauce = models.JSONField(blank=True, default=dict)

    objects = ArtFileManager()

    class Meta:
        ordering = ["-is_fileid", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "pack"], name="unique_artfile_name_pack"),
        ]

    def __str__(self):
        return self.name

    @property
    def sauce_str(self) -> str:
        return json.dumps(self.sauce, indent=2)

    @property
    def public_url(self) -> str:
        return reverse("textmode-artfile", args=[self.pack.name, self.name])

    @property
    def grid_width(self) -> int:
        if self.is_fileid:
            return 356

        return 160

    @property
    def grid_height(self) -> int:
        return int(self.grid_width * (self.image_tn.height / self.image_tn.width))
