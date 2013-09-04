"""
Root URLConf.

"""

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from django.contrib import admin

from blog.views import EntryArchiveIndex
from flashpolicies.views import no_access

# Redirect views which prevent an older URL scheme from 404'ing.
from .views import gone
from .views import redirect_entry_day
from .views import redirect_entry_detail
from .views import redirect_media
from .views import redirect_entry_month


admin.autodiscover()


urls = patterns('',
                url(r'^admin/', include(admin.site.urls)),
                url(r'^browserid/', include('django_browserid.urls')),
                url(r'^$',
                    EntryArchiveIndex.as_view(
                        template_name='home.html',
                        ),
                    name='home'),
                url(r'^contact/', include('contact_form.urls')),
                url(r'^feeds/', include('blog.urls.feeds')),
                url(r'^weblog/categories/', include('blog.urls.categories')),
                url(r'^weblog/', include('blog.urls.entries')),
                url(r'^crossdomain.xml$', no_access),
)


legacy = patterns('',
                  url(r'^links/', gone),
                  url(r'^weblog/(?P<year>\d{4})/(?P<month>\d{2})/$',
                      redirect_entry_month),
                  url(r'^weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
                      redirect_entry_day),
                  url(r'^weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                      redirect_entry_detail),
                  url(r'^media/(?P<path>.*)$', redirect_media),
)


# The redirecting patterns come first; otherwise, the main URLs would
# catch those and 404.
urlpatterns = legacy + urls
