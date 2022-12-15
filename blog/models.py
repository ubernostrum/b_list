import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse

from .markup import markup


class LiveEntryManager(models.Manager):
    """
    Manager which will only fetch live entries.

    """

    def get_queryset(self) -> models.QuerySet:
        return (
            super(LiveEntryManager, self)
            .get_queryset()
            .filter(status=self.model.Status.LIVE)
        )


class Entry(models.Model):
    """
    An entry in the blog.

    """

    class Status(models.IntegerChoices):
        """
        Enum reprsenting possible values for an entry's
        publication status.

        """

        LIVE = 1, "Live"
        DRAFT = 2, "Draft"
        HIDDEN = 3, "Hidden"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("Date posted", default=datetime.datetime.now)
    updated_date = models.DateTimeField(blank=True, editable=False)
    slug = models.SlugField(unique_for_date="pub_date")
    status = models.IntegerField(choices=Status.choices, default=Status.LIVE)
    title = models.CharField(max_length=250)

    body = models.TextField()
    body_html = models.TextField(editable=False, blank=True)

    excerpt = models.TextField(blank=True, null=True)
    excerpt_html = models.TextField(editable=False, blank=True, null=True)

    categories = models.ManyToManyField("Category")

    live = LiveEntryManager()
    objects = models.Manager()

    class Meta:
        get_latest_by = "pub_date"
        ordering = ("-pub_date",)
        verbose_name_plural = "Entries"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = markup(self.body)
        if self.excerpt:
            self.excerpt_html = markup(self.excerpt)
        self.updated_date = datetime.datetime.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse(
            "entries:entry",
            kwargs={
                "year": self.pub_date.strftime("%Y"),
                "month": self.pub_date.strftime("%b").lower(),
                "day": self.pub_date.strftime("%d"),
                "slug": self.slug,
            },
        )


class Category(models.Model):
    """
    A category into which entries can be filed.

    """

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse(
            "categories:category", kwargs={"slug": self.slug}, current_app="blog"
        )

    def _get_live_entries(self) -> models.QuerySet:
        return self.entry_set.filter(status=Entry.Status.LIVE)

    live_entries = property(_get_live_entries)
