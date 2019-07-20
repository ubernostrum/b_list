# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('description_html', models.TextField(editable=False, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('pub_date', models.DateTimeField(verbose_name='Date posted', default=datetime.datetime.now)),
                ('slug', models.SlugField(unique_for_date='pub_date')),
                ('status', models.IntegerField(choices=[(1, 'Live'), (2, 'Draft'), (3, 'Hidden')], default=1)),
                ('title', models.CharField(max_length=250)),
                ('body', models.TextField()),
                ('body_html', models.TextField(editable=False, blank=True)),
                ('excerpt', models.TextField(null=True, blank=True)),
                ('excerpt_html', models.TextField(null=True, editable=False, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='blog.Category')),
            ],
            options={
                'verbose_name_plural': 'Entries',
                'ordering': ('-pub_date',),
                'get_latest_by': 'pub_date',
            },
        ),
    ]
