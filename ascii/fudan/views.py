from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.fudan.ansi import ANSIParser
from ascii.fudan.models import Document


class FundanDocumentView(TemplateView):

    template_name = "fundan/ansi_document.html"

    def get_context_data(self, path: str) -> dict[str, Any]:
        document = get_object_or_404(Document, path=path)

        parser = ANSIParser()
        ansi = parser.to_html(document.data)

        return {"ansi": ansi}
