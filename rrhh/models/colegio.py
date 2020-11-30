from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from rrhh.models.base import *
from rrhh.models.persona import Funcionario, Persona
from datetime import datetime, date


CATEGORIAS = (
    (1, 'Docente Directivo'),
    (2, 'Docente'),
    (3, 'Asistente de Educación'),
    (4, 'Otro Profesional'),
)


class Colegio(models.Model):
    """
        Modelo de descripcion del colegio
    """
    nombre = models.CharField(max_length=250)
    abrev = models.CharField(max_length=50,verbose_name="Abreviación")
    fundacion = models.ForeignKey('Fundacion', on_delete=models.CASCADE, verbose_name='Fundación')
    rbd = models.CharField(max_length=50, null=True, blank=True, verbose_name="Rol de base de datos (RBD)")
    estado = models.CharField(max_length=25, default='particular_subvencionado', choices=TIPO_SUBVENCION)
    tipo_jornada = models.CharField(max_length=25, default='completa', choices=TIPO_JORNADA, verbose_name='Tipo de jornada')
    total_salas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de salas")
    capacidad_promedio_salas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Capacidad promedio de las salas")
    total_matricula_ultimo_anio = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de matricula el último año")
    total_profesores_aula = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de profesores de aula")
    total_profesionales_educacion = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de profesionales de la educación")
    total_asistentes_educacion = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de asistentes de la educación")
    total_alumnos_pie = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de alumnos en PIE")
    indice_vulnerabilidad = models.CharField(max_length=25, null=True, blank=True, verbose_name="Índice de vulnerabilidad")

    def __str__(self):
        return u"{}@{}".format(
            self.nombre,
            self.abrev
        )

    class Meta:
        verbose_name = u'Colegio'
        verbose_name_plural = u'Colegios'


class ContratoColegio(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE)
    categoria = models.PositiveSmallIntegerField(choices=CATEGORIAS, verbose_name='Categoría')
    funcion_principal = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='funcion_principal', verbose_name='Función principal')
    funcion_secundaria = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='funcion_secundaria', verbose_name='Función secundaria')
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO, verbose_name='Tipo de contrato')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de Término')
    reemplazando_licencia = models.ForeignKey('LicenciaFuncionarioColegio', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='En reemplazo de')
    # permiso_reemplazando = models.ForeignKey('PermisoFuncionarioColegio', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='En reemplazo de')
    horas_total = models.PositiveIntegerField(verbose_name='Horas contratadas')
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(
            self.funcionario,
            self.colegio.abrev
        )

    @property
    def periodo_contrato(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino) if self.fecha_termino else 'indefinido'
        )

    @property
    def dias_termino_contrato(self):
        return 200 if self.tipo_contrato == 1 else (self.fecha_termino - date.today()).days

    class Meta:
        verbose_name = u'Contrato de colegio'
        verbose_name_plural = u'Contratos de colegios'


class DistribucionHoras(models.Model):
    contrato = models.ForeignKey('ContratoColegio', on_delete=models.CASCADE)
    horas = models.PositiveIntegerField(verbose_name='Horas')
    tipo_horas = models.PositiveSmallIntegerField(default=1, choices=TIPO_HORA, verbose_name='Tipo de horas')
    jornada_trabajo = models.PositiveSmallIntegerField(default=1, choices=TIPO_JORNADA, verbose_name='Jornada de trabajo')
    hora_inicio_jornada = models.TimeField(verbose_name='Inicio de jornada')
    hora_termino_jornada = models.TimeField(verbose_name='Término de jornada')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.tipo_horas
        )

    class Meta:
        verbose_name = u'Distribución de horas'
        verbose_name_plural = u'Distribuciones de horas'


class FiniquitoColegio(models.Model):
    contrato = models.OneToOneField('ContratoColegio', on_delete=models.CASCADE)
    razon_baja = models.PositiveSmallIntegerField(default=1, choices=RAZON_FINIQUITO, verbose_name='Razón de baja')
    descripcion = models.TextField(max_length=1500, verbose_name='Descripción')
    voto_traslado = models.PositiveIntegerField(null=True, blank=True, verbose_name='Voto de autorización de traslado')
    archivo = models.FileField(upload_to="rrhh/finiquitos", verbose_name='Finiquito')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.razon_baja
        )

    class Meta:
        verbose_name = u'Finiquito de empleado de colegio'
        verbose_name_plural = u'Finiquitos de empleados de colegios'


