from __future__ import annotations

from typing import Any

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View

from ascii.mozz.choices import PLAINTEXT_FILETYPES, TEXTMODE_FILETYPES
from ascii.mozz.models import ArtPost, ScrollFile

SCROLLFILE_SLUG = "scrollfile"


class MozzIndexView(TemplateView):
    template_name = "mozz/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        posts = ArtPost.objects.visible()

        filetype = self.request.GET.get("filetype", "")
        match filetype:
            case "plaintext":
                posts = posts.filter(file_type__in=PLAINTEXT_FILETYPES)
            case "textmode":
                posts = posts.filter(file_type__in=TEXTMODE_FILETYPES)
            case _:
                filetype = ""

        return {
            "posts": posts,
            "filetype": filetype,
        }


class MozzAboutView(TemplateView):
    template_name = "mozz/about.html"


class MozzArtPostView(TemplateView):
    template_name = "mozz/artpost.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = get_object_or_404(
            ArtPost.objects.prefetch_related("attachments"),
            date=kwargs["date"],
            slug=kwargs["slug"],
        )
        return {
            "post": post,
            "prev": post.get_prev(),
            "next": post.get_next(),
        }


class MozzScrollFileView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        scrollfile = get_object_or_404(ScrollFile, slug=SCROLLFILE_SLUG)
        return HttpResponse(scrollfile.text, content_type="text/plain")
