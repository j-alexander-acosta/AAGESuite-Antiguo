from enum import Enum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_DOWN


class Nivel(Enum):
    PK = "Pre kinder"
    K = "Kinder"
    B1 = "Primero básico"
    B2 = "Segundo básico"
    B3 = "Tercero básico"
    B4 = "Cuarto básico"
    B5 = "Quinto básico"
    B6 = "Sexto básico"
    B7 = "Séptimo básico"
    B8 = "Octavo básico"
    M1 = "Primero medio"
    M2 = "Segundo medio"
    M3 = "Tercero medio"
    M4 = "Cuarto medio"


class Plan(models.Model):
    nivel = models.CharField(max_length=8, choices=[(tag.name, tag.value) for tag in Nivel])

    def __str__(self): 
        return "Plan de Estudios - {} (ID: {})".format(getattr(Nivel, self.nivel).value.title(), self.pk)

    class Meta:
        verbose_name = u"Plan"
        verbose_name_plural = u"Planes"

    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del plan
        :return: url
        """
        return reverse('carga-horaria:plan', args=[str(self.pk)])


class AsignaturaBase(models.Model):
    nombre = models.CharField(max_length=255)
    plan = models.ForeignKey('Plan')
    horas_jec = models.DecimalField(max_digits=3, decimal_places=1)
    horas_nec = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self): 
        return self.nombre

class Colegio(models.Model):
    nombre = models.CharField(max_length=255)
    jec = models.BooleanField(default=True)
    
    def __str__(self): 
        return self.nombre

    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del colegio
        :return: url
        """
        return reverse('carga-horaria:colegio', args=[str(self.pk)])

class Periodo(models.Model):
    plan = models.ForeignKey('Plan')
    nombre = models.CharField(max_length=255, blank=True, null=True)
    horas = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    horas_dif = models.DecimalField(max_digits=3, decimal_places=1, default=0, validators=[MinValueValidator(0), MaxValueValidator(9)])
    colegio = models.ForeignKey('Colegio')

    @property
    def floor(self):
        if self.colegio.jec:
            lookup = 'base__horas_jec'
        else:
            lookup = 'base__horas_nec'
        return sum(filter(None, self.asignatura_set.values_list(lookup, flat=True)))

    @property
    def ceiling(self):
        if self.colegio.jec:
            return self.floor + self.horas_dif + self.horas
        else:
            return self.floor + self.horas_dif

    @property
    def capacity(self):
        return sum(self.asignatura_set.values_list('horas', flat=True))

    @property
    def available(self):
        return self.ceiling - self.capacity

    @property
    def progress(self):
        return sum(Asignacion.objects.filter(asignatura__in=self.asignatura_set.all()).values_list('horas', flat=True))

    @property
    def completion_percentage(self):
        return round(self.progress * 100 / self.ceiling)

    def __str__(self): 
        return "{} {}".format(getattr(Nivel, self.plan.nivel).value.title(), str(self.nombre or '')).strip()

    class Meta:
        verbose_name = u"Curso"
        verbose_name_plural = u"Cursos"
    
    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del período
        :return: url
        """
        return reverse('carga-horaria:periodo', args=[str(self.pk)])


class Asignatura(models.Model):
    base = models.ForeignKey('AsignaturaBase', null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    periodo = models.ForeignKey('Periodo')
    horas = models.DecimalField(max_digits=3, decimal_places=1)

    @property
    def horas_asignadas(self):
        return sum(self.asignacion_set.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return self.horas - self.horas_asignadas

    @property
    def completa(self):
        return self.horas_asignadas >= self.horas

    @property
    def profesores(self):
        return {ax.profesor for ax in self.asignacion_set.all()}

    def __str__(self): 
        return str(self.base or self.nombre)


class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    horas = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(44)])
    especialidad = models.ForeignKey('Especialidad', blank=True, null=True)

    @property
    def horas_asignadas(self):
        return sum(self.asignacion_set.values_list('horas', flat=True)) + sum(self.asignacionextra_set.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return self.horas_docentes - self.horas_asignadas

    @property
    def horas_docentes(self):
        # considerar luego 60/40 colegios vulnerables
        return Decimal(self.horas * Decimal(60.0)/Decimal(45.0) * Decimal(.65)).quantize(Decimal(0), rounding=ROUND_HALF_DOWN)

    def __str__(self): 
        return self.nombre


class Asignacion(models.Model):
    profesor = models.ForeignKey('Profesor')
    asignatura = models.ForeignKey('Asignatura')
    horas = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self): 
        return "{} - {} ({})".format(self.profesor, self.asignatura, self.horas)


class AsignacionExtra(models.Model):
    profesor = models.ForeignKey('Profesor')
    curso = models.ForeignKey('Periodo', null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    horas = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self): 
        return "{} - {} ({})".format(self.profesor, self.descripcion, self.horas)


class Especialidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
