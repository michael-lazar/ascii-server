from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ascii.fundan.ansi import ANSIParser
from ascii.fundan.models import Document


class FundanDocumentView(View):
    def get(self, request: HttpRequest, path: str) -> HttpResponse:
        document = get_object_or_404(Document, path=path)

        parser = ANSIParser()
        html = parser.to_html(document.data)
        return HttpResponse(html)
