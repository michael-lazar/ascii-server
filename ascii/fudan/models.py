from __future__ import annotations

from django.db import models
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.fudan.ansi import ANSIParser
from ascii.fudan.choices import MenuLinkType
from ascii.fudan.utils import get_ansi_length


def get_navbar_html(obj: Menu | Document) -> str:
    def gen():
        for link in obj.parents.all().select_related("menu"):
            yield link.menu.bbs_url, link.menu.path

    return format_html_join("", "<a href='{}'>↑ {}/</a>\n", gen())


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

    @property
    def title(self) -> str:
        if link := self.parents.first():
            return link.text
        return ""

    def get_text(self) -> str:
        return "\n".join(link.text for link in self.links.all())

    def get_html(self) -> str:
        """
        Compose the menu page by stringing together the individual links.
        """

        def gen():
            for link in self.links.all():

                yield (
                    link.order,
                    link.bbs_tag,
                    link.target_bbs_url,
                    link.text,
                    " " * (45 - get_ansi_length(link.text)),  # padding
                    link.organizer,
                    link.time.strftime("%Y-%m-%d"),
                )

        header = mark_safe(f"ORD TYPE {'DESCRIPTION':46}{'ORGANIZER':16}{'DATE':10}\n")

        line_template = "{:>3}. [{}] <a href='{}'>{}</a> {}{:16}{:10}"
        body = format_html_join("\n", line_template, gen())
        return header + body


class Document(BaseModel):
    path = models.CharField(max_length=256, unique=True)
    data = models.BinaryField()
    text = models.TextField()

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
    def title(self) -> str:
        if link := self.parents.first():
            return link.text
        return ""

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

    @property
    def bbs_tag(self) -> str:
        match self.type:
            case MenuLinkType.FILE:
                return "F"
            case MenuLinkType.DIRECTORY:
                return "D"
            case MenuLinkType.ERROR:
                return "E"
            case _:
                return " "
