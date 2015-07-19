"""
Root URLconf.

"""

from django.conf.urls import include
from django.conf.urls import url

from django.contrib import admin

from blog.views import EntryArchiveIndex
from flashpolicies.views import no_access

# Redirect views which prevent an older URL scheme from 404'ing.
from . import views


urls = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        EntryArchiveIndex.as_view(
            template_name='home.html',
            ),
        name='home'),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^feeds/', include('blog.urls.feeds')),
    url(r'^projects/', include('projects.urls')),
    url(r'^weblog/categories/', include('blog.urls.categories')),
    url(r'^weblog/', include('blog.urls.entries')),
    url(r'^crossdomain.xml$', no_access),
]


legacy = [
    url(r'^links/', views.gone),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.EntryMonthRedirect.as_view()),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.EntryDayRedirect.as_view()),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.EntryDetailRedirect.as_view()),
    url(r'^media/(?P<path>.*)$', views.MediaRedirect.as_view()),
]


# The redirecting patterns come first; otherwise, the main URLs would
# catch those and 404.
urlpatterns = legacy + urls
