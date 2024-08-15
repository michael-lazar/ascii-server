from django.db import models


class TagCategory(models.TextChoices):
    ARTIST = "artist", "Artist"
    CONTENT = "content", "Content"
    GROUP = "group", "Group"
