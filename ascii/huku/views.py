from collections.abc import Iterable

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import format_html_join, mark_safe
from django.views.generic.base import TemplateView, View

from ascii.core.utils import reverse
from ascii.huku.models import MLTDirectory, MLTFile, MLTItem


def build_directory_breadcrumbs(obj: MLTFile | MLTDirectory) -> str:
    crumbs = []
    while obj.parent:
        crumbs.append((obj.public_url, obj.name))
        obj = obj.parent

    crumbs.append((reverse("huku-mlt-directory-index"), "mlt"))

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


class HukuIndexView(TemplateView):
    template_name = "huku/index.html"

    def get_context_data(self, **kwargs):
        mlt_root = MLTDirectory.objects.get(path="/")

        return {
            "mlt_root": mlt_root,
        }


class HukuMLTDirectoryView(TemplateView):
    template_name = "huku/mlt_directory.html"

    def get_context_data(self, **kwargs):
        if path := kwargs.get("path"):
            path = f"/{path}/"
        else:
            path = "/"

        obj = get_object_or_404(MLTDirectory, path=path)

        return {
            "obj": obj,
            "breadcrumbs": build_directory_breadcrumbs(obj),
        }


class HukuMLTFileView(TemplateView):
    template_name = "huku/mlt_file.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        path = f"/{kwargs['path']}"
        obj = get_object_or_404(MLTFile, path=path)
        headings, sections = structure_items(obj.items.all())
        breadcrumbs = build_directory_breadcrumbs(obj)

        return {
            "obj": obj,
            "headings": headings,
            "sections": sections,
            "breadcrumbs": breadcrumbs,
        }


class HukuMLTArtworkView(TemplateView):
    template_name = "huku/mlt_item.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        obj = get_object_or_404(MLTItem, slug=kwargs["slug"])
        if not obj.is_artwork:
            raise Http404()

        parent = obj.mlt_file
        breadcrumbs = build_directory_breadcrumbs(parent)

        return {
            "obj": obj,
            "parent": parent,
            "breadcrumbs": breadcrumbs,
        }


class HukuMLTFileDownloadView(View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        path = f"/{kwargs['path'][:-4]}"
        obj = get_object_or_404(MLTFile, path=path)
        response = HttpResponse(content=obj.data, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={obj.name}.mlt"
        return response
