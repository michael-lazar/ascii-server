from typing import Any

from django.core.paginator import Paginator
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.textmode.choices import TagCategory
from ascii.textmode.forms import PackFilterForm, SearchBarForm, TagFilterForm
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack

PER_PAGE = 10


def get_page_number(request: HttpRequest) -> int:
    try:
        page = int(request.GET.get("page"))  # noqa
    except (TypeError, ValueError):
        page = 1

    return page


class TextmodeIndexView(TemplateView):
    template_name = "textmode/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.annotate_artfile_count().prefetch_fileid()[:10]

        artist_tags = ArtFileTag.objects.for_tag_list(TagCategory.ARTIST)
        artist_tags = artist_tags.order_by("-artfile_count")[:20]

        group_tags = ArtFileTag.objects.for_tag_list(TagCategory.GROUP)
        group_tags = group_tags.order_by("-artfile_count")[:20]

        content_tags = ArtFileTag.objects.for_tag_list(TagCategory.CONTENT)
        content_tags = content_tags.order_by("-artfile_count")[:20]

        form = SearchBarForm()

        return {
            "packs": packs,
            "artist_tags": artist_tags,
            "group_tags": group_tags,
            "content_tags": content_tags,
            "form": form,
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

        p = Paginator(artfiles, PER_PAGE)
        page = p.page(get_page_number(self.request))

        total = artfiles.count()

        return {
            "pack": pack,
            "page": page,
            "total": total,
            "form": form,
            "is_filtered": is_filtered,
        }


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

        # Note the order of the filters is important here!
        # We need to count the artfiles before applying the filter.
        tags = (
            ArtFileTag.objects.order_by("category", "name")
            .annotate_artfile_count()
            .filter(artfiles=artfile)
        )

        return {
            "pack": pack,
            "tags": tags,
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

        p = Paginator(artfiles, PER_PAGE)
        page = p.page(get_page_number(self.request))

        total = artfiles.count()

        return {
            "tag": tag,
            "page": page,
            "total": total,
            "form": form,
            "is_filtered": is_filtered,
        }


class TextmodeTagListView(TemplateView):
    template_name = "textmode/tag_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        artist_tags = ArtFileTag.objects.for_tag_list(TagCategory.ARTIST)
        group_tags = ArtFileTag.objects.for_tag_list(TagCategory.GROUP)
        content_tags = ArtFileTag.objects.for_tag_list(TagCategory.CONTENT)

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

        tags = ArtFileTag.objects.for_tag_list(category)

        form = SearchBarForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                tags = tags.filter(name__icontains=q)

        return {
            "tags": tags,
            "category": category,
            "form": form,
        }


class TextModeSearchView(TemplateView):
    template_name = "textmode/search.html"

    def get_context_data(self, **kwargs):

        form = SearchBarForm(data=self.request.GET)
        artfiles = ArtFile.objects.select_related("pack").all()

        if "q" in self.request.GET:
            show_total = True
            if form.is_valid():
                if q := form.cleaned_data["q"]:
                    artfiles = artfiles.search(q)
        else:
            show_total = False
            artfiles = artfiles.none()

        p = Paginator(artfiles, PER_PAGE)
        page = p.page(get_page_number(self.request))

        total = artfiles.count()

        return {
            "form": form,
            "page": page,
            "total": total,
            "show_total": show_total,
        }
