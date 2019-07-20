import datetime

from django.db import models
from django.urls import reverse

from . import managers


class License(models.Model):
    """
    A license in use for a project.

    This model is related through Version instead of directly on
    Project, in order to support re-licensing the project with a new
    version.

    """
    name = models.CharField(max_length=255,
                            unique=True)
    slug = models.SlugField(unique=True)
    link = models.URLField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    A software project.

    """
    HIDDEN_STATUS = 0
    PUBLIC_STATUS = 1
    STATUS_CHOICES = (
        (HIDDEN_STATUS, 'Hidden'),
        (PUBLIC_STATUS, 'Public'),
    )

    name = models.CharField(max_length=255,
                            unique=True)
    slug = models.SlugField(unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=PUBLIC_STATUS)
    description = models.TextField()

    package_link = models.URLField(
        blank=True, null=True,
        help_text="URL of the project's package(s)"
    )
    repository_link = models.URLField(
        blank=True, null=True,
        help_text="URL of the project's repostory"
    )
    documentation_link = models.URLField(
        blank=True, null=True,
        help_text="URL of the project's documentation"
    )
    tests_link = models.URLField(
        blank=True, null=True,
        help_text="URL of the project's tests/continuous integration"
    )

    objects = managers.ProjectQuerySet.as_manager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'projects:detail',
            kwargs={'slug': self.slug}
        )

    def latest_version(self):
        latest = self.versions.filter(is_latest=True)
        if latest:
            return latest[0]
        return None


class Version(models.Model):
    """
    A version of a software project.

    """
    PLANNING_STATUS = 1
    PRE_ALPHA_STATUS = 2
    ALPHA_STATUS = 3
    BETA_STATUS = 4
    STABLE_STATUS = 5

    STATUS_CHOICES = (
        (PLANNING_STATUS, 'Planning'),
        (PRE_ALPHA_STATUS, 'Pre-Alpha'),
        (ALPHA_STATUS, 'Alpha'),
        (BETA_STATUS, 'Beta'),
        (STABLE_STATUS, 'Stable'),
    )

    project = models.ForeignKey(
        Project,
        related_name='versions',
        on_delete=models.CASCADE
    )
    version = models.CharField(max_length=255)
    is_latest = models.BooleanField(default=False)

    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=STABLE_STATUS)
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE
    )
    release_date = models.DateField(default=datetime.date.today)

    objects = managers.VersionManager()

    class Meta:
        ordering = ('project', 'version')
        unique_together = ('project', 'version')

    def __str__(self):
        return "%s %s" % (self.project, self.version)

    def get_absolute_url(self):
        return reverse(
            'projects_version_detail',
            kwargs={
                'project_slug': self.project.slug,
                'slug': self.version
            }
        )
