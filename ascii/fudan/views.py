from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.fudan.models import Document, Menu


class FudanBBSMenuView(TemplateView):

    template_name = "fudan/bbs_menu.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Menu, path=f"/{kwargs['path']}")

        parents = obj.parents.all().select_related("menu")
        links = obj.links.all()

        return {"links": links, "parents": parents, "obj": obj}


class FudanBBSDocumentView(TemplateView):

    template_name = "fudan/bbs_document.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        obj = get_object_or_404(Document, path=f"/{kwargs['path']}")

        parents = obj.parents.all().select_related("menu")
        html = obj.get_html()

        return {"html": html, "parents": parents, "obj": obj}
