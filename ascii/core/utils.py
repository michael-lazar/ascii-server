from django.http import HttpRequest


def get_query_param(request: HttpRequest, name: str) -> str | None:
    return request.GET.get(name)  # noqa
