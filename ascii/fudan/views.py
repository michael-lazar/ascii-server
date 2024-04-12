from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.fudan.models import Document, Menu


class FudanBBSView(TemplateView):

    template_name = "fudan/ansi_bbs.html"

    def get_context_data(self, path: str) -> dict[str, Any]:
        if path.endswith("/"):
            obj = get_object_or_404(Menu, path=path)
        else:
            obj = get_object_or_404(Document, path=path)

        bbs_html = obj.get_html()
        return {"bbs_html": bbs_html}
