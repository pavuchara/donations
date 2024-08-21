from django.apps import AppConfig


class CollectiveDonationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.collective_donations'
    verbose_name = 'Коллективные пожертвования'

    def ready(self) -> None:
        from . import signals
