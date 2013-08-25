"""
Views which handle an older URL scheme and now-nonexistent
functionality.

"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.template.response import TemplateResponse


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


def redirect_entry_detail(request, year, month, day, slug):
    return HttpResponsePermanentRedirect(reverse('blog_entry_detail',
                                                 kwargs={'year': year,
                                                         'month': MONTH_DICT[month],
                                                         'day': day,
                                                         'slug': slug}))


def redirect_entry_day(request, year, month, day):
    return HttpResponsePermanentRedirect(reverse('blog_entry_archive_day',
                                                 kwargs={'year': year,
                                                         'month': MONTH_DICT[month],
                                                         'day': day}))


def redirect_entry_month(request, year, month):
    return HttpResponsePermanentRedirect(reverse('blog_entry_archive_month',
                                                 kwargs={'year': year,
                                                         'month': MONTH_DICT[month]}))

def redirect_media(request, path):
    return HttpResponsePermanentRedirect('%s%s' % (settings.MEDIA_URL, path))


def gone(request, *args, **kwargs):
    return TemplateResponse(request,
                            '410.html',
                            status=410)
