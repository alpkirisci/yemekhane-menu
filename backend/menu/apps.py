from django.apps import AppConfig
from django.core.signals import request_finished


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'

    def ready(self):
        """Signals.py configuration."""
        # See, https://docs.djangoproject.com/en/4.2/topics/signals/ .
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals

        # Explicitly connect a signal handler.
        # request_finished.connect(signals.my_callback)