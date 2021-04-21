from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import AsignacionLog
from .models import AsignacionAsistenteLog
from .models import Asignacion, AsignacionExtra, AsignacionNoAula
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
        old = Periodo.objects.get(pk=instance.pk)
        if old.jec != instance.jec:
            for aa in instance.asignatura_set.filter(base__isnull=False):
                if instance.jec:
                    aa.horas = aa.base.horas_jec
                else:
                    aa.horas = aa.base.horas_nec
                aa.save()
        

@receiver(pre_delete, sender=Periodo)
def cleanup_after_periodo_delete(sender, instance, using, **kwargs):
    instance.asignatura_set.all().delete()

@receiver(pre_delete, sender=AsignaturaBase)
def cleanup_after_asignaturabase_delete(sender, instance, using, **kwargs):
    instance.asignatura_set.all().delete()

@receiver(pre_delete, sender=Asignatura)
def cleanup_after_asignatura_delete(sender, instance, using, **kwargs):
    instance.asignacion_set.all().delete()


# Asignacion*Log
@receiver(post_save, sender=Asignacion)
def record_asignacion_log(sender, instance, created, **kwargs):
    if created:
        AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"asignó {instance}", usuario=instance.last_edited_by)
    else:
        AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"modificó {instance}", usuario=instance.last_edited_by)

@receiver(pre_delete, sender=Asignacion)
def record_asignacion_delete_log(sender, instance, using, **kwargs):
    AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"quitó {instance}", usuario=instance.last_edited_by)

@receiver(post_save, sender=AsignacionExtra)
def record_asignacion_extra_log(sender, instance, created, **kwargs):
    if created:
        AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"asignó {instance}", usuario=instance.last_edited_by)
    else:
        AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"modificó {instance}", usuario=instance.last_edited_by)

@receiver(pre_delete, sender=AsignacionExtra)
def record_asignacion_extra_delete_log(sender, instance, using, **kwargs):
    AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"quitó {instance}", usuario=instance.last_edited_by)

@receiver(post_save, sender=AsignacionNoAula)
def record_asignacion_no_aula_log(sender, instance, created, **kwargs):
    if created:
        AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"asignó {instance}", usuario=instance.last_edited_by)
    else:
        AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"modificó {instance}", usuario=instance.last_edited_by)

@receiver(pre_delete, sender=AsignacionNoAula)
def record_asignacion_no_aula_delete_log(sender, instance, using, **kwargs):
    AsignacionLog.objects.create(profesor=instance.profesor, mensaje=f"quitó {instance}", usuario=instance.last_edited_by)
