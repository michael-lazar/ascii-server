import typing

from django.db import models
from django.urls import reverse


class DirtyFieldsMixin:
    # https://stackoverflow.com/a/332225

    _original_state: dict
    _meta: typing.Any

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_state = self._as_dict()

    def _as_dict(self):
        return {
            f.name: getattr(self, f.name) for f in self._meta.local_fields if not f.remote_field
        }

    def get_dirty_fields(self):
        new_state = self._as_dict()
        return {
            key: value for key, value in self._original_state.items() if value != new_state[key]
        }


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
