from collections.abc import Iterable

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import format_html_join, mark_safe
from django.views.generic.base import TemplateView, View

from ascii.huku.models import MLTDirectory, MLTFile, MLTItem


def build_breadcrumbs(obj: MLTFile | MLTDirectory) -> str:
    crumbs = []
    while obj.parent:
        crumbs.append((obj.public_url, obj.name))
        obj = obj.parent

    return format_html_join(
        mark_safe(' <span class="sep">/</span> '),
        '<a href="{}">{}</a>',
        crumbs[::-1],
    )


def structure_items(items: Iterable[MLTItem]) -> tuple[list, list]:
    sections = []
    headings = []

    for item in items:
        if item.is_heading:
            headings.append(item)
            sections.append(item)
        else:
            if not sections or not isinstance(sections[-1], list):
                sections.append([])
            sections[-1].append(item)

    return headings, sections


class MLTDirectoryView(TemplateView):
    template_name = "huku/mlt_directory.html"

    def get_context_data(self, **kwargs):
        if path := kwargs.get("path"):
            path = f"/{path}/"
        else:
            path = "/"

        obj = get_object_or_404(MLTDirectory, path=path)
        subdirectories = obj.subdirectories.all()
        files = obj.files.all()

        return {
            "obj": obj,
            "subdirectories": subdirectories,
            "files": files,
            "breadcrumbs": build_breadcrumbs(obj),
        }


class MLTFileView(TemplateView):
    template_name = "huku/mlt_file.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        path = f"/{kwargs['path']}"
        obj = get_object_or_404(MLTFile, path=path)
        headings, sections = structure_items(obj.items.all())
        breadcrumbs = build_breadcrumbs(obj)

        return {
            "obj": obj,
            "headings": headings,
            "sections": sections,
            "breadcrumbs": breadcrumbs,
        }


class MLTFileDownloadView(View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        path = f"/{kwargs['path'][:-4]}"
        obj = get_object_or_404(MLTFile, path=path)
        response = HttpResponse(content=obj.data, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={obj.name}.mlt"
        return response
