from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords
from django.contrib.humanize.templatetags import humanize
from rrhh.models.base import *
from datetime import date

CATEGORIAS = (
    (1, 'Docente Directivo'),
    (2, 'Docente'),
    (3, 'Asistente de Educación'),
    (4, 'Otro Profesional'),
)

TIPO_ENTIDAD = (
    ('colegio', 'Colegio'),
    ('fundacion', 'Fundación'),
    ('union', 'Unión'),
)


class Entidad(models.Model):
    nombre = models.CharField(max_length=250)
    abrev = models.CharField(max_length=50, verbose_name="Abreviación")
    direccion = models.CharField(max_length=250, null=True, blank=True, verbose_name='Dirección')
    tipo_entidad = models.CharField(max_length=50, default='colegio', choices=TIPO_ENTIDAD)
    dependiente = models.ForeignKey('Entidad', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Depende de')

    @property
    def colaboradores(self):
        return Contrato.objects.filter(entidad=self, vigente=True)

    def __str__(self):
        return u"{} @ {}".format(
            self.nombre,
            self.abrev
        )

    class Meta:
        verbose_name = u'Entidad'
        verbose_name_plural = u'Entidades'


class DetalleFundacion(models.Model):
    fundacion = models.OneToOneField('Entidad', on_delete=models.CASCADE, verbose_name='Fundación')
    rut = models.CharField(max_length=50, null=True, blank=True, verbose_name="Rol de base de datos (RBD)")

    def __str__(self):
        return self.fundacion

    class Meta:
        verbose_name = u'Detalle de Fundación'
        verbose_name_plural = u'Detalles de Fundaciones'


class RepresentanteLegal(models.Model):
    fundacion = models.ForeignKey('Entidad', on_delete=models.CASCADE, verbose_name='Fundación')
    representante = models.ForeignKey('Contrato', on_delete=models.CASCADE, verbose_name='Responsable legal')

    @property
    def vigente(self):
        return self.representante.vigente

    def __str__(self):
        return '{} - {}'.format(
            self.representante.funcionario,
            self.fundacion,
        )

    class Meta:
        verbose_name = u'Representante Legal'
        verbose_name_plural = u'Representates Legales'


class DetalleColegio(models.Model):
    """
        Modelo de descripcion del colegio
    """
    colegio = models.ForeignKey('Entidad', on_delete=models.CASCADE)
    rbd = models.CharField(max_length=50, null=True, blank=True, verbose_name="Rol de base de datos (RBD)")
    tipo_subvencion = models.CharField(max_length=75, default='particular_subvencionado', choices=TIPO_SUBVENCION,
                              verbose_name='Tipo de subvención')
    tipo_jornada = models.CharField(max_length=25, default='completa', choices=TIPO_JORNADA,
                                    verbose_name='Tipo de jornada')
    total_salas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de salas")
    capacidad_promedio_salas = models.PositiveIntegerField(null=True, blank=True,
                                                           verbose_name="Capacidad promedio de las salas")
    total_matricula_ultimo_anio = models.PositiveIntegerField(null=True, blank=True,
                                                              verbose_name="Total de matricula el último año")
    total_profesores_aula = models.PositiveIntegerField(null=True, blank=True,
                                                        verbose_name="Total de profesores de aula")
    total_profesionales_educacion = models.PositiveIntegerField(null=True, blank=True,
                                                                verbose_name="Total de profesionales de la educación")
    total_asistentes_educacion = models.PositiveIntegerField(null=True, blank=True,
                                                             verbose_name="Total de asistentes de la educación")
    total_alumnos_pie = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total de alumnos en PIE")
    indice_vulnerabilidad = models.CharField(max_length=25, null=True, blank=True,
                                             verbose_name="Índice de vulnerabilidad")

    def __str__(self):
        return self.colegio

    class Meta:
        verbose_name = u'Detalle del Colegio'
        verbose_name_plural = u'Detalles de los Colegios'


class Contrato(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    entidad = models.ForeignKey('Entidad', on_delete=models.CASCADE)
    categoria = models.PositiveSmallIntegerField(choices=CATEGORIAS, verbose_name='Categoría')
    funcion_principal = models.ForeignKey(
        'Funcion',
        on_delete=models.CASCADE,
        related_name='funcion_principal',
        verbose_name='Función principal'
    )
    funcion_secundaria = models.ForeignKey(
        'Funcion',
        on_delete=models.CASCADE,
        related_name='funcion_secundaria',
        verbose_name='Función secundaria'
    )
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO, verbose_name='Tipo de contrato')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de Término')
    reemplazando_licencia = models.ForeignKey(
        'Licencia',
        related_name='reemplazando_licencia',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='En reemplazo de (licencia)'
    )
    reemplazando_permiso = models.ForeignKey(
        'Permiso',
        related_name='reemplazando_permiso',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='En reemplazo de (permiso)'
    )
    horas_total = models.PositiveIntegerField(verbose_name='Horas contratadas')
    sueldo = models.PositiveIntegerField(null=True, blank=True, verbose_name='Sueldo a percibir')
    asignacion_funcion = models.PositiveIntegerField(null=True, blank=True, verbose_name='Asignación por función')
    asignacion_locomocion = models.PositiveIntegerField(null=True, blank=True, verbose_name='Asignación por locomoción')
    vigente = models.BooleanField(default=False)

    @property
    def periodo_contrato(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino) if self.fecha_termino else 'indefinido'
        )

    @property
    def dias_termino_contrato(self):
        return 200 if self.tipo_contrato == 1 else (self.fecha_termino - date.today()).days

    @property
    def estado(self):
        try:
            estado = self.estadocontratacion_set.all().last().get_estado_display()
        except:
            estado = 'No existe'

        return estado

    @property
    def estado_id(self):
        try:
            estado = self.estadocontratacion_set.all().last().estado
        except:
            estado = 1

        return estado

    @property
    def colaborador(self):
        return '{} - {}'.format(
            self.funcionario.persona.get_name,
            self.funcion_principal
        )

    def __str__(self):
        return '{} - {}'.format(
            self.funcionario,
            self.entidad.abrev
        )

    class Meta:
        verbose_name = u'Contrato'
        verbose_name_plural = u'Contratos'


