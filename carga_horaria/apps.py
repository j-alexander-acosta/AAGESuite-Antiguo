from django.apps import AppConfig


class CargaHorariaConfig(AppConfig):
    name = 'carga_horaria'

    def ready(self):
        from . import signals
