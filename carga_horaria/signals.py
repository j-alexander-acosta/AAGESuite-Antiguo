from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Periodo
from .models import Asignatura, AsignaturaBase


@receiver(post_save, sender=Periodo)
def create_asignaturas(sender, instance, **kwargs):
    colegio = instance.colegio
    for ab in instance.plan.asignaturabase_set.all():
        if colegio.jec:
            horas = ab.horas_jec
        else:
            horas = ab.horas_nec
        Asignatura.objects.create(base=ab,
                                  periodo=instance,
                                  horas=horas)

