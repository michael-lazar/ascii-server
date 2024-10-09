from django import forms

from ascii.mozz.choices import ArtPostFileType


class MozzGalleryFilterForm(forms.Form):
    filetype = forms.ChoiceField(
        choices=[("", "Format: All")] + [(k, f"Format: {v}") for k, v in ArtPostFileType.choices],
        required=False,
    )
    category = forms.ChoiceField(
        choices=[("", "Category: All"), ("featured", "Category: Featured")],
        required=False,
    )
