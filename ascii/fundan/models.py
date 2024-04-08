from django.db import models


class MenuLinkType(models.TextChoices):
    DOCUMENT = "d"
    FILE = "f"
    ERROR = "e"


class Menu(models.Model):
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"Menu {self.pk}"


class MenuLink(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(db_index=True)
    path = models.CharField(max_length=256)
    time = models.DateTimeField()
    type = models.CharField(max_length=1, choices=MenuLinkType.choices)
    content = models.CharField(max_length=256)

    def __str__(self):
        return f"MenuLink {self.pk}"


class Document(models.Model):
    path = models.CharField(max_length=256, unique=True)
    content = models.CharField(max_length=256)

    def __str__(self):
        return f"Document {self.pk}"
