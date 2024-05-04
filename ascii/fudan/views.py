from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from ascii.core.utils import get_query_param
from ascii.fudan.models import AssetFile, Document, Menu, ScratchFile
from ascii.translations.choices import TranslationLanguages


class FudanScratchFileView(TemplateView):

    template_name = "fudan/scratch_file.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(ScratchFile, slug=kwargs["slug"])
        return {"obj": obj}


class FudanAssetFileView(View):

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        obj = get_object_or_404(AssetFile, slug=slug)
        return redirect(obj.file.url)


class FudanBBSMenuView(TemplateView):

    template_name = "fudan/bbs_menu.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Menu, path=f"/{kwargs['path']}")

        match self.request.GET.get("lang"):  # noqa
            case TranslationLanguages.ENGLISH:
                en, zh = True, False
            case _:
                en, zh = False, True

        links = obj.links.all()
        parents = obj.parents.all().select_related("menu")

        return {
            "links": links,
            "parents": parents,
            "obj": obj,
            "en": en,
            "zh": zh,
        }


class FudanBBSDocumentView(TemplateView):

    template_name = "fudan/bbs_document.html"

    def get_template_names(self) -> list[str]:
        if get_query_param(self.request, "plain"):
            return ["fudan/bbs_document_plain.html"]

        return [self.template_name]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Document, path=f"/{kwargs['path']}")

        match get_query_param(self.request, "lang"):
            case TranslationLanguages.ENGLISH:
                en, zh = True, False
            case _:
                en, zh = False, True

        start, end = None, None
        if _range := get_query_param(self.request, "range"):
            try:
                parts = _range.split(":", 2)
                if parts[0]:
                    start = int(parts[0])
                if parts[1]:
                    end = int(parts[1])
            except (IndexError, ValueError):
                pass

        content_zh = obj.get_html(start=start, end=end)
        content_en = obj.get_translated_text(start=start, end=end)

        parents = obj.parents.all().select_related("menu")

        return {
            "parents": parents,
            "obj": obj,
            "content_zh": content_zh,
            "content_en": content_en,
            "en": en,
            "zh": zh,
        }
