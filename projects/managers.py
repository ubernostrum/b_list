from django.db import models


class ProjectQuerySet(models.QuerySet):
    """
    Custom QuerySet for the Project model, enabling an easy query for
    live Projects.

    """

    def public(self) -> models.QuerySet:
        """
        Return only Projects with 'public' status.

        """
        return self.filter(status=self.model.Status.PUBLIC)


class VersionQuerySet(models.QuerySet):
    """
    Custom QuerySet for the Version model, enabling an easy query for
    stable Versions.

    """

    def stable(self) -> models.QuerySet:
        """
        Return only Versions with 'stable' status.

        """
        return self.filter(status=self.model.Stability.STABLE)


class VersionManager(models.Manager):
    """
    Custom manager for the Version model, making use of
    VersionQuerySet.

    """

    # We write a full Manager instead of using
    # VersionQuerySet.as_manager() in order to set
    # use_for_related_fields and ensure that queries from the related
    # Project will use VersionQuerySet.
    use_for_related_fields = True

    def get_queryset(self) -> models.QuerySet:
        return VersionQuerySet(self.model)

    def stable(self) -> models.QuerySet:
        return self.get_queryset().stable()

    def update_latest(self, sender: type, instance: models.Model, **kwargs):
        """
        Signal handler which ensures that when a Version is saved with
        is_latest=True, all other Versions for that Project are
        toggled to is_latest=False.

        """
        if not instance.is_latest:
            return
        self.filter(project__id=instance.project.id, is_latest=True).exclude(
            pk=instance.id
        ).update(is_latest=False)
