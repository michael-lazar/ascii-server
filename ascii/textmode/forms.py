from collections import Counter

from django import forms
from django.db.models import Count

from ascii.textmode.choices import TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag, ArtPack


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, artfiles: ArtFileQuerySet, **kwargs):
        self.unknown_count = artfiles.not_tagged(category).count()

        tags_qs = ArtFileTag.objects.filter(category=category, artfiles__in=artfiles)
        tags_qs = tags_qs.order_by("name").annotate(artfile_count=Count("name"))

        initial = tags_qs.values_list("id", flat=True)
        super().__init__(queryset=tags_qs, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.artfile_count})"

    @property
    def choices(self):
        yield "", "all"

        if self.unknown_count:
            yield "_unknown", f"not set ({self.unknown_count})"

        for choice in super().choices:
            if choice[0]:
                yield choice

    def to_python(self, value):
        if value == "_unknown":
            return value

        return super().to_python(value)


class PackChoiceField(forms.ModelChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        packs_qs = ArtPack.objects.filter(artfiles__in=artfiles)
        packs_qs = packs_qs.order_by("year", "name").annotate(artfile_count=Count("name"))

        initial = packs_qs.values_list("id", flat=True)
        super().__init__(queryset=packs_qs, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtPack) -> str:
        return f"{obj.year} - {obj.name} ({obj.artfile_count})"

    @property
    def choices(self):
        yield "", "all"

        for choice in super().choices:
            if choice[0]:
                yield choice


class FileExtensionChoiceField(forms.ChoiceField):

    def __init__(self, artfiles: ArtFileQuerySet, **kwargs):
        extension_counts = dict(artfiles.count_file_extensions())

        choices = [("", "all")]

        if unknown_count := extension_counts.pop("", 0):
            choices.append(("_none", f"none ({unknown_count})"))

        for ext, count in extension_counts.items():
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

        self.fields["artist"] = ArtFileTagChoiceField(
            category=TagCategory.ARTIST,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="Artist",
            widget=forms.RadioSelect(attrs={"class": "sidebar-choice-field"}),
        )
        self.fields["collab"] = CollabChoiceField(
            artfiles=artfiles,
            required=False,
            label="Collab",
            widget=forms.RadioSelect(attrs={"class": "sidebar-choice-field"}),
        )
        self.fields["extension"] = FileExtensionChoiceField(
            artfiles=artfiles,
            required=False,
            label="File Extension",
            widget=forms.RadioSelect(attrs={"class": "sidebar-choice-field"}),
        )


class TagFilterForm(forms.Form):

    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["pack"] = PackChoiceField(
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="Pack",
            widget=forms.RadioSelect(attrs={"class": "sidebar-choice-field"}),
        )
        self.fields["extension"] = FileExtensionChoiceField(
            artfiles=artfiles,
            required=False,
            label="File Extension",
            widget=forms.RadioSelect(attrs={"class": "sidebar-choice-field"}),
        )
