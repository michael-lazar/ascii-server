from django import forms
from django.db.models import Count

from ascii.textmode.choices import TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, artfiles: ArtFileQuerySet, **kwargs):
        tags_qs = ArtFileTag.objects.filter(category=category, artfiles__in=artfiles)
        tags_qs = tags_qs.order_by("name").annotate(artfile_count=Count("name"))

        initial = tags_qs.values_list("id", flat=True)

        self.unknown_count = artfiles.not_tagged(category).count()

        super().__init__(queryset=tags_qs, initial=initial, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.artfile_count})"

    @property
    def choices(self):
        yield "_unknown", f"unknown ({self.unknown_count})"
        yield from super().choices

    def to_python(self, value):
        if value == "_unknown":
            return value

        return super().to_python(value)


class GalleryFilterForm(forms.Form):

    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["artist"] = ArtFileTagChoiceField(
            category=TagCategory.ARTIST,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="Artist",
            widget=forms.RadioSelect,
        )
