from enum import Enum
from django.db import models
from django.urls import reverse


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
    nombre = models.CharField(max_length=255)
    nivel = models.CharField(max_length=8, choices=[(tag.name, tag.value) for tag in Nivel])

    def __str__(self): 
        return self.nombre

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
    horas_jec = models.PositiveSmallIntegerField()
    horas_nec = models.PositiveSmallIntegerField()

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
    nombre = models.CharField(max_length=255)
    colegio = models.ForeignKey('Colegio')
    plan = models.ForeignKey('Plan')

    def __str__(self): 
        return self.nombre

    class Meta:
        verbose_name = u"Periodo"
        verbose_name_plural = u"Periodos"
    
    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del período
        :return: url
        """
        return reverse('carga-horaria:periodo', args=[str(self.pk)])



class Asignatura(models.Model):
    base = models.ForeignKey('AsignaturaBase')
    periodo = models.ForeignKey('Periodo')
    horas = models.PositiveSmallIntegerField()

    def __str__(self): 
        return self.base

class Curso(models.Model):
    periodo = models.ForeignKey('Periodo')
    letra = models.CharField(max_length=1)

    def __str__(self): 
        return self.letra

class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    horas = models.PositiveSmallIntegerField()

    def __str__(self): 
        return self.nombre


class Asignacion(models.Model):
    profesor = models.ForeignKey('Profesor')
    asignatura = models.ForeignKey('Asignatura')
    horas = models.PositiveSmallIntegerField()

    def __str__(self): 
        return self.profesor
