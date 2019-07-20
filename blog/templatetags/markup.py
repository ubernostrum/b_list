from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from ..markup import markup as markup_func


register = template.Library()


@register.filter
@stringfilter
def markup(value):
    return mark_safe(markup_func(value))
