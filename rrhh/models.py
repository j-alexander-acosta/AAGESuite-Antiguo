from django.db import models


class Funcionario(models.Model):
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=16)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    fecha_ingreso = models.DateField(verbose_name='Fecha ingreso SEA')
    titulo = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    estado_civil = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=255)
    sexo = models.CharField(max_length=255)
    email = models.EmailField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    # añadir listado de archivos

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Funcionario'
        verbose_name_plural = u'Funcionarios'


class Entrevista(models.Model):
    FELICITACIONES = 1
    RECOMENDACIONES = 2

    TIPO_CHOICES = ((FELICITACIONES, 'Felicitaciones'),
                    (RECOMENDACIONES, 'Recomendaciones'))

    funcionario = models.ForeignKey('Funcionario')
    entrevistador = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=FELICITACIONES, choices=TIPO_CHOICES)
    contenido = models.TextField()
    acuerdos = models.TextField()
    # añadir fecha
    

class Archivo(models.Model):
    descripcion = models.CharField(max_length=255)
    archivo = models.FileField()
    funcionario = models.ForeignKey('Funcionario')
