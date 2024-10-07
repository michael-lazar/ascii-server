from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from ascii.mozz.models import ArtPost


class MozzIndexView(TemplateView):
    template_name = "mozz/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        posts = ArtPost.objects.visible()
        return {"posts": posts}


class MozzArtPostView(TemplateView):
    template_name = "mozz/artpost.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post = get_object_or_404(ArtPost, date=kwargs["date"], slug=kwargs["slug"])
        return {
            "post": post,
            "prev": post.get_prev(),
            "next": post.get_next(),
        }
