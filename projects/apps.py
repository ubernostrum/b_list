from django.apps import AppConfig
from django.db.models.signals import post_save


class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        """
        Register the signal handler which ensures only one Version of
        a Project at a time can have is_latest=True.

        """
        Version = self.get_model('Version')
        post_save.connect(
            Version.objects.update_latest,
            sender=Version,
            dispatch_uid="projects_version_latest_toggle"
        )
