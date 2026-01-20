from django.db import models
from django.urls import reverse


class BaseModel(models.Model):

    class Meta:
        abstract = True

    @property
    def change_url(self):
        view_name = f"admin:{self._meta.app_label}_{self._meta.model_name}_change"
        return reverse(view_name, args=[self.pk])

    @property
    def changelist_url(self):
        view_name = f"admin:{self._meta.app_label}_{self._meta.model_name}_changelist"
        return reverse(view_name)
