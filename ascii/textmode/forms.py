from dal import autocomplete
from django import forms
from django.db.models import Count

from ascii.textmode.choices import AspectRatio, LetterSpacing, TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag, ArtPack


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, artfiles: ArtFileQuerySet, **kwargs):
        queryset = ArtFileTag.objects.filter(category=category, artfiles__in=artfiles)
        queryset = queryset.annotate(tag_count=Count("name")).order_by("-tag_count")
        initial = queryset.values_list("id", flat=True)
        super().__init__(queryset=queryset, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.tag_count})"


class PackChoiceField(forms.ModelChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        queryset = ArtPack.objects.filter(artfiles__in=artfiles)
        queryset = queryset.annotate(artfile_count=Count("name")).order_by("-artfile_count")
        initial = queryset.values_list("id", flat=True)
        super().__init__(queryset=queryset, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtPack) -> str:
        return f"{obj.year}/{obj.name} ({obj.artfile_count})"


class FileExtensionChoiceField(forms.ChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        choices = []
        for ext, count in artfiles.count_file_extensions():
            choices.append((ext, f"{ext} ({count})"))

        super().__init__(choices=choices, **kwargs)


class PackYearChoiceField(forms.ChoiceField):

    def __init__(self, **kwargs):
        choices = [("", "all years")]
        for year in ArtPack.objects.list_years():
            choices.append((year, year))
        super().__init__(choices=choices, **kwargs)


class CollabChoiceField(forms.ChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        choices = []
        for is_joint, count in artfiles.count_is_joint():
            if is_joint:
                choices.append(("joint", f"joint ({count})"))
            else:
                choices.append(("solo", f"solo ({count})"))

        super().__init__(choices=choices, **kwargs)


class PackFilterForm(forms.Form):

    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.artfiles = artfiles

        self.fields["artist"] = ArtFileTagChoiceField(
            category=TagCategory.ARTIST,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="Artist",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )
        self.fields["group"] = ArtFileTagChoiceField(
            category=TagCategory.GROUP,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="Group",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )
        self.fields["collab"] = CollabChoiceField(
            artfiles=artfiles,
            required=False,
            label="Collab",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )
        self.fields["extension"] = FileExtensionChoiceField(
            artfiles=artfiles,
            required=False,
            label="Extension",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )


class SearchBarForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search...",
                "autocomplete": "off",
            },
        ),
    )


class SearchPackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["q"] = forms.CharField(
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={
                    "placeholder": "search...",
                    "autocomplete": "off",
                },
            ),
        )
        self.fields["year"] = PackYearChoiceField(required=False)


