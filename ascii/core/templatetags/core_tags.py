import os

from django import template

register = template.Library()


@register.filter(name="get_extension")
def get_extension(value):
    _, ext = os.path.splitext(value)
    return ext.lower() if ext else ""


@register.simple_tag(takes_context=True)
def build_page_url(context, page):
    request = context["request"]
    params = request.GET.copy()
    params["page"] = page
    return f"{request.path}?{params.urlencode()}"
