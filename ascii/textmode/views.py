from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.textmode.forms import GalleryFilterForm
from ascii.textmode.models import ArtFile, ArtPack


class TextmodeIndexView(TemplateView):

    template_name = "textmode/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.annotate_artfile_count().prefetch_fileid()
        return {"packs": packs}


class TextmodePackView(TemplateView):

    template_name = "textmode/pack.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(
            ArtPack,
            name=kwargs["pack"],
        )
        artfiles = pack.artfiles.select_related("pack").all()

        filter_form = GalleryFilterForm(artfiles)

        return {"pack": pack, "artfiles": artfiles, "filter_form": filter_form}


class TextmodeArtfileView(TemplateView):
    template_name = "textmode/artfile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        artfile = get_object_or_404(
            ArtFile,
            pack__name=kwargs["pack"],
            name=kwargs["artfile"],
        )
        return {"artfile": artfile}
