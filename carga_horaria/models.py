from django.contrib.postgres.fields import ArrayField
from django.db import models
from gestion.models import TimeStampModel


# Create your models here.
tipos_ensenanza = (
    ('basica', 'Básica'),
    ('media', 'Media')
)

tipos_formacion = (
    ('general-dif.cient.human', 'Formación General y Diferenciada Humanístico-Científica'),
    ('general-dif.tec.profesional', 'Formación General y Diferenciada Técnico Profesional'),
    ('diferenciada-artistica', 'Formación Diferenciada Artística')
)

tipos_jornada = (
    ('media', 'Media Jornada'),
    ('completa', 'Jornada Completa'),
)

tipos_cursos = (
    ('normal', 'Normal'),
    ('combinado', 'Combinado')
)

niveles = (
    ('k', 'Kinder'),
    ('pk', 'Pre Kinder'),
    ('1', 'Primero Básico'),
    ('2', 'Segundo Básico'),
    ('3', 'Tercero Básico'),
    ('4', 'Cuarto Básico'),
    ('5', 'Quinto Básico'),
    ('6', 'Sexto Básico'),
    ('7', 'Septimo Básico'),
    ('8', 'Octavo Básico'),
    ('1M', 'Primero Medio'),
    ('2M', 'Segundo Medio'),
    ('3M', 'Tercero Medio'),
    ('4M', 'Cuarto Medio'),
)


class Curso(TimeStampModel):
    """
        Modelo de descripcion del curso, esta es la especificacion de estructura de cursos
    """
    periodo = models.ForeignKey(
        "gestion.Periodo",
        on_delete=models.CASCADE
    )
    tipo_ensenanza = models.CharField(
        max_length=150,
        choices=tipos_ensenanza,
        verbose_name="Tipo de enseñanza"
    )
    nivel = models.CharField(
        max_length=150,
        choices=niveles
    )
    letra = models.CharField(
        max_length=10,
        null=True
    )
    jornada = models.CharField(
        max_length=150,
        choices=tipos_jornada
    )
    tipo_curso = models.CharField(
        max_length=150,
        choices=tipos_cursos,
        default='normal'
    )
    cursos = models.ManyToManyField(
        "Curso"
    )
    profesor_jefe = models.ForeignKey(
        "recursos_humanos.FuncionarioColegio",
        null=True,
        on_delete=models.SET_NULL
    )
    decreto_evaluacion = models.CharField(
        max_length=150,
        null=True
    )

    def __unicode__(self):
        return u"{} {} - {}".format(
            self.nivel,
            self.tipo_ensenanza,
            self.periodo
        )

    class Meta:
        verbose_name = u'Curso'
        verbose_name_plural = u'Cursos'


class Asignatura(TimeStampModel):
    """
        Modelo de registro de Asignaturas
    """
    nombre = models.CharField(
        max_length=250
    )
    tipo_ensenanza = models.CharField(
        max_length=250,
        default="basica",
        choices=tipos_ensenanza
    )
    tipo_formacion = models.CharField(
        max_length=150,
        choices=tipos_formacion
    )
    niveles = ArrayField(
        models.CharField(
            max_length=150,
            choices=niveles
        )
    )
    lengua_indigena = models.BooleanField(
        default=False,
        verbose_name="¿Es Lengua Indigena?"
    )
    horas_anuales_jec = models.PositiveIntegerField(
        default=0,
        verbose_name="Horas anuales con JEC"
    )
    horas_anuales_sin_jec = models.PositiveIntegerField(
        default=0,
        verbose_name="Horas anuales sin JEC"
    )
    horas_semanales_jec = models.PositiveIntegerField(
        default=0,
        verbose_name="Horas semanales con JEC"
    )
    horas_semanales_sin_jec = models.PositiveIntegerField(
        default=0,
        verbose_name="Horas semanales sin JEC"
    )

    def __unicode__(self):
        return u"{} - {}".format(
            self.nombre,
            self.tipo_ensenanza
        )

    class Meta:
        verbose_name = u'Asignatura'
        verbose_name_plural = u'Asignaturas'


