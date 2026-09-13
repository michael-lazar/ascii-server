from django.db import models


class ArtPostFileType(models.TextChoices):
    TEXT = "text", ".txt"
    ANS = "ans", ".ans"
    ASC = "asc", ".asc"
    XBIN = "xbin", ".xbin"
    OTHER = "other", "other"


# How the file types are grouped in the public gallery vocabulary
PLAINTEXT_FILETYPES = [ArtPostFileType.TEXT]
TEXTMODE_FILETYPES = [ArtPostFileType.ANS, ArtPostFileType.ASC, ArtPostFileType.XBIN]


class ArtPostFontName(models.TextChoices):
    MENLO = "menlo", "Menlo"
    TOPAZ_2PLUS = "topaz_2plus", "Amiga Topaz 2+"
    JGS = "jgs", "Jgs"
    CP437 = "cp437", "IBM CP437"
    CUSTOM = "custom", "Custom"
