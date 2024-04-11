from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.fudan.models import Document, Menu


class FundanDocumentView(TemplateView):

    template_name = "fudan/ansi_document.html"

    def get_context_data(self, path: str) -> dict[str, Any]:
        document = get_object_or_404(Document, path=path)
        return {"document": document}


class FudanMenuView(TemplateView):

    template_name = "fudan/ansi_menu.html"

    def get_context_data(self, path: str) -> dict[str:Any]:
        menu = get_object_or_404(Menu, path=path)
        return {"menu": menu}
