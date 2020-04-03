from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    """
        Clase base para los demás modelos registrados
        en la aplicación.
        Contiene los campos de fecha y usuario de creación y fecha y usuario de modificacion
        necesarios para cada modelo.
    """
    creado_en = models.DateTimeField(
        auto_now_add=True
    )
    modificado_en = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Union(TimeStampModel):
    """
       Modelo de descripcion de la Union
    """
    nombre = models.CharField(
        max_length=250
    )

    def __str__(self):
        return u"{}".format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Union'
        verbose_name_plural = u'Uniones'


class Fundacion(TimeStampModel):
    """
        Modelo de descripción del Fundación
    """
    nombre = models.CharField(
        max_length=250
    )
    union = models.ForeignKey(
        "Union",
        on_delete=models.CASCADE
    )
    asesores = models.ManyToManyField(
        "recursos_humanos.FuncionarioFundacion",
        related_name="+"
    )

    def __str__(self):
        return u"{}".format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Fundación'
        verbose_name_plural = u'Fundaciones'


tipos_jornada = {
    ('completa', 'Jornada Completa'),
    ('media', 'Media Jornada'),
}

tipos_estados = {
    ('particular', 'Particular'),
    ('particular_subvencionado', 'Particular Subvencionado'),
    ('gratuito', 'Gratuito'),
}


class Colegio(TimeStampModel):
    """
        Modelo de descripcion del colegio
    """
    nombre = models.CharField(
        max_length=250
    )
    abrev = models.CharField(
        max_length=50,
        verbose_name="Abreviación"
    )
    fundacion = models.ForeignKey(
        "Fundacion",
        on_delete=models.CASCADE
    )
    rbd = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Rol de base de datos (RBD)"
    )
    estado = models.CharField(
        max_length=25,
        default='particular_subvencionado',
        choices=tipos_estados
    )
    tipo_jornada = models.CharField(
        max_length=25,
        default='completa',
        choices=tipos_jornada
    )
    total_salas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total de salas"
    )
    capacidad_promedio_salas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Capacidad promedio de las salas"
    )
    total_matricula_ultimo_anio = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total de matricula el último año"
    )
    total_profesores_aula = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total de profesores de aula"
    )
    total_profesionales_educacion = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total de profesionales de la educación"
    )
    total_asistentes_educacion = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total de asistentes de la educación"
    )
    total_alumnos_pie = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total de alumnos en PIE"
    )
    indice_vulnerabilidad = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="Índice de vulnerabilidad"
    )

    def __str__(self):
        return u"{} @ {}".format(
            self.nombre,
            self.abrev
        )

    class Meta:
        verbose_name = u'Colegio'
        verbose_name_plural = u'Colegios'


class ExcelenciaAcademica(TimeStampModel):
    """
        Modelo para registrar si el colegio consiguió excelencia académica en un año específico
    """
    colegio = models.ForeignKey(
        "Colegio",
        on_delete=models.CASCADE
    )
    detalle = models.TextField(
        max_length=2500
    )
    anio = models.PositiveIntegerField(
        verbose_name="Año"
    )

    def __str__(self):
        return u"{} - {}".format(
            self.colegio.abrev,
            self.anio
        )

    class Meta:
        verbose_name = u'Excelencia Académica'
        verbose_name_plural = u'Excelencias Académicas'


class Periodo(TimeStampModel):
    """
        Modelo para el control de periodos
        (este contendra la estructura de curso de carga horaria y ciclos de calidad)
    """
    nombre = models.CharField(
        max_length=250,
    )
    colegio = models.ForeignKey(
        "Colegio",
        on_delete=models.CASCADE
    )
    anio = models.PositiveIntegerField(
        verbose_name="Año"
    )
    activo = models.BooleanField(
        default=False
    )

    def __str__(self):
        return u"{} - {}".format(
            self.nombre,
            self.colegio.abrev
        )

    class Meta:
        verbose_name = u'Periodo'
        verbose_name_plural = u'Periodos'
