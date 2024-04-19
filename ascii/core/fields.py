from django.db import models


class NonStrippingCharField(models.CharField):
    def formfield(self, **kwargs):
        kwargs["strip"] = False
        return super().formfield(**kwargs)


class NonStrippingTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["strip"] = False
        return super().formfield(**kwargs)
