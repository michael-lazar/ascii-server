from typing import Any

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.textmode.choices import TagCategory
from ascii.textmode.forms import PackFilterForm, SearchBarForm, TagFilterForm
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

        artfiles = (
            pack.artfiles.select_related("pack")
            .annotate_artist_count()
            .order_by("-is_fileid", "name")
        )

        form = PackFilterForm(artfiles, data=self.request.GET)
        if form.is_valid():
            if artist := form.cleaned_data["artist"]:
                artfiles = artfiles.filter(tags=artist)
            if group := form.cleaned_data["group"]:
                artfiles = artfiles.filter(tags=group)
            if extension := form.cleaned_data["extension"]:
                artfiles = artfiles.filter(file_extension=extension)
            if collab := form.cleaned_data["collab"]:
                if collab == "solo":
                    artfiles = artfiles.filter(artist_count__lte=1)
                elif collab == "joint":
                    artfiles = artfiles.filter(artist_count__gt=1)

        is_filtered = any(form.cleaned_data.values())

        return {"pack": pack, "artfiles": artfiles, "form": form, "is_filtered": is_filtered}


class TextmodePackListView(TemplateView):
    template_name = "textmode/pack_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.prefetch_fileid().order_by("-year", "-created_at")

        form = SearchBarForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                packs = packs.filter(name__icontains=q)

        # For some reason the generators appear empty if I loop them inside of
        # the template, I need to cast them to lists first.
        packs_by_year = [(year, list(packs)) for year, packs in packs.group_by_year()]

        return {
            "packs_by_year": packs_by_year,
            "form": form,
        }


class TextmodeArtfileView(TemplateView):
    template_name = "textmode/artfile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(ArtPack, name=kwargs["pack"])
        artfile = get_object_or_404(ArtFile, pack=pack, name=kwargs["artfile"])

        return {
            "pack": pack,
            "artfile": artfile,
            "next": artfile.get_next(),
            "prev": artfile.get_prev(),
            "sauce": artfile.get_sauce_display(),
        }


class TextmodeTagView(TemplateView):
    template_name = "textmode/tag.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        tag = get_object_or_404(ArtFileTag, category=kwargs["category"], name=kwargs["name"])
        artfiles = tag.artfiles.select_related("pack").order_by("-is_fileid", "name")

        form = TagFilterForm(artfiles, data=self.request.GET)
        if form.is_valid():
            if artist := form.cleaned_data["artist"]:
                artfiles = artfiles.filter(tags=artist)
            if group := form.cleaned_data["group"]:
                artfiles = artfiles.filter(tags=group)
            if extension := form.cleaned_data["extension"]:
                artfiles = artfiles.filter(file_extension=extension)
            if pack := form.cleaned_data["pack"]:
                artfiles = artfiles.filter(pack=pack)

        is_filtered = any(form.cleaned_data.values())

        return {
            "tag": tag,
            "artfiles": artfiles,
            "form": form,
            "is_filtered": is_filtered,
        }


class TextmodeTagListView(TemplateView):
    template_name = "textmode/tag_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        artist_tags = ArtFileTag.objects.by_category(TagCategory.ARTIST)
        group_tags = ArtFileTag.objects.by_category(TagCategory.GROUP)
        content_tags = ArtFileTag.objects.by_category(TagCategory.CONTENT)

        form = SearchBarForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                artist_tags = artist_tags.filter(name__icontains=q)
                group_tags = group_tags.filter(name__icontains=q)
                content_tags = content_tags.filter(name__icontains=q)

        return {
            "artist_tags": artist_tags,
            "group_tags": group_tags,
            "content_tags": content_tags,
            "form": form,
        }


class TextmodeTagCategoryListView(TemplateView):
    template_name = "textmode/tag_category_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        category = kwargs["category"]
        if category not in TagCategory:
            raise Http404()

        tags = ArtFileTag.objects.by_category(category)

        form = SearchBarForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                tags = tags.filter(name__icontains=q)

        return {
            "tags": tags,
            "category": category,
            "form": form,
        }
