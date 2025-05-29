from __future__ import annotations

from django.db import models
from django.db.models import Count, Manager

from ascii.core.fields import NonStrippingTextField
from ascii.core.models import BaseModel
from ascii.core.utils import gen_random_slug, reverse


class MLTDirectoryQuerySet(models.QuerySet):

    def annotate_file_count(self) -> MLTDirectoryQuerySet:
        return self.annotate(file_count=Count("files"))

    def annotate_subdirectory_count(self) -> MLTDirectoryQuerySet:
        return self.annotate(subdirectory_count=Count("subdirectories"))


MLTDirectoryManager = Manager.from_queryset(MLTDirectoryQuerySet)  # noqa


class MLTDirectory(BaseModel):
    slug = models.SlugField(unique=True, default=gen_random_slug)
    path = models.CharField(max_length=512, unique=True)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        "MLTDirectory",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="subdirectories",
    )

    objects = MLTDirectoryManager()

    # Annotated fields
    file_count: int
    subdirectory_count: int

    def __str__(self):
        return self.name or "/"

    class Meta:
        verbose_name = "MLT Directory"
        verbose_name_plural = "MLT Directories"

    @property
    def public_url(self) -> str:
        if self.path == "/":
            return reverse("huku-mlt-directory-index")
        else:
            return reverse("huku-mlt-directory", args=[self.path[1:-1]])

    @property
    def display_name(self) -> str:
        return self.name or "mlt"


class MLTFileQuerySet(models.QuerySet):

    def annotate_item_count(self) -> MLTFileQuerySet:
        return self.annotate(item_count=Count("items"))


class MLTFileManager(Manager.from_queryset(MLTFileQuerySet)):  # noqa
    def get_queryset(self):
        # This is a large field that won't be used most of the time,
        # so defer it as an optimization.
        return super().get_queryset().defer("data")


class MLTFile(BaseModel):
    slug = models.SlugField(unique=True, default=gen_random_slug)
    parent = models.ForeignKey(
        MLTDirectory,
        on_delete=models.CASCADE,
        related_name="files",
    )
    path = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    last_update = models.DateField(blank=True, null=True)
    nsfw = models.BooleanField(default=False, verbose_name="NSFW")
    data = models.BinaryField()
    decoding_error = models.BooleanField(default=False)
    artwork_count = models.IntegerField(default=0)

    objects = MLTFileManager()

    # Annotated fields
    item_count: int

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "MLT File"

    @property
    def public_url(self) -> str:
        return reverse("huku-mlt-file", args=[self.path[1:]])

    @property
    def download_url(self) -> str:
        return reverse("huku-mlt-file-download", args=[f"{self.path[1:]}.mlt"])


class MLTItemType(models.TextChoices):
    HEADING = "heading"
    ARTWORK = "artwork"


def upload_to(instance: MLTItem, filename: str) -> str:
    return f"huku/{instance.mlt_file.path}-{instance.order}.svg"


class MLTItem(BaseModel):
    slug = models.SlugField(unique=True, default=gen_random_slug)
    mlt_file = models.ForeignKey(
        MLTFile,
        on_delete=models.CASCADE,
        related_name="items",
    )
    item_type = models.CharField(max_length=8, choices=MLTItemType.choices, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    heading = models.CharField(max_length=256, blank=True)
    text = NonStrippingTextField(blank=True)
    line_count = models.IntegerField()
    image = models.FileField(blank=True, null=True, upload_to=upload_to)

    def __str__(self):
        return f"MLTItem: {self.pk}"

    class Meta:
        verbose_name = "MLT Item"
        ordering = ["mlt_file", "order"]

    @property
    def is_heading(self) -> bool:
        return self.item_type == MLTItemType.HEADING

    @property
    def is_artwork(self) -> bool:
        return self.item_type == MLTItemType.ARTWORK

    @property
    def public_url(self) -> str | None:
        if self.is_heading:
            return None

        return reverse("huku-mlt-item", args=[self.slug])
