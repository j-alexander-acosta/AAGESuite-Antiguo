from enum import Enum
from django.db import models


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
    nivel = models.CharField(max_length=8, choices=[(tag, tag.value) for tag in Nivel])


class AsignaturaBase(models.Model):
    nombre = models.CharField(max_length=255)
    plan = models.ForeignKey('Plan')
    horas_jec = models.PositiveSmallIntegerField()
    horas_nec = models.PositiveSmallIntegerField()


class Colegio(models.Model):
    nombre = models.CharField(max_length=255)
    jec = models.BooleanField(default=True)
    

class Periodo(models.Model):
    nombre = models.CharField(max_length=255)
    colegio = models.ForeignKey('Colegio')
    plan = models.ForeignKey('Plan')


class Asignatura(models.Model):
    base = models.ForeignKey('AsignaturaBase')
    periodo = models.ForeignKey('Periodo')
    horas = models.PositiveSmallIntegerField()


class Curso(models.Model):
    periodo = models.ForeignKey('Periodo')
    letra = models.CharField(max_length=1)


class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    horas = models.PositiveSmallIntegerField()


class Asignacion(models.Model):
    profesor = models.ForeignKey('Profesor')
    asignatura = models.ForeignKey('Asignatura')
    horas = models.PositiveSmallIntegerField()
