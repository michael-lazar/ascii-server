from django.db import models


class ArtPostFileType(models.TextChoices):
    TEXT = "text", "Text"
    XBIN = "xbin", "XBin"
    IMAGE = "image", "Image"


class ArtPostFontName(models.TextChoices):
    MENLO = "menlo", "Menlo"
    TOPAZ_2PLUS = "topaz_2plus", "Amiga Topaz 2+"
