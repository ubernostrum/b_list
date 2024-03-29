from markdown import markdown
from typogrify.filters import typogrify


def markup(text: str) -> str:
    """
    Mark up plain text into fancy HTML.

    """
    return typogrify(
        markdown(
            text,
            output_format="html5",
            extensions=[
                "abbr",
                "codehilite",
                "fenced_code",
                "sane_lists",
                "md_in_html",
            ],
        )
    )
