from __future__ import annotations

from django.db import models

from ascii.core.models import BaseModel
from ascii.fudan.ansi import ANSIParser
from ascii.fudan.choices import MenuLinkType


class Menu(BaseModel):
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"Menu {self.pk}"

    def get_text(self) -> str:
        return "".join(f"{link.text}\r\n" for link in self.links.all())

    def get_html(self) -> str:
        parser = ANSIParser()
        return parser.to_html(self.get_text())

    @property
    def source_url(self) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/0an?path={self.path}"


class MenuLinkQuerySet(models.QuerySet):

    def linked_to_document(self, document: Document) -> MenuLinkQuerySet:
        qs = self.filter(path=document.path, type=MenuLinkType.FILE)
        qs = qs.select_related("menu")
        return qs

    def linked_to_menu(self, menu: Menu) -> MenuLinkQuerySet:
        qs = self.filter(path=menu.path, type=MenuLinkType.DIRECTORY)
        qs = qs.select_related("menu")
        return qs


MenuLinkManager = models.Manager.from_queryset(MenuLinkQuerySet)  # noqa


class MenuLink(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="links")
    order = models.PositiveIntegerField(db_index=True)
    organizer = models.CharField(blank=True, max_length=64)
    path = models.CharField(max_length=256, db_index=True)
    time = models.DateTimeField()
    type = models.CharField(max_length=1, choices=MenuLinkType.choices, db_index=True)
    text = models.CharField(max_length=256, blank=True)

    objects = MenuLinkManager()

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"MenuLink {self.pk}"

    @property
    def data(self) -> bytes:
        return self.text.encode("gb18030")

    def get_html(self) -> str:
        parser = ANSIParser()
        return parser.to_html(self.text)

    def get_source_url(self) -> str | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return f"https://bbs.fudan.edu.cn/bbs/0an?path={self.path}"
            case MenuLinkType.FILE:
                return f"https://bbs.fudan.edu.cn/bbs/anc?path={self.path}"
            case _:
                return None

    def get_link_change_url(self) -> str | None:
        """
        Return the admin page for the linked menu/document, if it exists.
        """
        if self.type == MenuLinkType.DIRECTORY:
            if menu := Menu.objects.filter(path=self.path).first():
                return menu.change_url

        if self.type == MenuLinkType.FILE:
            if directory := Document.objects.filter(path=self.path).first():
                return directory.change_url

        return None


class Document(BaseModel):
    path = models.CharField(max_length=256, unique=True)
    data = models.BinaryField()
    html = models.TextField(verbose_name="HTML")

    def __str__(self):
        return f"Document {self.pk}"

    @property
    def source_url(self) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/anc?path={self.path}"

    @property
    def text(self) -> str:
        return self.data.decode("gb18030", errors="replace")

    def get_html(self) -> str:
        parser = ANSIParser()
        return parser.to_html(self.text)