class VacacionFuncionarioColegio(models.Model):
    contrato = models.ForeignKey('ContratoColegio', on_delete=models.CASCADE)
    total_dias = models.IntegerField(verbose_name='Total de días de vacaciones')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    total_feriados = models.IntegerField(default=0, verbose_name='Total de feriados en el periodo de vacaciones')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de término')
    fecha_retorno = models.DateField(null=True, blank=True, verbose_name='Fecha de retorno')
    dias_pendiente = models.IntegerField(default=0, verbose_name='Días pendientes')
    es_pendiente = models.BooleanField(default=False, verbose_name='Corresponde a vacaciones pendientes')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.fecha_inicio
        )

    class Meta:
        verbose_name = u'Vacación de empleado de colegio'
        verbose_name_plural = u'Vacaciones de empleados de colegios'

    @property
    def dias_correspondientes(self):
        # TODO crear funcion dias correspondientes, apartir de la antiguedad del funcionario
        dias = 0
        return dias


class LicenciaFuncionarioColegio(models.Model):
    contrato = models.ForeignKey('ContratoColegio', on_delete=models.CASCADE, )
    tipo_licencia = models.ForeignKey('TipoLicencia', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de licencia')
    tipo_licencia_descripcion = models.TextField(max_length=500, null=True, blank=True, verbose_name='Tipo de licencia')
    folio_licencia = models.CharField(max_length=30, null=True, blank=True, verbose_name='Folio de la licencia')
    total_dias = models.IntegerField(verbose_name='Total de días de licencia')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    total_feriados = models.IntegerField(default=0, verbose_name='Total de feriados en el periodo de la licencia')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de término')
    fecha_retorno = models.DateField(null=True, blank=True, verbose_name='Fecha de retorno')
    dias_habiles = models.BooleanField(default=True, verbose_name='Corresponde a días hábiles')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.tipo_licencia
        )

    class Meta:
        verbose_name = u'Licencia de empleado de colegio'
        verbose_name_plural = u'Licencias de empleados de colegios'


class Entrevista(models.Model):
    contrato = models.ForeignKey('ContratoColegio', on_delete=models.CASCADE)
    entrevistador = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_ENTREVISTA)
    contenido = models.TextField()
    acuerdos = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.tipo
        )

    class Meta:
        verbose_name = u'Entevista de empleado de colegio'
        verbose_name_plural = u'Entrevistas de empleados de colegios'


class SolicitudContratacion(models.Model):
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE)
    categoria = models.PositiveSmallIntegerField(default=2, choices=CATEGORIAS)
    cargo = models.CharField(max_length=250)
    horas = models.PositiveIntegerField(verbose_name='Horas de contrato')
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO)
    reemplazando_licencia = models.ForeignKey('LicenciaFuncionarioColegio', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='En reemplazo de')
    # reemplazando_permiso = models.ForeignKey('PermisoFuncionarioColegio', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='En reemplazo de')
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    justificacion = models.CharField(max_length=255, verbose_name='Justificación')
    postulantes = models.ManyToManyField(Persona, blank=True)

    def __str__(self):
        return '{}, {}'.format(
            self.colegio,
            self.cargo
        )

    @property
    def estado(self):
        try:
            estado = self.estadosolicitud_set.all().last().get_estado_display
        except:
            estado = 'No existe'

        return estado

    @property
    def voto(self):
        try:
            voto = self.estadosolicitud_set.all().last().voto
        except:
            voto = ''

        return voto

    @property
    def periodo_contratacion(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino) if self.fecha_termino else 'indefinido'
        )

    class Meta:
        verbose_name = u'Solicitud de contratación'
        verbose_name_plural = u'Solicitudes de contratación'


class EstadoSolicitud(models.Model):
    solicitud = models.ForeignKey('SolicitudContratacion', on_delete=models.CASCADE)
    estado = models.PositiveSmallIntegerField(default=2, choices=ESTADO_SOLICITUD)
    observaciones = models.TextField(max_length=2500, null=True, blank=True)
    voto = models.CharField(max_length=150, null=True, blank=True, verbose_name='Voto de autorización')
    fecha = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(
            self.solicitud,
            self.estado
        )

    class Meta:
        verbose_name = u'Estado de solicitud'
        verbose_name_plural = u'Estados de solicitudes'


class SolicitudRenovacion(models.Model):
    contrato = models.OneToOneField('ContratoColegio', on_delete=models.CASCADE)
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO)
    horas = models.PositiveIntegerField(verbose_name='Horas de contrato')
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    estado = models.PositiveSmallIntegerField(default=1, choices=ESTADO_SOLICITUD_RENOVACION)
    voto = models.CharField(max_length=150, null=True, blank=True, verbose_name='Voto de autorización')
    observaciones = models.TextField(max_length="2100", null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.estado
        )

    @property
    def periodo_contratacion(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino) if self.fecha_termino else 'indefinido'
        )

    class Meta:
        verbose_name = u'Solicitud de renovación'
        verbose_name_plural = u'Solicitudes de renovación'
