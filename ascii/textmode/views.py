from typing import Any

from dal import autocomplete
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ascii.core.utils import reverse
from ascii.textmode.choices import TagCategory
from ascii.textmode.forms import AdvancedSearchForm, PackFilterForm, SearchBarForm, SearchPackForm
from ascii.textmode.models import ALT_SLASH, ArtFile, ArtFileTag, ArtPack, Gallery

PAGE_SIZE = 100


def get_page_number(request: HttpRequest) -> int:
    try:
        page = int(request.GET.get("page"))  # noqa
    except (TypeError, ValueError):
        page = 1

    return page


class TextmodeIndexView(TemplateView):
    template_name = "textmode/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.prefetch_fileid().order_by("-year")[:10]

        galleries = Gallery.objects.visible().annotate_artfile_count()
        galleries = galleries.order_by("-artfile_count")[:20]

        artist_tags = ArtFileTag.objects.for_tag_list(TagCategory.ARTIST)
        artist_tags = artist_tags.order_by("-artfile_count")[:20]

        group_tags = ArtFileTag.objects.for_tag_list(TagCategory.GROUP)
        group_tags = group_tags.order_by("-artfile_count")[:20]

        content_tags = ArtFileTag.objects.for_tag_list(TagCategory.CONTENT)
        content_tags = content_tags.order_by("-artfile_count")[:20]

        search_bar_form = SearchBarForm()
        search_pack_form = SearchPackForm()

        return {
            "packs": packs,
            "galleries": galleries,
            "artist_tags": artist_tags,
            "group_tags": group_tags,
            "content_tags": content_tags,
            "search_bar_form": search_bar_form,
            "search_pack_form": search_pack_form,
        }


