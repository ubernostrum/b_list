"""
Root URLconf.

"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django_contact_form.forms import AkismetContactForm
from django_contact_form.views import ContactFormView
from flashpolicies.views import no_access

from blog.views import EntryArchiveIndex

# Redirect views which prevent an older URL scheme from 404'ing.
from . import views


urls = [
    path("admin/", admin.site.urls),
    path("", EntryArchiveIndex.as_view(template_name="home.html"), name="home"),
    path(
        "contact/",
        ContactFormView.as_view(form_class=AkismetContactForm),
        name="contact_form",
    ),
    path(
        "contact/sent/",
        TemplateView.as_view(
            template_name="django_contact_form/contact_form_sent.html"
        ),
        name="contact_form_sent",
    ),
    path("projects/", include("projects.urls")),
    path("feeds/", include("blog.urls.feeds", namespace="feeds")),
    path("weblog/categories/", include("blog.urls.categories", namespace="categories")),
    path("weblog/", include("blog.urls.entries", namespace="entries")),
    path("crossdomain.xml", no_access),
]


legacy = [
    path("links/", views.gone),
    re_path(
        r"^weblog/(?P<year>\d{4})/(?P<month>\d{2})/$",
        views.EntryMonthRedirect.as_view(),
    ),
    re_path(
        r"^weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$",
        views.EntryDayRedirect.as_view(),
    ),
    re_path(
        r"^weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$",
        views.EntryDetailRedirect.as_view(),
    ),
    path("media/<path:path>", views.MediaRedirect.as_view()),
]


# The redirecting patterns come first; otherwise, the main URLs would
# catch those and 404.
urlpatterns = legacy + urls