class PlanEstudio(TimeStampModel):
    """
        Modelo de registro de plan de estudio:
            Asignaturas en un curso específico
    """
    curso = models.ForeignKey(
        "Curso",
        on_delete=models.CASCADE
    )
    asignatura = models.ForeignKey(
        "Asignatura",
        on_delete=models.CASCADE
    )
    horas_asignatura = models.PositiveIntegerField(
        verbose_name="Horas para la asignatura"
    )
    horas_asignadas = models.PositiveIntegerField(
        verbose_name="Horas asignadas a docentes"
    )
    horas_sin_asignar = models.PositiveIntegerField(
        verbose_name="Horas sin asignar"
    )

    def __unicode__(self):
        return u"{} - {} {}".format(
            self.asignatura.nombre,
            self.curso.nivel,
            self.curso.tipo_ensenanza
        )

    class Meta:
        verbose_name = u'Plan de Estudio'
        verbose_name_plural = u'Planes de estudio'


class Semestre(TimeStampModel):
    """
        Modelo de registro de semestres o trimestres, segun el establecimiento
    """
    periodo = models.ForeignKey(
        "gestion.Periodo",
        on_delete=models.CASCADE
    )
    nombre = models.CharField(
        max_length=250
    )
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    def __unicode__(self):
        return u"{} - {}".format(
            self.nombre,
            self.periodo
        )

    class Meta:
        verbose_name = u'Semestre'
        verbose_name_plural = u'Semestres'


class AsignaturaExtra(TimeStampModel):
    """
        Modelo de Asignaturas extra para un semestre, tales como talleres, religion, orientacion, etc.
    """
    nombre = models.CharField(
        max_length=250,
    )
    semestre = models.ForeignKey(
        "Semestre",
        on_delete=models.CASCADE
    )
    curso = models.ForeignKey(
        "Curso",
        on_delete=models.CASCADE
    )
    horas_asignatura = models.PositiveIntegerField(
        null=True,
        verbose_name="Horas para la asignatura"
    )
    horas_asignadas = models.PositiveIntegerField(
        null=True,
        verbose_name="Horas asignadas a docentes"
    )
    horas_sin_asignar = models.PositiveIntegerField(
        null=True,
        verbose_name="Horas sin asignar"
    )

    def __unicode__(self):
        return u"{} - {}".format(
            self.nombre,
            self.curso.nivel,
            self.curso.tipo_ensenanza
        )

    class Meta:
        verbose_name = u'Asignatura extra'
        verbose_name_plural = u'Asignaturas extra'


class CargaHoraria(TimeStampModel):
    """
        Modelo para el registro de las horas por asignatura y docente
    """
    plan_estudio = models.ForeignKey(
        "PlanEstudio",
        null=True,
        on_delete=models.CASCADE
    )
    asignatura_extra = models.ForeignKey(
        "AsignaturaExtra",
        null=True,
        on_delete=models.CASCADE
    )
    docente = models.ForeignKey(
        "recursos_humanos.FuncionarioColegio",
        null=True,
        on_delete=models.SET_NULL
    )
    horas_asignadas = models.PositiveIntegerField()

    def __unicode__(self):
        return u"{} - {}".format(
            self.plan_estudio if self.plan_estudio is not None else self.asignatura_extra,
            self.docente
        )

    class Meta:
        verbose_name = u'Carga horaria'
        verbose_name_plural = u'Cargas horarias'


class TablaTiempoLectivo(TimeStampModel):
    """
        Modelo para la especificacion del Tiempo Lectivo
    """
    nombre = models.CharField(
        max_length=250,
        verbose_name="Nombre de la tabla"
    )
    proporcion = models.CharField(
        max_length=150,
        verbose_name="Proporción"
    )
    decreto = models.CharField(
        max_length=250
    )
    restriccion = models.CharField(
        max_length=250,
        verbose_name="Restricción de aplicación"
    )

    def __unicode__(self):
        return u"{} ({})".format(
            self.nombre,
            self.proporcion
        )

    class Meta:
        verbose_name = u'Tabla de tiempo lectivo'
        verbose_name_plural = u'Tablas de tiempo lectivo'


class DistribucionTiempoLectivo(TimeStampModel):
    """
        Modelo de descripción de las horas, según la jornada semanal de contrato
    """
    jornada_semanal = models.PositiveIntegerField(
        verbose_name="Jornada Semanal (Horas cronológicas de contrato)"
    )
    horas_lectivas_HA = models.PositiveIntegerField(
        verbose_name="Horas lectivas (horas aula)"
    )
    horas_lectivas_HC = models.TimeField(
        verbose_name="Horas lectivas (horas cronológicas)"
    )
    recreo = models.TimeField()
    horas_no_lectivas = models.TimeField(
        verbose_name="Horas no lectivas"
    )
