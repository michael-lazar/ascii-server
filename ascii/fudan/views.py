from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.fudan.models import Document, Menu


class FudanBBSMenuView(TemplateView):

    template_name = "fudan/bbs_menu.html"

    def get_context_data(self, path: str) -> dict[str, Any]:
        obj = get_object_or_404(Menu, path=f"/{path}")
        links = obj.parents.all().select_related("menu")
        return {"obj": obj, "links": links}


class FudanBBSDocumentView(TemplateView):

    template_name = "fudan/bbs_document.html"

    def get_context_data(self, path: str) -> dict[str, Any]:
        obj = get_object_or_404(Document, path=f"/{path}")
        links = obj.parents.all().select_related("menu")
        return {"obj": obj, "links": links}
