from urllib.parse import urlencode

from django.urls import reverse as builtin_reverse


# https://code.djangoproject.com/ticket/25582
def reverse(*args, qs: dict | tuple | None = None, **kwargs) -> str:
    url = builtin_reverse(*args, **kwargs)
    if qs is not None:
        url += "?" + urlencode(qs)
    return url