class EstadoContratacion(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    estado = models.PositiveSmallIntegerField(default=2, choices=ESTADO_CONTRATACION)
    observaciones = models.TextField(max_length=2500, null=True, blank=True)
    fecha = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.estado
        )

    class Meta:
        verbose_name = u'Estado de contratación'
        verbose_name_plural = u'Estados de contrataciones'


class DistribucionHoras(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    horas = models.PositiveIntegerField(verbose_name='Horas')
    tipo_horas = models.PositiveSmallIntegerField(default=1, choices=TIPO_HORA, verbose_name='Tipo de horas')
    jornada_trabajo = models.PositiveSmallIntegerField(
        default=1,
        choices=TIPO_JORNADA,
        verbose_name='Jornada de trabajo'
    )
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


class AcuerdoContrato(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    acuerdo = models.TextField(verbose_name='Acuerdo pactado')
    monto = models.PositiveIntegerField(null=True, blank=True, verbose_name='Monto pactado')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            truncatewords(self.acuerdo, 7)
        )

    class Meta:
        verbose_name = u'Acuerdo de Contrato'
        verbose_name_plural = u'Acuerdos de Contratos'


class Finiquito(models.Model):
    contrato = models.OneToOneField('Contrato', on_delete=models.CASCADE)
    razon_baja = models.PositiveSmallIntegerField(default=1, choices=RAZON_FINIQUITO, verbose_name='Razón de baja')
    descripcion = models.TextField(max_length=1500, verbose_name='Descripción')
    voto_traslado = models.PositiveIntegerField(null=True, blank=True, verbose_name='Voto de autorización de traslado')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.razon_baja
        )

    class Meta:
        verbose_name = u'Finiquito de empleado'
        verbose_name_plural = u'Finiquitos de empleados'


