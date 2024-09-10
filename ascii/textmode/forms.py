from collections import Counter

from django import forms
from django.db.models import Count

from ascii.textmode.choices import AspectRatio, DataType, FileType, LetterSpacing, TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag, ArtPack


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, artfiles: ArtFileQuerySet, **kwargs):
        queryset = ArtFileTag.objects.filter(category=category, artfiles__in=artfiles)
        queryset = queryset.annotate(artfile_count=Count("name")).order_by("-artfile_count")
        initial = queryset.values_list("id", flat=True)
        super().__init__(queryset=queryset, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.artfile_count})"


class ArtFileTagSimpleChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, **kwargs):
        queryset = ArtFileTag.objects.filter(category=category)
        initial = queryset.values_list("id", flat=True)
        super().__init__(queryset=queryset, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return obj.name


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


class CollabChoiceField(forms.ChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):

        counter = Counter()
        for artfile in artfiles.all():
            if artfile.artist_count == 1:
                counter["solo"] += 1
            elif artfile.artist_count > 1:
                counter["joint"] += 1

        choices = []
        if count := counter["solo"]:
            choices.append(("solo", f"solo ({count})"))
        if count := counter["joint"]:
            choices.append(("joint", f"joint ({count})"))

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
                "type": "search",
            },
        ),
    )


class AdvancedSearchForm(forms.Form):
    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["q"] = forms.CharField(
            required=False,
            label="Keyword",
            widget=forms.TextInput(
                attrs={
                    "placeholder": "search...",
                    "autocomplete": "off",
                    "type": "search",
                },
            ),
        )
        self.fields["is_fileid"] = forms.ChoiceField(
            choices=[(False, "no"), (True, "yes")],
            label="File ID",
            widget=forms.RadioSelect,
            required=False,
        )

        extensions = (
            artfiles.order_by("file_extension")
            .values_list("file_extension", flat=True)
            .exclude(file_extension="")
            .distinct()
        )
        self.fields["extension"] = forms.ChoiceField(
            choices=(("", ""), *((val, val) for val in extensions)),
            label="Extension",
            required=False,
        )
        self.fields["datatype"] = forms.ChoiceField(
            choices=(("", ""), *DataType.choices),
            label="Data Type",
            required=False,
        )
        self.fields["filetype"] = forms.ChoiceField(
            choices=(("", ""), *FileType.choices),
            label="File Type",
            required=False,
        )
        self.fields["ice_colors"] = forms.ChoiceField(
            choices=[(False, "no"), (True, "yes")],
            label="ICE Colors",
            widget=forms.RadioSelect,
            required=False,
        )
        self.fields["letter_spacing"] = forms.ChoiceField(
            choices=LetterSpacing.choices,
            label="Letter Spacing",
            widget=forms.RadioSelect,
            required=False,
        )
        self.fields["aspect_ratio"] = forms.ChoiceField(
            choices=AspectRatio.choices,
            label="Aspect Ratio",
            widget=forms.RadioSelect,
            required=False,
        )

        font_names = (
            artfiles.order_by("font_name")
            .values_list("font_name", flat=True)
            .exclude(font_name="")
            .distinct()
        )
        self.fields["font_name"] = forms.ChoiceField(
            choices=(("", ""), *((val, val) for val in font_names)),
            label="Font Name",
            required=False,
        )

        years = artfiles.order_by("pack__year").values_list("pack__year", flat=True).distinct()
        self.fields["year"] = forms.ChoiceField(
            choices=(("", ""), *((val, val) for val in years)),
            label="Year",
            required=False,
        )

        self.fields["artist"] = ArtFileTagSimpleChoiceField(
            category=TagCategory.ARTIST,
            required=False,
            to_field_name="name",
            label="Artist",
        )
        self.fields["group"] = ArtFileTagSimpleChoiceField(
            category=TagCategory.GROUP,
            required=False,
            to_field_name="name",
            label="Group",
        )

    @property
    def fieldsets(self):
        for field in self:
            if field.name != "q":
                yield field
