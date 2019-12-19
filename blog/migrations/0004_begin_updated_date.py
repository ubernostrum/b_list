# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-26 03:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [("blog", "0003_remove_markupfield")]

    operations = [
        migrations.AlterModelManagers(
            name="entry", managers=[("live", django.db.models.manager.Manager())]
        ),
        migrations.AddField(
            model_name="entry",
            name="updated_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
