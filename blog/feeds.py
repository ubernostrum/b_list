from django.utils.feedgenerator import Atom1Feed

from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed

from .models import Category
from .models import Entry


current_site = Site.objects.get_current()


class EntriesFeed(Feed):
    author_name = "James Bennett"
    copyright = "https://{}/about/copyright/".format(current_site.domain)
    description = "Latest entriess"
    feed_type = Atom1Feed
    item_copyright = "https://{}/about/copyright/".format(current_site.domain)
    item_author_name = "James Bennett"
    item_author_link = "https://{}/".format(current_site.domain)
    feed_url = "https://{}/feeds/entries/".format(current_site.domain)
    link = "https://{}/".format(current_site.domain)
    title = "James Bennett (b-list.org)"

    description_template = 'feeds/entry_description.html'
    title_template = 'feeds/entry_title.html'

    def item_categories(self, item):
        return [c.title for c in item.categories.all()]

    def item_guid(self, item):
        return "tag:{},{}:{}".format(
            current_site.domain,
            item.pub_date.strftime('%Y-%m-%d'),
            item.get_absolute_url()
    )

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.updated_date

    def items(self):
        return Entry.live.all()[:15]

    def item_link(self, item):
        return "https://{}{}".format(
            current_site.domain,
            item.get_absolute_url()
        )


class CategoryFeed(EntriesFeed):
    def feed_url(self, obj):
        return "https://{}/feeds/categories/{}/".format(
            current_site.domain, obj.slug
        )

    def description(self, obj):
        return "Latest entries in category '{}'".format(
            obj.title
        )

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def items(self, obj):
        return obj.live_entries[:15]

    def link(self, obj):
        return self.item_link(obj)

    def title(self, obj):
        return "Latest entries in category '{}'".format(
            obj.title
        )
