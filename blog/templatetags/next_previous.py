from django import template
from django.core.exceptions import ObjectDoesNotExist


class NextPreviousNode(template.Node):
    def __init__(self, direction, queryset, date_field, varname):
        (self.direction,
         self.date_field,
         self.varname) = (direction,
                          date_field,
                          varname)
        self.queryset = template.Variable(queryset)

    def render(self, context):
        queryset = list(self.queryset.resolve(context))
        result = None

        try:
            obj = queryset[{'next': 0,
                            'previous': -1}[self.direction]]
        except IndexError:
            return ''

        method = getattr(obj, 'get_%s_by_pub_date' % self.direction)

        try:
            result = method()
        except ObjectDoesNotExist:
            pass

        context[self.varname] = result
        return ''


def next_previous(parser, token):
    """
    Helps navigation of date-based archives, by finding next/previous
    objects.

    This is slightly different from what Django's date-based views do;
    they simply calculate date objects immediately beyond the range of
    the view. This tag finds the first actually-existing Entry, in
    either direction, so that links can go to a date range which
    actually has entries in it.

    This is done in a template tag rather than simply calling the
    model methods in templates because it needs to catch
    ``DoesNotExist`` and simply return ``None``.

    Can be called as either ``get_next`` (to get the first Entry after
    the date range) or ``get_previous`` (to get the first Entry before
    it).

    Syntax::

        {% get_(next/previous) queryset as varname %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError(
            "'%s' takes four arguments" % bits[0]
        )
    if bits[3] != 'as':
        raise template.TemplateSyntaxError(
            "Third argument to '%s' must be 'as'" % bits[0]
        )
    return NextPreviousNode(bits[0].split('_')[1], bits[1], bits[2], bits[4])


register = template.Library()
register.tag('get_next', next_previous)
register.tag('get_previous', next_previous)
