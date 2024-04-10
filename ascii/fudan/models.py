from django.db import models

from ascii.core.utils import reverse
from ascii.fudan.choices import MenuLinkType


class Menu(models.Model):
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"Menu {self.pk}"

    def get_data(self) -> bytes:
        """
        Get the raw ANSI data for the menu screen.
        """
        return b"".join(link.data + b"\r\n" for link in self.links.all())

    @property
    def source_url(self) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/0an?path={self.path}"


class MenuLink(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="links")
    order = models.PositiveIntegerField(db_index=True)
    organizer = models.CharField(blank=True, max_length=64)
    path = models.CharField(max_length=256)
    time = models.DateTimeField()
    type = models.CharField(max_length=1, choices=MenuLinkType.choices)
    text = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"MenuLink {self.pk}"

    @property
    def data(self) -> bytes:
        return self.text.encode("gb18030")

    def get_source_url(self) -> str | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return f"https://bbs.fudan.edu.cn/bbs/0an?path={self.path}"
            case MenuLinkType.FILE:
                return f"https://bbs.fudan.edu.cn/bbs/anc?path={self.path}"
            case _:
                return None

    def get_admin_url(self) -> str | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return reverse("admin:fudan_menu_changelist", qs={"path": self.path})
            case MenuLinkType.FILE:
                return reverse("admin:fudan_document_changelist", qs={"path": self.path})
            case _:
                return None


class Document(models.Model):
    path = models.CharField(max_length=256, unique=True)
    data = models.BinaryField()
    html = models.TextField(verbose_name="HTML")

    def __str__(self):
        return f"Document {self.pk}"

    @property
    def source_url(self) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/anc?path={self.path}"
