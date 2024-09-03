import os

from django import template

register = template.Library()


@register.filter(name="get_extension")
def get_extension(value):
    _, ext = os.path.splitext(value)
    return ext.lower() if ext else ""
