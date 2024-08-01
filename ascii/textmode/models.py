from __future__ import annotations

from django.db import models
from django.db.models import Count, Manager

from ascii.core.models import BaseModel


class ContentTagQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> ContentTagQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))


ContentTagManager = Manager.from_queryset(ContentTagQuerySet)  # noqa


class ContentTag(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    objects = ContentTagManager()

    # Annotated fields
    artfile_count: int

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ArtistTagQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> ArtistTagQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))


ArtistTagManager = Manager.from_queryset(ArtistTagQuerySet)  # noqa


class ArtistTag(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    objects = ArtistTagManager()

    # Annotated fields
    artfile_count: int

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GroupTagQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> GroupTagQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))


GroupTagManager = Manager.from_queryset(GroupTagQuerySet)  # noqa


class GroupTag(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    objects = GroupTagManager()

    # Annotated fields
    artfile_count: int

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ArtPackQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> ArtPackQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))


ArtPackManager = Manager.from_queryset(ArtPackQuerySet)  # noqa


class ArtPack(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    fileid = models.ForeignKey(
        "textmode.ArtFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="File ID",
    )

    objects = ArtPackManager()

    # Annotated fields
    artfile_count: int

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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

    raw = models.FileField(upload_to=upload_to_raw)

    image_tn = models.ImageField(verbose_name="Image (thumbnail)", upload_to=upload_to_tn)
    image_x1 = models.ImageField(verbose_name="Image (x1)", upload_to=upload_to_x1)
    image_x2 = models.ImageField(
        verbose_name="Image (x2)",
        upload_to=upload_to_x2,
        null=True,
        blank=True,
    )

    content_tags = models.ManyToManyField(ContentTag, blank=True, related_name="artfiles")
    artist_tags = models.ManyToManyField(ArtistTag, blank=True, related_name="artfiles")
    group_tags = models.ManyToManyField(GroupTag, blank=True, related_name="artfiles")

    sauce = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "pack"], name="unique_artfile_name_pack"),
        ]

    def __str__(self):
        return self.name
