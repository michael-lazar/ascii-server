from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.textmode.choices import TagCategory
from ascii.textmode.forms import GalleryFilterForm
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack


class TextmodeIndexView(TemplateView):

    template_name = "textmode/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.annotate_artfile_count().prefetch_fileid()

        artist_tags = (
            ArtFileTag.objects.visible()
            .filter(category=TagCategory.ARTIST)
            .annotate_artfile_count()
            .order_by("-artfile_count")
        )
        group_tags = (
            ArtFileTag.objects.visible()
            .filter(category=TagCategory.GROUP)
            .annotate_artfile_count()
            .order_by("-artfile_count")
        )
        content_tags = (
            ArtFileTag.objects.visible()
            .filter(category=TagCategory.CONTENT)
            .annotate_artfile_count()
            .order_by("-artfile_count")
        )

        return {
            "packs": packs,
            "artist_tags": artist_tags,
            "group_tags": group_tags,
            "content_tags": content_tags,
        }


class TextmodePackView(TemplateView):

    template_name = "textmode/pack.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(ArtPack, name=kwargs["pack"])

        artfiles = pack.artfiles.select_related("pack").all()

        filter_form = GalleryFilterForm(artfiles, data=self.request.GET)
        if filter_form.is_valid():
            cleaned_data = filter_form.cleaned_data
            if cleaned_data["artist"]:
                artfiles = artfiles.filter(tags=cleaned_data["artist"])
            if cleaned_data["group"]:
                artfiles = artfiles.filter(tags=cleaned_data["group"])
            if cleaned_data["content"]:
                artfiles = artfiles.filter(tags=cleaned_data["content"])

        return {
            "pack": pack,
            "artfiles": artfiles,
            "filter_form": filter_form,
        }


class TextmodePacksView(TemplateView):

    template_name = "textmode/packs.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.prefetch_fileid()

        return {"packs": packs}


class TextmodeArtfileView(TemplateView):
    template_name = "textmode/artfile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(ArtPack, name=kwargs["pack"])
        artfile = get_object_or_404(ArtFile, pack=pack, name=kwargs["artfile"])

        return {
            "pack": pack,
            "artfile": artfile,
        }
