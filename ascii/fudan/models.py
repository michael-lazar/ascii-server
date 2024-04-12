from __future__ import annotations

from django.db import models
from django.utils.html import format_html_join

from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.fudan.ansi import ANSIParser
from ascii.fudan.choices import MenuLinkType


class Menu(BaseModel):
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"Menu: {self.pk}"

    @classmethod
    def build_source_url(cls, path: str) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/0an?path={path}"

    @classmethod
    def build_bbs_url(cls, path: str) -> str:
        return reverse("fudan-bbs", args=[f"{path[1:]}/"])

    @property
    def source_url(self) -> str:
        return self.build_source_url(self.path)

    @property
    def bbs_url(self) -> str:
        return self.build_bbs_url(self.path)

    def get_text(self) -> str:
        return "\n".join(link.text for link in self.links.all())

    def get_html(self) -> str:
        def gen():
            for link in self.links.all():
                yield (
                    link.order,
                    link.target_bbs_url,
                    link.text,
                    link.organizer,
                    link.time.strftime("%Y-%m-%d"),
                )

        # TODO: Add link to parent at the top - make this a separate function
        # TODO: Align to 80 characters, only wrap link around text & not spaces
        template = "{:4}  <a href='{}'>{:40}</a> {:20}{}"
        return format_html_join("\n", template, gen())


class Document(BaseModel):
    path = models.CharField(max_length=256, unique=True)
    data = models.BinaryField()

    def __str__(self):
        return f"Document: {self.pk}"

    @classmethod
    def build_source_url(cls, path: str) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/anc?path={path}"

    @classmethod
    def build_bbs_url(cls, path: str) -> str:
        return reverse("fudan-bbs", args=[f"{path[1:]}"])

    @property
    def source_url(self) -> str:
        return self.build_source_url(self.path)

    @property
    def bbs_url(self) -> str:
        return self.build_bbs_url(self.path)

    @property
    def text(self) -> str:
        return self.data.decode("gb18030", errors="replace")

    @property
    def escaped_text(self):
        return self.data.decode("gb18030", errors="backslashreplace")

    def get_html(self) -> str:
        parser = ANSIParser()
        return parser.to_html(self.text)


class MenuLink(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="links")
    order = models.PositiveIntegerField(db_index=True)
    organizer = models.CharField(blank=True, max_length=64)
    path = models.CharField(max_length=256)
    time = models.DateTimeField()
    type = models.CharField(max_length=1, choices=MenuLinkType.choices)
    text = models.CharField(max_length=256, blank=True)

    target_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name="parents",
    )
    target_menu = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL,
        null=True,
        related_name="parents",
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"MenuLink: {self.pk}"

    @property
    def data(self) -> bytes:
        return self.text.encode("gb18030")

    @property
    def target(self) -> Menu | Document | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return self.target_menu
            case MenuLinkType.FILE:
                return self.target_document
            case _:
                return None

    @property
    def target_source_url(self) -> str | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return Menu.build_source_url(self.path)
            case MenuLinkType.FILE:
                return Document.build_source_url(self.path)
            case _:
                return None

    @property
    def target_bbs_url(self) -> str | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return Menu.build_bbs_url(self.path)
            case MenuLinkType.FILE:
                return Document.build_bbs_url(self.path)
            case _:
                return None
