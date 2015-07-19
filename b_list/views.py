"""
Views which handle an older URL scheme and now-nonexistent
functionality.

"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.generic.base import RedirectView


MONTH_DICT = {'01': 'jan',
              '02': 'feb',
              '03': 'mar',
              '04': 'apr',
              '05': 'may',
              '06': 'jun',
              '07': 'jul',
              '08': 'aug',
              '09': 'sep',
              '10': 'oct',
              '11': 'nov',
              '12': 'dec'}


class EntryDetailRedirect(RedirectView):
    permanent = True
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'blog_entry_detail',
            kwargs={'year': kwargs['year'],
                    'month': MONTH_DICT[kwargs['month']],
                    'day': kwargs['day'],
                    'slug': kwargs['slug']}
        )
                    

class EntryDayRedirect(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'blog_entry_archive_day',
            kwargs={'year': kwargs['year'],
                    'month': MONTH_DICT[kwargs['month']],
                    'day': kwargs['day']}
        )


class EntryMonthRedirect(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'blog_entry_archive_month',
            kwargs={'year': kwargs['year'],
                    'month': MONTH_DICT[kwargs['month']]}
        )


class MediaRedirect(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return '%s%s' % (settings.MEDIA_URL, kwargs['path'])


def gone(request, *args, **kwargs):
    return TemplateResponse(request,
                            '410.html',
                            status=410)
