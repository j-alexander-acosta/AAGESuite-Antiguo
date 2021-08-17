from django.apps import AppConfig


class CargaHorariaConfig(AppConfig):
    name = 'carga_horaria'
    verbose_name = 'Carga Horaria'

    def ready(self):
        from . import signals
