from django import forms

from ascii.mozz.choices import ArtPostFileType


class MozzGalleryFilterForm(forms.Form):
    filetype = forms.ChoiceField(
        choices=[("", "All formats")] + ArtPostFileType.choices,
        required=False,
    )
