import json
from contextlib import suppress

from django import forms


class FormattedJSONWidget(forms.Textarea):
    """
    Render the value as formatted JSON with spaces and indents.
    """

    def format_value(self, value):
        # May fail if the user enters invalid JSON into the admin form
        with suppress(json.JSONDecodeError):
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
        return value


class ImagePreviewWidget(forms.ClearableFileInput):
    """
    Renders the image form field with an inline preview.
    """

    template_name = "core/widgets/image-preview.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["image_preview"] = value and value.name.endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
        )
        return context
