import datetime
import typing

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

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    link = models.URLField()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    """
    A software project.

    """

    class Status(models.IntegerChoices):
        """
        Enum representing possible values for a project's
        publication status.

        """

        HIDDEN = 0, "Hidden"
        PUBLIC = 1, "Public"

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PUBLIC)
    description = models.TextField()

    package_link = models.URLField(
        blank=True, null=True, help_text="URL of the project's package(s)"
    )
    repository_link = models.URLField(
        blank=True, null=True, help_text="URL of the project's repostory"
    )
    documentation_link = models.URLField(
        blank=True, null=True, help_text="URL of the project's documentation"
    )
    tests_link = models.URLField(
        blank=True,
        null=True,
        help_text="URL of the project's tests/continuous integration",
    )

    objects = managers.ProjectQuerySet.as_manager()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def latest_version(self) -> typing.Optional[int]:
        latest = self.versions.filter(is_latest=True)
        if latest:
            return latest[0]
        return None


class Version(models.Model):
    """
    A version of a software project.

    """

    class Stability(models.IntegerChoices):
        """
        Enum representing possible values for the stability of a
        version.

        """

        PLANNING = 1, "Planning"
        PRE_ALPHA = 2, "Pre-Alpha"
        ALPHA = 3, "Alpha"
        BETA = 4, "Beta"
        STABLE = 5, "Stable"

    project = models.ForeignKey(
        Project, related_name="versions", on_delete=models.CASCADE
    )
    version = models.CharField(max_length=255)
    is_latest = models.BooleanField(default=False)

    status = models.IntegerField(choices=Stability.choices, default=Stability.STABLE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    release_date = models.DateField(default=datetime.date.today)

    objects = managers.VersionManager()

    class Meta:
        ordering = ("project", "version")
        unique_together = ("project", "version")

    def __str__(self) -> str:
        return "%s %s" % (self.project, self.version)

    def get_absolute_url(self) -> str:
        return reverse(
            "projects_version_detail",
            kwargs={"project_slug": self.project.slug, "slug": self.version},
        )
