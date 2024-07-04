from django import template

register = template.Library()

@register.filter
def is_external_link(value):
    return value.strip().startswith("http")