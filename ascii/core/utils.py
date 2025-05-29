import random
import string
from urllib.parse import urlencode

from django.http import HttpRequest
from django.urls import reverse as builtin_reverse


# https://code.djangoproject.com/ticket/25582
def reverse(*args, qs: dict | tuple | None = None, **kwargs) -> str:
    url = builtin_reverse(*args, **kwargs)
    if qs is not None:
        url += "?" + urlencode(qs)
    return url


def get_query_param(request: HttpRequest, name: str) -> str | None:
    return request.GET.get(name)  # noqa


def gen_random_slug(length: int = 12) -> str:
    return "".join(random.choices(string.digits + string.ascii_letters, k=length))