class AdvancedSearchForm(forms.Form):
    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["q"] = forms.CharField(
            required=False,
            label="Filename",
            widget=forms.TextInput(
                attrs={
                    "placeholder": "Name",
                    "autocomplete": "off",
                    "class": "advanced-search-input",
                },
            ),
        )
        self.fields["extension"] = forms.MultipleChoiceField(
            choices=[(val, val) for val in artfiles.file_extensions()],
            label="Extension",
            required=False,
            widget=autocomplete.Select2Multiple,
        )
        self.fields["ice_colors"] = forms.MultipleChoiceField(
            choices=[(False, "no"), (True, "yes")],
            label="ICE Colors",
            widget=autocomplete.Select2Multiple,
            required=False,
        )
        self.fields["is_joint"] = forms.MultipleChoiceField(
            choices=[(False, "solo"), (True, "joint")],
            label="Collaboration",
            widget=autocomplete.Select2Multiple,
            required=False,
        )
        self.fields["letter_spacing"] = forms.MultipleChoiceField(
            choices=LetterSpacing.choices,
            label="Letter Spacing",
            widget=autocomplete.Select2Multiple,
            required=False,
        )
        self.fields["aspect_ratio"] = forms.MultipleChoiceField(
            choices=AspectRatio.choices,
            label="Aspect Ratio",
            widget=autocomplete.Select2Multiple,
            required=False,
        )
        self.fields["font_name"] = forms.MultipleChoiceField(
            choices=[(val, val) for val in artfiles.font_names()],
            label="Font Name",
            required=False,
            widget=autocomplete.Select2Multiple,
        )
        self.fields["artist"] = forms.ModelMultipleChoiceField(
            queryset=ArtFileTag.objects.artists(),
            required=False,
            to_field_name="name",
            label="Artist",
            widget=autocomplete.ModelSelect2Multiple(
                url="textmode-artist-autocomplete",
            ),
        )
        self.fields["group"] = forms.ModelMultipleChoiceField(
            queryset=ArtFileTag.objects.groups(),
            required=False,
            to_field_name="name",
            label="Group",
            widget=autocomplete.ModelSelect2Multiple(
                url="textmode-group-autocomplete",
            ),
        )
        self.fields["content"] = forms.ModelMultipleChoiceField(
            queryset=ArtFileTag.objects.content(),
            required=False,
            to_field_name="name",
            label="Content",
            widget=autocomplete.ModelSelect2Multiple(
                url="textmode-content-autocomplete",
            ),
        )
        self.fields["pack"] = forms.ModelMultipleChoiceField(
            queryset=ArtPack.objects.all(),
            required=False,
            to_field_name="name",
            label="Pack",
            widget=autocomplete.ModelSelect2Multiple(
                url="textmode-pack-autocomplete",
            ),
        )
        self.fields["min_num_lines"] = forms.IntegerField(
            min_value=0,
            required=False,
            label="Min",
            widget=forms.NumberInput(
                attrs={
                    "placeholder": "Min",
                    "class": "advanced-search-input",
                }
            ),
        )
        self.fields["max_num_lines"] = forms.IntegerField(
            min_value=0,
            required=False,
            label="Max",
            widget=forms.NumberInput(
                attrs={
                    "placeholder": "Max",
                    "class": "advanced-search-input",
                }
            ),
        )
        self.fields["min_char_width"] = forms.IntegerField(
            min_value=0,
            required=False,
            label="Min",
            widget=forms.NumberInput(
                attrs={
                    "placeholder": "Min",
                    "class": "advanced-search-input",
                }
            ),
        )
        self.fields["max_char_width"] = forms.IntegerField(
            min_value=0,
            required=False,
            label="Max",
            widget=forms.NumberInput(
                attrs={
                    "placeholder": "Max",
                    "class": "advanced-search-input",
                }
            ),
        )

        pack_years = list(ArtPack.objects.list_years())

        self.fields["min_year"] = forms.IntegerField(
            min_value=pack_years[0],
            max_value=pack_years[-1],
            required=False,
            label="Min",
            widget=forms.NumberInput(
                attrs={
                    "placeholder": "Min",
                    "class": "advanced-search-input",
                }
            ),
        )
        self.fields["max_year"] = forms.IntegerField(
            min_value=pack_years[0],
            max_value=pack_years[-1],
            required=False,
            label="Max",
            widget=forms.NumberInput(
                attrs={
                    "placeholder": "Max",
                    "class": "advanced-search-input",
                }
            ),
        )
        self.fields["order"] = forms.ChoiceField(
            choices=(
                ("", ""),
                ("pack__year", "year"),
                ("-pack__year", "year (reverse)"),
                ("name", "name"),
                ("-name", "name (reverse)"),
                ("filesize", "size"),
                ("-filesize", "size (reverse)"),
                ("number_of_lines", "rows"),
                ("-number_of_lines", "rows (reverse)"),
                ("character_width", "columns"),
                ("-character_width", "columns (reverse)"),
            ),
            label="Sort Order",
            widget=autocomplete.Select2,
            required=False,
        )

    @property
    def fieldsets(self):
        for field in self:
            if field.name != "q":
                yield field
