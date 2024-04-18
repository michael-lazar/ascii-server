from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.fudan.models import Document, Menu
from ascii.translations.choices import TranslationLanguages


class FudanBBSMenuView(TemplateView):

    template_name = "fudan/bbs_menu.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Menu, path=f"/{kwargs['path']}")

        match self.request.GET.get("lang"):  # noqa
            case TranslationLanguages.ENGLISH:
                en, zh = True, False
            case _:
                en, zh = False, True

        return {
            "links": obj.links.all(),
            "parents": obj.parents.all().select_related("menu"),
            "obj": obj,
            "en": en,
            "zh": zh,
        }


class FudanBBSDocumentView(TemplateView):

    template_name = "fudan/bbs_document.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Document, path=f"/{kwargs['path']}")

        match self.request.GET.get("lang"):  # noqa
            case TranslationLanguages.ENGLISH:
                en, zh = True, False
            case _:
                en, zh = False, True

        return {
            "parents": obj.parents.all().select_related("menu"),
            "obj": obj,
            "en": en,
            "zh": zh,
        }
