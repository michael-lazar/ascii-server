from __future__ import annotations

import itertools
import mimetypes
import os

from django.db import models
from django.db.models import Count, Exists, Manager, OuterRef, Prefetch, Q
from django.utils import timezone

from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.textmode.choices import AspectRatio, DataType, FileType, LetterSpacing, TagCategory

# https://stackoverflow.com/a/67857443
ALT_SLASH = "%2F"

# Supported by the <sound> web player
AUDIO_MIMETYPES = [
    "audio/mpeg",  # .mp3
    "audio/ogg",  # .ogg
    "audio/wav",  # .wav
    "audio/aac",  # .aac
    "audio/webm",  # .weba
]

# Supported by the <video> web player
VIDEO_MIMETYPES = [
    "video/mp4",  # .mp4
    "video/webm",  # .webm
    "video/ogg",  # .ogv
]


class ArtFileTagQuerySet(models.QuerySet):

    def annotate_artfile_count(self) -> ArtFileTagQuerySet:
        return self.annotate(artfile_count=Count("artfiles"))

    def visible(self) -> ArtFileTagQuerySet:
        return self.filter(artfiles__isnull=False)

    def for_tag_list(self, category: TagCategory) -> ArtFileTagQuerySet:
        return self.visible().filter(category=category).annotate_artfile_count().order_by("name")

    def artists(self) -> ArtFileTagQuerySet:
        return self.filter(category=TagCategory.ARTIST)

    def groups(self) -> ArtFileTagQuerySet:
        return self.filter(category=TagCategory.GROUP)

    def content(self) -> ArtFileTagQuerySet:
        return self.filter(category=TagCategory.CONTENT)


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

    @property
    def public_url(self) -> str:
        name = self.name.replace("/", ALT_SLASH)
        return reverse("textmode-tag", args=[self.category, name])


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

    def group_by_year(self):
        return itertools.groupby(self, key=lambda obj: obj.year)


ArtPackManager = Manager.from_queryset(ArtPackQuerySet)  # noqa


def upload_to_zip(instance: ArtPack, filename: str) -> str:
    return f"pack/{instance.year}/{filename}"


class ArtPack(BaseModel):
    created_at = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()
    zip_file = models.FileField(upload_to=upload_to_zip)

    objects = ArtPackManager()

    # Annotated fields
    artfile_count: int
    fileid: list[ArtFile]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def public_url(self) -> str:
        return reverse("textmode-pack", args=[self.year, self.name])


class ArtFileQuerySet(models.QuerySet):

    def not_tagged(self, category: TagCategory) -> ArtFileQuerySet:
        """
        Return files that do not contain a tag within the given category.
        """
        tags_in_category = ArtFileTag.objects.filter(category=category, artfiles=OuterRef("pk"))
        return self.exclude(Exists(tags_in_category))

    def count_file_extensions(self) -> list[tuple[str, int]]:
        qs = (
            self.values("file_extension")
            .exclude(file_extension="")
            .annotate(count=Count("id", distinct=True))
            .order_by("-count")
            .values_list("file_extension", "count")
        )
        return list(qs)

    def annotate_artist_count(self):
        """
        Count the number of artist tags associated with the file.
        """
        return self.annotate(
            artist_count=Count("tags", filter=Q(tags__category=TagCategory.ARTIST))
        )

    def font_names(self) -> list[str]:
        return (
            self.order_by("font_name")
            .values_list("font_name", flat=True)
            .exclude(font_name="")
            .distinct()
        )

    def file_extensions(self) -> list[str]:
        return (
            self.order_by("file_extension")
            .values_list("file_extension", flat=True)
            .exclude(file_extension="")
            .distinct()
        )

    def years(self) -> list[int]:
        return self.order_by("pack__year").values_list("pack__year", flat=True).distinct()

    def search(self, text: str) -> ArtFileQuerySet:
        if not text:
            return self

        return self.filter(name__icontains=text)


ArtFileManager = Manager.from_queryset(ArtFileQuerySet)  # noqa


def upload_to_raw(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.year}/{instance.pack.name}/raw/{filename}"


def upload_to_tn(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.year}/{instance.pack.name}/tn/{filename}"


def upload_to_x1(instance: ArtFile, filename: str) -> str:
    return f"pack/{instance.pack.year}/{instance.pack.name}/x1/{filename}"


