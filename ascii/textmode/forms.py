from django import forms
from django.db.models import Count

from ascii.textmode.choices import TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def __init__(self, category: TagCategory, artfiles: ArtFileQuerySet, **kwargs):
        queryset = (
            ArtFileTag.objects.filter(category=category, artfiles__in=artfiles)
            .order_by("name")
            .annotate(artfile_count=Count("name"))
        )
        super().__init__(queryset=queryset, **kwargs)

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.artfile_count})"


class GalleryFilterForm(forms.Form):

    def __init__(self, artfiles: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["artist"] = ArtFileTagChoiceField(
            category=TagCategory.ARTIST,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="artist",
        )

        self.fields["group"] = ArtFileTagChoiceField(
            category=TagCategory.GROUP,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="group",
        )

        self.fields["content"] = ArtFileTagChoiceField(
            category=TagCategory.CONTENT,
            artfiles=artfiles,
            required=False,
            to_field_name="name",
            label="content",
        )
