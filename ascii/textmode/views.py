from typing import Any

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.textmode.choices import TagCategory
from ascii.textmode.forms import GalleryFilterForm
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack


class TextmodeIndexView(TemplateView):

    template_name = "textmode/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.annotate_artfile_count().prefetch_fileid()[:20]

        artist_tags = ArtFileTag.objects.by_category(TagCategory.ARTIST)
        artist_tags = artist_tags.order_by("-artfile_count")[:20]

        group_tags = ArtFileTag.objects.by_category(TagCategory.GROUP)
        group_tags = group_tags.order_by("-artfile_count")[:20]

        content_tags = ArtFileTag.objects.by_category(TagCategory.CONTENT)
        content_tags = content_tags.order_by("-artfile_count")[:20]

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

        artfiles = pack.artfiles.select_related("pack").order_by("-is_fileid", "name")

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


class TextmodePackListView(TemplateView):

    template_name = "textmode/pack_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.prefetch_fileid()

        return {"packs": packs}


class TextmodeArtfileView(TemplateView):
    template_name = "textmode/artfile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(ArtPack, name=kwargs["pack"])
        artfile = get_object_or_404(ArtFile, pack=pack, name=kwargs["artfile"])

        return {"pack": pack, "artfile": artfile}


class TextmodeTagListView(TemplateView):

    template_name = "textmode/tag_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        artist_tags = ArtFileTag.objects.by_category(TagCategory.ARTIST)
        group_tags = ArtFileTag.objects.by_category(TagCategory.GROUP)
        content_tags = ArtFileTag.objects.by_category(TagCategory.CONTENT)

        return {
            "artist_tags": artist_tags,
            "group_tags": group_tags,
            "content_tags": content_tags,
        }


class TextmodeTagCategoryListView(TemplateView):

    template_name = "textmode/tag_category_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        category = kwargs["category"]
        if category not in TagCategory:
            raise Http404()

        tags = ArtFileTag.objects.by_category(category)

        return {"tags": tags, "category": category}
