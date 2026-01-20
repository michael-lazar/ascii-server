from typing import Any

from django.db import models
from django.forms import ChoiceField, Field


class NonStrippingCharField(models.CharField):
    def formfield(
        self,
        form_class: type[Field] | None = None,
        choices_form_class: type[ChoiceField] | None = None,
        **kwargs: Any,
    ) -> Field | None:
        kwargs["strip"] = False
        return super().formfield(form_class, choices_form_class, **kwargs)


class NonStrippingTextField(models.TextField):
    def formfield(
        self,
        form_class: type[Field] | None = None,
        choices_form_class: type[ChoiceField] | None = None,
        **kwargs: Any,
    ) -> Field | None:
        kwargs["strip"] = False
        return super().formfield(form_class, choices_form_class, **kwargs)
