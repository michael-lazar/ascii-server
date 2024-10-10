from __future__ import annotations

from typing import Any

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View

from ascii.mozz.forms import MozzGalleryFilterForm
from ascii.mozz.models import ArtPost, ScrollFile


class MozzIndexView(TemplateView):
    template_name = "mozz/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        posts = ArtPost.objects.visible()

        form = MozzGalleryFilterForm(data=self.request.GET)
        if form.is_valid():
            if filetype := form.cleaned_data["filetype"]:
                posts = posts.filter(file_type=filetype)
            if category := form.cleaned_data["category"]:
                match category:
                    case "favorite":
                        posts = posts.filter(favorite=True)

        is_filtered = any(form.cleaned_data.values())

        return {
            "posts": posts,
            "form": form,
            "is_filtered": is_filtered,
        }


class MozzArtPostView(TemplateView):
    template_name = "mozz/artpost.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = get_object_or_404(
            ArtPost.objects.visible().prefetch_related("attachments"),
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
        scrollfile = get_object_or_404(ScrollFile, slug=kwargs["slug"])
        return HttpResponse(scrollfile.text.strip(), content_type="text/plain")
