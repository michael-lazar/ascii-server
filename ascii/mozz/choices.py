from django.db import models


class ArtPostFileType(models.TextChoices):
    TEXT = "text", "plaintext"
    XBIN = "xbin", "XBin"
    OTHER = "other", "other"


class ArtPostFontName(models.TextChoices):
    MENLO = "menlo", "Menlo"
    TOPAZ_2PLUS = "topaz_2plus", "Amiga Topaz 2+"
    JGS = "jgs", "Jgs"
    CUSTOM = "custom", "Custom"
