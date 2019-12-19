from django.contrib import admin
from django.db import models
from django.http import HttpRequest

from .models import Category, Entry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Metadata", {"fields": ("title", "slug")}),
        (None, {"fields": ("description",)}),
    )

    list_display = ("title", "slug", "num_live_entries")
    list_display_links = ("title", "slug")

    prepopulated_fields = {"slug": ("title",)}

    def num_live_entries(self, obj: Category) -> int:
        return obj.live_entries.count()

    num_live_entries.short_description = "Live entries"


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"

    fieldsets = (
        ("Metadata", {"fields": ("author", "pub_date", "title", "slug", "status")}),
        (None, {"fields": ("excerpt", "body")}),
        (None, {"fields": ("categories",)}),
    )

    filter_horizontal = ("categories",)
    list_display = ("title", "pub_date", "status")
    list_display_links = ("title",)
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)

    def get_queryset(self, request: HttpRequest) -> models.QuerySet:
        # Default manager only returns live entries; we want them all.
        return Entry.objects.all()
