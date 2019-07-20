from django.contrib import admin

from .models import License, Project, Version


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


class VersionInline(admin.StackedInline):
    fields = (
        'version', 'status', 'release_date',
        'is_latest', 'license'
    )
    model = Version


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {
            'fields': ('name', 'slug', 'status'),
        }),
        ('Project information', {
            'fields': ('description', 'package_link',
                       'repository_link', 'documentation_link',
                       'tests_link'),
        }),
    )
    inlines = [
        VersionInline,
    ]
    list_display = ('name', 'status', 'latest_version')
    list_filter = ('status',)
    prepopulated_fields = {
        'slug': ('name',),
    }

    def latest_version(self, obj):
        return obj.latest_version().version
    latest_version.short_description = 'Latest version'
