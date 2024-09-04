from collections import Counter

from django import forms
from django.db.models import Count

from ascii.textmode.choices import TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag, ArtPack


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, artfiles: ArtFileQuerySet, **kwargs):
        queryset = ArtFileTag.objects.filter(category=category, artfiles__in=artfiles)
        queryset = queryset.order_by("name").annotate(artfile_count=Count("name"))
        initial = queryset.values_list("id", flat=True)
        super().__init__(queryset=queryset, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.artfile_count})"


class PackChoiceField(forms.ModelChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        queryset = ArtPack.objects.filter(artfiles__in=artfiles)
        queryset = queryset.order_by("year", "name").annotate(artfile_count=Count("name"))
        initial = queryset.values_list("id", flat=True)
        super().__init__(queryset=queryset, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtPack) -> str:
        return f"{obj.year} / {obj.name} ({obj.artfile_count})"


class FileExtensionChoiceField(forms.ChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        choices = [("", "all")]
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

        choices = [("", "all")]
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
            empty_label="all",
            blank=True,
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
            empty_label="all",
            blank=True,
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
            label="File Extension",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )


class TagFilterForm(forms.Form):

    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["pack"] = PackChoiceField(
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            empty_label="all",
            blank=True,
            label="Pack",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )
        self.fields["artist"] = ArtFileTagChoiceField(
            category=TagCategory.ARTIST,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            empty_label="all",
            blank=True,
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
            empty_label="all",
            blank=True,
            label="Group",
            widget=forms.RadioSelect(
                attrs={
                    "class": "sidebar-choice-field",
                }
            ),
        )
        self.fields["extension"] = FileExtensionChoiceField(
            artfiles=artfiles,
            required=False,
            label="File Extension",
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
