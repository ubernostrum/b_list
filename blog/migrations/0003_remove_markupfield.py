# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# This migration and the preceding one have been edited to be no-ops;
# previously, they set up django-markupfield's MarkupField for several
# fields on the blog models, then returned those fields to their
# original TextField definitions once I decided not to use
# MarkupField. Preserving these migrations as they originally were
# would require maintaining a dependency on django-markupfield (to
# make MarkupField importable for these migrations) despite it no
# longer being used.
class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_markupfield'),
    ]

    operations = [
        migrations.RunPython(
            migrations.RunPython.noop,
            migrations.RunPython.noop
        )
    ]
