from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.textmode.models import ArtFile, ArtistTag, ArtPack, ContentTag, GroupTag


class TextmodeIndexView(TemplateView):

    template_name = "textmode/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.annotate_artfile_count().all()
        return {"packs": packs}


class TextmodePackView(TemplateView):

    template_name = "textmode/pack.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(
            ArtPack,
            name=kwargs["pack"],
        )
        artfiles = pack.artfiles.select_related("pack").all()
        return {"pack": pack, "artfiles": artfiles}


class TextmodeArtfileView(TemplateView):
    template_name = "textmode/artfile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        artfile = get_object_or_404(
            ArtFile,
            pack__name=kwargs["pack"],
            name=kwargs["artfile"],
        )
        return {"artfile": artfile}


class TextmodeGroupTagListView(TemplateView):
    template_name = "textmode/group_tag_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        tags = GroupTag.objects.annotate_artfile_count().all()
        return {"tags": tags}


class TextmodeGroupTagDetailView(TemplateView):
    template_name = "textmode/group_tag_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        tag = get_object_or_404(GroupTag, name=kwargs["name"])
        artfiles = tag.artfiles.select_related("pack").all()
        return {"tag": tag, "artfiles": artfiles}


class TextmodeArtistTagListView(TemplateView):
    template_name = "textmode/artist_tag_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        tags = ArtistTag.objects.annotate_artfile_count().all()
        return {"tags": tags}


class TextmodeArtistTagDetailView(TemplateView):
    template_name = "textmode/artist_tag_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        tag = get_object_or_404(ArtistTag, name=kwargs["name"])
        artfiles = tag.artfiles.select_related("pack").all()
        return {"tag": tag, "artfiles": artfiles}


class TextmodeContentTagListView(TemplateView):
    template_name = "textmode/content_tag_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        tags = ContentTag.objects.annotate_artfile_count().all()
        return {"tags": tags}


class TextmodeContentTagDetailView(TemplateView):
    template_name = "textmode/content_tag_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        tag = get_object_or_404(ContentTag, name=kwargs["name"])
        artfiles = tag.artfiles.select_related("pack").all()
        return {"tag": tag, "artfiles": artfiles}
