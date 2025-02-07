from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from ascii.core.utils import get_query_param
from ascii.fudan.models import AssetFile, Document, Menu, ScratchFile


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

        links = obj.links.all()
        parents = obj.parents.all().select_related("menu")
        if parents:
            next_link = parents[0].get_next()
            prev_link = parents[0].get_prev()
        else:
            next_link = None
            prev_link = None

        return {
            "links": links,
            "parents": parents,
            "next_link": next_link,
            "prev_link": prev_link,
            "obj": obj,
            "lang": "en",
        }


class FudanBBSDocumentView(TemplateView):

    template_name = "fudan/bbs_document.html"

    def get_template_names(self) -> list[str]:
        if get_query_param(self.request, "plain"):
            return ["fudan/bbs_document_plain.html"]

        return [self.template_name]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Document, path=f"/{kwargs['path']}")

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

        if get_query_param(self.request, "plain"):
            content_en = None
        else:
            content_en = obj.get_translated_text(start=start, end=end)

        parents = obj.parents.all().select_related("menu")
        if parents:
            next_link = parents[0].get_next()
            prev_link = parents[0].get_prev()
        else:
            next_link = None
            prev_link = None

        return {
            "parents": parents,
            "next_link": next_link,
            "prev_link": prev_link,
            "obj": obj,
            "content_zh": content_zh,
            "content_en": content_en,
            "lang": "zh",
        }
