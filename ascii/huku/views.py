from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView, View

from ascii.core.utils import reverse
from ascii.huku.models import MLTArtwork, MLTDirectory, MLTFile


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
        sections = obj.sections.all()
        breadcrumbs = build_directory_breadcrumbs(obj)

        return {
            "obj": obj,
            "sections": sections,
            "breadcrumbs": breadcrumbs,
        }


# TODO: Make it look like a section in the file, with only a single artwork in the center, centered on the page
# TODO: Add an obvious way to get back to the file from the individual artwork
# TODO: Better header colors
# TODO: Align file size and add date


class HukuMLTArtworkView(TemplateView):
    template_name = "huku/mlt_artwork.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        obj = get_object_or_404(MLTArtwork, slug=kwargs["slug"])
        breadcrumbs = build_directory_breadcrumbs(obj.section.mlt_file)
        return {
            "obj": obj,
            "breadcrumbs": breadcrumbs,
        }


class HukuMLTFileDownloadView(View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        path = f"/{kwargs['path'][:-4]}"
        obj = get_object_or_404(MLTFile, path=path)
        response = HttpResponse(content=obj.data, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={obj.name}.mlt"
        return response
