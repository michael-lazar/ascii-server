from django import forms
from django.db.models import Count

from ascii.textmode.choices import TagCategory
from ascii.textmode.models import ArtFileQuerySet, ArtFileTag


class ArtFileTagChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj: ArtFileTag) -> str:
        return f"{obj.name} ({obj.artfile_count})"


class GalleryFilterForm(forms.Form):

    def __init__(self, artfile_qs: ArtFileQuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)

        artist_tags_qs = (
            ArtFileTag.objects.filter(
                category=TagCategory.ARTIST,
                artfiles__in=artfile_qs,
            )
            .order_by("name")
            .annotate(artfile_count=Count("name"))
        )

        self.fields["artist"] = ArtFileTagChoiceField(
            queryset=artist_tags_qs,
            to_field_name="name",
        )
