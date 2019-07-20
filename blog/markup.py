from markdown import markdown
from typogrify.filters import typogrify


def markup(text):
    """
    Mark up plain text into fancy HTML.

    """
    return typogrify(
        markdown(text,
                 lazy_ol=False,
                 output_format='html5',
                 extensions=['abbr',
                             'codehilite',
                             'fenced_code',
                             'sane_lists',
                             'smart_strong']))
