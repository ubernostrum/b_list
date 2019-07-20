# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id',
                 models.AutoField(
                     primary_key=True,
                     auto_created=True,
                     serialize=False,
                     verbose_name='ID')),
                ('name',
                 models.CharField(
                     max_length=255,
                     unique=True)),
                ('slug',
                 models.SlugField(unique=True)),
                ('link',
                 models.URLField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id',
                 models.AutoField(
                     primary_key=True,
                     auto_created=True,
                     serialize=False,
                     verbose_name='ID')),
                ('name',
                 models.CharField(
                     max_length=255,
                     unique=True)),
                ('slug',
                 models.SlugField(unique=True)),
                ('status',
                 models.IntegerField(
                     choices=[
                         (0, 'Hidden'),
                         (1, 'Public')],
                     default=1)),
                ('description',
                 models.TextField()),
                ('package_link',
                 models.URLField(
                     blank=True,
                     help_text="URL of the project's package(s)",
                     null=True)),
                ('repository_link',
                 models.URLField(
                     blank=True,
                     help_text="URL of the project's repostory",
                     null=True)),
                ('documentation_link',
                 models.URLField(
                     blank=True,
                     help_text="URL of the project's documentation",
                     null=True)),
                ('tests_link',
                 models.URLField(
                     blank=True,
                     help_text=("URL of the project's tests/continuous "
                                "integration"),
                     null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id',
                 models.AutoField(
                     primary_key=True,
                     auto_created=True,
                     serialize=False,
                     verbose_name='ID')),
                ('version',
                 models.CharField(max_length=255)),
                ('is_latest',
                 models.BooleanField(default=False)),
                ('status',
                 models.IntegerField(
                     choices=[
                         (1, 'Planning'),
                         (2, 'Pre-Alpha'),
                         (3, 'Alpha'),
                         (4, 'Beta'),
                         (5, 'Stable')],
                     default=5)),
                ('release_date',
                 models.DateField(default=datetime.date.today)),
                ('license',
                 models.ForeignKey(to='projects.License')),
                ('project',
                 models.ForeignKey(
                     related_name='versions',
                     to='projects.Project')),
            ],
            options={
                'ordering': ('project', 'version'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('project', 'version')]),
        ),
    ]
