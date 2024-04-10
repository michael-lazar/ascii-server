from django.db import models


class MenuLinkType(models.TextChoices):
    DIRECTORY = "d", "Directory"
    FILE = "f", "File"
    ERROR = "e", "Error"
