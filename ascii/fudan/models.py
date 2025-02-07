from __future__ import annotations

from django.db import models

from ascii.core.fields import NonStrippingCharField, NonStrippingTextField
from ascii.core.models import BaseModel
from ascii.core.utils import reverse
from ascii.fudan.ansi import ANSIParser
from ascii.fudan.choices import MenuLinkType
from ascii.translations.choices import TranslationLanguages
from ascii.translations.models import Translation


class Menu(BaseModel):
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"Menu: {self.pk}"

    @classmethod
    def build_source_url(cls, path: str) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/0an?path={path}"

    @property
    def source_url(self) -> str:
        return self.build_source_url(self.path)

    @property
    def public_url(self) -> str:
        return reverse("fudan-bbs-menu", args=[self.path[1:]])


class Document(BaseModel):
    path = models.CharField(max_length=256, unique=True)
    data = models.BinaryField()
    text = NonStrippingTextField()

    def __str__(self):
        return f"Document: {self.pk}"

    @classmethod
    def build_source_url(cls, path: str) -> str:
        return f"https://bbs.fudan.edu.cn/bbs/anc?path={path}"

    @property
    def source_url(self) -> str:
        return self.build_source_url(self.path)

    @property
    def public_url(self) -> str:
        return reverse("fudan-bbs-document", args=[self.path[1:]])

    def get_translation(self) -> Translation | None:
        parser = ANSIParser(self.text)
        original = parser.to_stripped_text()

        translation = Translation.objects.filter(
            original=original,
            language=TranslationLanguages.CHINESE_SIMPLIFIED,
        ).first()

        return translation

    def get_translated_text(self, start: int | None = None, end: int | None = None) -> str:
        parser = ANSIParser(self.text)
        original = parser.to_stripped_text()

        translation, created = Translation.objects.get_or_create(
            original=original,
            language=TranslationLanguages.CHINESE_SIMPLIFIED,
        )
        if created:
            translation.populate_translation()

        translated_text = translation.translated
        translated_text = parser.apply_line_indents(translated_text)

        # Slice after translating to avoid busting the cache.
        translated_text = "\n".join(translated_text.splitlines()[start:end])
        return translated_text

    def get_html(self, start: int | None = None, end: int | None = None) -> str:
        text = "\n".join(self.text.splitlines()[start:end])
        parser = ANSIParser(text)
        return parser.to_html()


class MenuLink(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="links")
    order = models.PositiveIntegerField(db_index=True)
    organizer = models.CharField(blank=True, max_length=64)
    path = models.CharField(max_length=256)
    time = models.DateTimeField()
    type = models.CharField(max_length=1, choices=MenuLinkType.choices)
    text = NonStrippingCharField(max_length=256, blank=True)

    target_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="parents",
    )
    target_menu = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL,
        blank=True,
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
    def target_public_url(self) -> str | None:
        match self.type:
            case MenuLinkType.DIRECTORY:
                return reverse("fudan-bbs-menu", args=[self.path[1:]])
            case MenuLinkType.FILE:
                return reverse("fudan-bbs-document", args=[self.path[1:]])
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

    def get_prev(self) -> MenuLink | None:
        qs = MenuLink.objects.filter(menu=self.menu, order__lt=self.order)
        return qs.order_by("-order").first()

    def get_next(self) -> MenuLink | None:
        qs = MenuLink.objects.filter(menu=self.menu, order__gt=self.order)
        return qs.order_by("order").first()

    def get_translation(self) -> Translation | None:
        parser = ANSIParser(self.text)
        original = parser.to_stripped_text()

        translation = Translation.objects.filter(
            original=original,
            language=TranslationLanguages.CHINESE_SIMPLIFIED,
        ).first()

        return translation

    def get_translated_text(self) -> str:
        parser = ANSIParser(self.text)
        original = parser.to_stripped_text()

        translation, created = Translation.objects.get_or_create(
            original=original,
            language=TranslationLanguages.CHINESE_SIMPLIFIED,
        )
        if created:
            translation.populate_translation()

        translated_text = translation.translated or "-"
        # translated_text = parser.apply_line_indents(translated_text)
        return translated_text


class ScratchFile(BaseModel):
    slug = models.SlugField(unique=True)
    text = NonStrippingTextField()

    def __str__(self):
        return f"Scratch: {self.pk}"

    def get_html(self) -> str:
        parser = ANSIParser(self.text)
        html = parser.to_html()
        return html

    @property
    def public_url(self) -> str:
        return reverse("fudan-scratch", args=[self.slug])


class AssetFile(BaseModel):
    slug = models.SlugField(unique=True)
    file = models.FileField()

    def __str__(self):
        return f"Asset: {self.pk}"

    @property
    def public_url(self) -> str:
        return reverse("fudan-asset", args=[self.slug])
