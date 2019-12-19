from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


def current_site(request: HttpRequest) -> dict:
    """
    Context processor returning the current site object.

    """
    return {
        "protocol": "https" if request.is_secure() else "http",
        "site": get_current_site(request),
    }
