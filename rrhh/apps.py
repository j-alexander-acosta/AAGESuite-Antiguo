from django.apps import AppConfig


class RrhhConfig(AppConfig):
    name = 'recursos_humanos'

    def ready(self):
        from . import signals