class TextmodePackView(TemplateView):

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("Hx-Request"):
            return ["textmode/fragments/artfile_grid_partial.html"]
        else:
            return ["textmode/pack.html"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(ArtPack, name=kwargs["pack"])

        artfiles = pack.artfiles.select_related("pack").order_by("-is_fileid", "name")

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
                    artfiles = artfiles.filter(is_joint=False)
                elif collab == "joint":
                    artfiles = artfiles.filter(is_joint=True)

        search_url = reverse("textmode-search", qs={"pack": pack.name})

        is_filtered = any(form.cleaned_data.values())

        p = Paginator(artfiles, PAGE_SIZE)
        page = p.page(get_page_number(self.request))

        return {
            "pack": pack,
            "page": page,
            "form": form,
            "is_filtered": is_filtered,
            "search_url": search_url,
        }


class TextmodePackListView(TemplateView):
    template_name = "textmode/pack_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        packs = ArtPack.objects.prefetch_fileid().order_by("-year", "-created_at")

        form = SearchPackForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                packs = packs.filter(name__icontains=q)
            if year := form.cleaned_data["year"]:
                packs = packs.filter(year=year)

        # For some reason the generators appear empty if I loop them inside of
        # the template, I need to cast them to lists first.
        packs_by_year = [(year, list(packs)) for year, packs in packs.group_by_year()]

        return {
            "packs_by_year": packs_by_year,
            "form": form,
        }


class TextmodePackYearListView(TemplateView):
    template_name = "textmode/pack_year_list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        year = kwargs["year"]

        packs = ArtPack.objects.prefetch_fileid().filter(year=year).order_by("-created_at")

        form = SearchBarForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                packs = packs.filter(name__icontains=q)

        return {
            "packs": packs,
            "form": form,
            "year": year,
        }


class TextmodeArtFileView(TemplateView):
    template_name = "textmode/artfile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        pack = get_object_or_404(ArtPack, name=kwargs["pack"])
        artfile = get_object_or_404(ArtFile, pack=pack, name=kwargs["artfile"])

        tags = ArtFileTag.objects.order_by("category", "name").filter(artfiles=artfile)

        return {
            "pack": pack,
            "tags": tags,
            "artfile": artfile,
            "next": artfile.get_next(),
            "prev": artfile.get_prev(),
            "sauce": artfile.get_sauce_display(),
        }


class TextmodeTagView(TemplateView):

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("Hx-Request"):
            return ["textmode/fragments/artfile_grid_partial.html"]
        else:
            return ["textmode/tag.html"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        name = kwargs["name"]
        name = name.replace(ALT_SLASH, "/")

        tag = get_object_or_404(ArtFileTag, category=kwargs["category"], name=name)

        artfiles = tag.artfiles.select_related("pack").order_by("name")

        p = Paginator(artfiles, PAGE_SIZE)
        page = p.page(get_page_number(self.request))

        match tag.category:
            case TagCategory.GROUP:
                search_url = reverse("textmode-search", qs={"group": tag.name})
            case TagCategory.ARTIST:
                search_url = reverse("textmode-search", qs={"artist": tag.name})
            case TagCategory.CONTENT:
                search_url = reverse("textmode-search", qs={"content": tag.name})
            case _:
                raise ValueError

        return {
            "tag": tag,
            "page": page,
            "search_url": search_url,
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

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("Hx-Request"):
            return ["textmode/fragments/artfile_grid_partial.html"]
        else:
            return ["textmode/search.html"]

    def get_context_data(self, **kwargs):
        artfiles = ArtFile.objects.select_related("pack").all()
        form = AdvancedSearchForm(artfiles, data=self.request.GET)

        if form.is_valid():
            if q := form.cleaned_data["q"]:
                artfiles = artfiles.search(q)
            if extension := form.cleaned_data["extension"]:
                artfiles = artfiles.filter(file_extension__in=extension)
            if ice_colors := form.cleaned_data["ice_colors"]:
                artfiles = artfiles.filter(ice_colors__in=ice_colors)
            if letter_spacing := form.cleaned_data["letter_spacing"]:
                artfiles = artfiles.filter(letter_spacing__in=letter_spacing)
            if aspect_ratio := form.cleaned_data["aspect_ratio"]:
                artfiles = artfiles.filter(aspect_ratio__in=aspect_ratio)
            if font_name := form.cleaned_data["font_name"]:
                artfiles = artfiles.filter(font_name__in=font_name)
            if artist := form.cleaned_data["artist"]:
                artfiles = artfiles.filter(tags__in=artist)
            if group := form.cleaned_data["group"]:
                artfiles = artfiles.filter(tags__in=group)
            if content := form.cleaned_data["content"]:
                artfiles = artfiles.filter(tags__in=content)
            if pack := form.cleaned_data["pack"]:
                artfiles = artfiles.filter(pack__in=pack)
            if min_num_lines := form.cleaned_data["min_num_lines"]:
                artfiles = artfiles.filter(number_of_lines__gte=min_num_lines)
            if max_num_lines := form.cleaned_data["max_num_lines"]:
                artfiles = artfiles.filter(number_of_lines__lte=max_num_lines)
            if min_char_width := form.cleaned_data["min_char_width"]:
                artfiles = artfiles.filter(character_width__gte=min_char_width)
            if max_char_width := form.cleaned_data["max_char_width"]:
                artfiles = artfiles.filter(character_width__lte=max_char_width)
            if min_year := form.cleaned_data["min_year"]:
                artfiles = artfiles.filter(pack__year__gte=min_year)
            if max_year := form.cleaned_data["max_year"]:
                artfiles = artfiles.filter(pack__year__lte=max_year)
            if is_joint := form.cleaned_data["is_joint"]:
                artfiles = artfiles.filter(is_joint__in=is_joint)
            if order := form.cleaned_data["order"]:
                artfiles = artfiles.filter(**{f"{order.lstrip('-')}__isnull": False})
                artfiles = artfiles.order_by(order)

        p = Paginator(artfiles, PAGE_SIZE)
        page = p.page(get_page_number(self.request))

        is_filtered = any(form.cleaned_data.values())

        return {
            "form": form,
            "page": page,
            "is_filtered": is_filtered,
        }


class TextModeGalleryView(TemplateView):
    template_name = "textmode/gallery.html"

    def get_context_data(self, **kwargs):
        gallery = get_object_or_404(Gallery, id=kwargs["id"])
        artfiles = gallery.artfiles.all()

        p = Paginator(artfiles, PAGE_SIZE)
        page = p.page(get_page_number(self.request))

        return {"gallery": gallery, "page": page}


class TextModeGalleryListView(TemplateView):
    template_name = "textmode/gallery_list.html"

    def get_context_data(self, **kwargs):
        galleries = Gallery.objects.visible().annotate_artfile_count()

        form = SearchBarForm(data=self.request.GET)
        if form.is_valid():
            if q := form.cleaned_data["q"]:
                galleries = galleries.filter(name__icontains=q)

        return {"galleries": galleries, "form": form}


class TextModeArtistAutocomplete(autocomplete.Select2QuerySetView):
    queryset = ArtFileTag.objects.artists()
    paginate_by = 100

    def get_result_value(self, result):
        return result.name


class TextModeGroupAutocomplete(autocomplete.Select2QuerySetView):
    queryset = ArtFileTag.objects.groups()
    paginate_by = 100

    def get_result_value(self, result):
        return result.name


class TextModeContentAutocomplete(autocomplete.Select2QuerySetView):
    queryset = ArtFileTag.objects.content()
    paginate_by = 100

    def get_result_value(self, result):
        return result.name


class TextModePackAutocomplete(autocomplete.Select2QuerySetView):
    queryset = ArtPack.objects.all()
    paginate_by = 100

    def get_result_label(self, obj: ArtPack):
        return f"pack: {obj.name}"

    def get_result_value(self, result):
        return result.name
