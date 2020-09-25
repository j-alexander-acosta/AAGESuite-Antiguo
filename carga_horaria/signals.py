from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Periodo
from .models import Asignatura, AsignaturaBase


@receiver(post_save, sender=Periodo)
def horas_asignaturas(sender, instance, created, **kwargs):
    if created:
        for ab in instance.plan.asignaturabase_set.all():
            if instance.jec:
                horas = ab.horas_jec
            else:
                horas = ab.horas_nec
            aa = Asignatura.objects.create(base=ab,
                                           horas=horas)
            aa.periodos.add(instance)


@receiver(pre_save, sender=Periodo)
def horas_asignaturas_jec(sender, instance, **kwargs):
    if instance.pk is None:
        pass
    else:
        for aa in instance.asignatura_set.filter(base__isnull=False):
            if instance.jec:
                aa.horas = aa.base.horas_jec
            else:
                aa.horas = aa.base.horas_nec
            aa.save()
        