class ArtFile(BaseModel):
    created_at = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=130, db_index=True)
    pack = models.ForeignKey(ArtPack, on_delete=models.CASCADE, related_name="artfiles")

    is_fileid = models.BooleanField(default=False, db_index=True)

    raw_file = models.FileField(upload_to=upload_to_raw, max_length=130)
    file_extension = models.CharField(max_length=20, blank=True, db_index=True)
    filesize = models.PositiveIntegerField(default=0, db_index=True)

    image_tn = models.ImageField(
        verbose_name="Image (thumbnail)",
        upload_to=upload_to_tn,
        null=True,
        blank=True,
        max_length=130,
    )
    image_x1 = models.ImageField(
        verbose_name="Image (x1)",
        upload_to=upload_to_x1,
        null=True,
        blank=True,
        max_length=130,
    )

    tags = models.ManyToManyField(ArtFileTag, blank=True, related_name="artfiles")
    sauce_data = models.JSONField(blank=True, default=dict)

    title = models.CharField(max_length=35, blank=True, db_index=True)
    author = models.CharField(max_length=20, blank=True, db_index=True)
    group = models.CharField(max_length=20, blank=True, db_index=True)
    date = models.DateField(blank=True, null=True, db_index=True)
    comments = models.TextField(blank=True, db_index=True)
    datatype = models.IntegerField(
        choices=DataType.choices,
        blank=True,
        null=True,
        db_index=True,
    )
    filetype = models.IntegerField(
        choices=FileType.choices,
        blank=True,
        null=True,
        db_index=True,
    )
    pixel_width = models.IntegerField(blank=True, null=True, db_index=True)
    pixel_height = models.IntegerField(blank=True, null=True, db_index=True)
    character_width = models.IntegerField(blank=True, null=True, db_index=True)
    number_of_lines = models.IntegerField(blank=True, null=True, db_index=True)
    ice_colors = models.BooleanField(blank=True, null=True, db_index=True)
    letter_spacing = models.IntegerField(
        choices=LetterSpacing.choices,
        blank=True,
        null=True,
        db_index=True,
    )
    aspect_ratio = models.IntegerField(
        choices=AspectRatio.choices,
        blank=True,
        null=True,
        db_index=True,
    )
    font_name = models.CharField(max_length=50, blank=True, db_index=True)

    objects = ArtFileManager()

    # Annotated fields
    artist_count: int

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["name", "pack"], name="unique_artfile_name_pack"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.file_extension = os.path.splitext(self.name)[1].lower()

        if self.raw_file:
            self.file_size = self.raw_file.size
        else:
            self.file_size = 0

        super().save(*args, **kwargs)

    @property
    def public_url(self) -> str:
        return reverse("textmode-artfile", args=[self.pack.year, self.pack.name, self.name])

    @property
    def thumb_width(self) -> int:
        return 160

    @property
    def thumb_height(self) -> int:
        return min(int(self.thumb_width * (self.image_tn.height / self.image_tn.width)), 800)

    @property
    def thumb_width_2x(self) -> int:
        # 2*160px + 2*5px padding + 20px gap
        return 2 * self.thumb_width + 30

    @property
    def thumb_height_2x(self) -> int:
        return min(int(self.thumb_width_2x * (self.image_tn.height / self.image_tn.width)), 800)

    def get_next(self) -> ArtFile | None:
        qs = self.pack.artfiles.filter(name__gt=self.name)
        return qs.order_by("name").first()

    def get_prev(self) -> ArtFile | None:
        qs = self.pack.artfiles.filter(name__lt=self.name)
        return qs.order_by("-name").first()

    def get_artist_tags(self) -> ArtFileTagQuerySet:
        return ArtFileTag.objects.filter(category=TagCategory.ARTIST, artfiles=self)

    def get_group_tags(self) -> ArtFileTagQuerySet:
        return ArtFileTag.objects.filter(category=TagCategory.GROUP, artfiles=self)

    def get_content_tags(self) -> ArtFileTagQuerySet:
        return ArtFileTag.objects.filter(category=TagCategory.CONTENT, artfiles=self)

    def get_sauce_display(self) -> dict[str, str]:
        data = {}
        if self.title:
            data["Title"] = self.title
        if self.author:
            data["Author"] = self.author
        if self.group:
            data["Group"] = self.group
        if self.date:
            data["Date"] = self.date.strftime("%Y-%m-%d")
        if self.comments:
            data["Comments"] = self.comments
        if self.pixel_width and self.pixel_height:
            data["Size"] = f"{self.pixel_width}x{self.pixel_height} px"
        if self.number_of_lines and self.character_width:
            data["Size"] = f"{self.character_width}x{self.number_of_lines}"
        if self.datatype is not None:
            data["Type"] = f"{self.get_datatype_display()} / {self.get_filetype_display()}"
        if self.ice_colors is not None:
            data["ICE Color"] = "on" if self.ice_colors else "off"
        if self.letter_spacing is not None:
            data["Letter Spacing"] = self.get_letter_spacing_display()
        if self.aspect_ratio is not None:
            data["Aspect Ratio"] = self.get_aspect_ratio_display()
        if self.font_name:
            data["Font Name"] = self.font_name

        return data

    @property
    def mimetype(self) -> str | None:
        return mimetypes.guess_type(self.name, strict=False)[0]

    def is_audio(self) -> bool:
        return self.mimetype in AUDIO_MIMETYPES

    def is_video(self) -> bool:
        return self.mimetype in VIDEO_MIMETYPES
