import os

from django.conf import settings
from django.http import HttpRequest


def get_project_file(filepath):
    return os.path.join(settings.BASE_DIR, filepath)


def get_query_param(request: HttpRequest, name: str) -> str | None:
    return request.GET.get(name)  # noqa