class Vacacion(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    anio_vacacion = models.PositiveIntegerField(default=0)
    total_dias = models.IntegerField(verbose_name='Total de días de vacaciones')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    total_feriados = models.IntegerField(default=0, verbose_name='Total de feriados en el periodo de vacaciones')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de término')
    fecha_retorno = models.DateField(null=True, blank=True, verbose_name='Fecha de retorno')
    es_pendiente = models.BooleanField(default=False, verbose_name='Corresponde a vacaciones pendientes')

    @property
    def dias_correspondientes(self):
        # TODO crear funcion dias correspondientes, apartir de la antiguedad del funcionario
        dias = 0
        return dias

    @property
    def dias_pendientes(self):
        dias = 0

        return dias

    @property
    def periodo(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino)
        )

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.fecha_inicio
        )

    class Meta:
        verbose_name = u'Vacación'
        verbose_name_plural = u'Vacaciones'


class DiasPendientesVacacion(models.Model):
    anio_vacacion = models.PositiveIntegerField()
    vacacion = models.ForeignKey("Vacacion", on_delete=models.CASCADE)
    dias_pendientes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} / {} / {}'.format(
            self.anio_vacacion,
            self.vacacion,
            self.dias_pendientes
        )

    class Meta:
        verbose_name = u'Dias pendientes de vacación'
        verbose_name_plural = u'Dias pendinetes de vacaciones'


class Licencia(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    tipo_licencia = models.ForeignKey(
        'TipoLicencia',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Tipo de licencia'
    )
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
            self.tipo_licencia if self.tipo_licencia else 'Personalizada'
        )

    @property
    def periodo(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino)
        )

    class Meta:
        verbose_name = u'Licencia'
        verbose_name_plural = u'Licencias'


class Permiso(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    total_dias = models.IntegerField(verbose_name='Total de días de permiso')
    observaciones = models.TextField(max_length=2500, verbose_name='Motivos u observaciones')
    fecha_solicitud = models.DateField(verbose_name='Fecha de solicitud')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    total_feriados = models.IntegerField(default=0, verbose_name='Total de feriados en el periodo del permiso')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de término')
    fecha_retorno = models.DateField(null=True, blank=True, verbose_name='Fecha de retorno')
    goce_sueldo = models.BooleanField(default=False, verbose_name="Con goce de sueldo")
    dias_habiles = models.BooleanField(default=True, verbose_name='Corresponde a días hábiles')
    voto = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            truncatewords(self.observaciones, 7)
        )

    @property
    def periodo(self):
        return '{} - {}'.format(
            humanize.naturalday(self.fecha_inicio),
            humanize.naturalday(self.fecha_termino)
        )

    class Meta:
        verbose_name = u'Permiso'
        verbose_name_plural = u'Permisos'


class Entrevista(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
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
        verbose_name = u'Entevista'
        verbose_name_plural = u'Entrevistas'


class Solicitud(models.Model):
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPOS_SOLICITUD)
    entidad = models.ForeignKey('Entidad', on_delete=models.CASCADE)
    contrato = models.ForeignKey('Contrato', on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.PositiveSmallIntegerField(default=2, choices=CATEGORIAS)
    cargo = models.CharField(max_length=250)
    horas = models.PositiveIntegerField(verbose_name='Horas de contrato')
    sueldo = models.PositiveIntegerField(null=True, blank=True, verbose_name='Sueldo a percibir')
    asignacion_funcion = models.PositiveIntegerField(null=True, blank=True, verbose_name='Asignación por función')
    asignacion_locomocion = models.PositiveIntegerField(null=True, blank=True, verbose_name='Asignación por locomoción')
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO)
    reemplazando_licencia = models.ForeignKey(
        'Licencia',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='En reemplazo de (licencia)'
    )
    reemplazando_permiso = models.ForeignKey(
        'Permiso',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='En reemplazo de (permiso)'
    )
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    justificacion = models.CharField(max_length=255, verbose_name='Justificación')
    postulantes = models.ManyToManyField('Persona', blank=True)

    def __str__(self):
        return '{}, {}'.format(
            self.entidad,
            self.cargo
        )

    @property
    def estado(self):
        try:
            estado = self.estadosolicitud_set.all().last().get_estado_display()
        except:
            estado = 'No existe'

        return estado

    @property
    def estado_id(self):
        try:
            estado = self.estadosolicitud_set.all().last().estado
        except:
            estado = 2

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
        verbose_name = u'Solicitud'
        verbose_name_plural = u'Solicitudes'


class EstadoSolicitud(models.Model):
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
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
