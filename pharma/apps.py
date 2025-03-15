from django.apps import AppConfig


class PharmaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharma'

    def ready(self):
        import pharma.signals  # Import signals when app is ready
