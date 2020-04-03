from django.db import models
from gestion.models import TimeStampModel


# Create your models here.
generos = (
    ('M', 'Masculino'),
    ('F', 'Femenino')
)

estados_civiles = (
    ('soltero', 'Soltero/a'),
    ('casado', 'Casado/a'),
    ('viudo', 'Viudo/a'),
    ('divorciado', 'Divorciado/a'),
    ('separado', 'Separado/a'),
    ('conviviente', 'Conviviente')
)

estados_funcionario = (
    ('contratado', 'Contratado'),
    ('desvinculado', 'Desvinculado')
)


class Funcionario(TimeStampModel):
    """
        Modelo para el detalle de un funcionario, como persona Natural
    """
    rut = models.CharField(
        max_length=10
    )
    nombres = models.CharField(
        max_length=250
    )
    apellido_paterno = models.CharField(
        max_length=250
    )
    apellido_materno = models.CharField(
        max_length=250
    )
    genero = models.CharField(
        max_length=5,
        choices=generos,
        verbose_name="Género"
    )
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de Nacimiento"
    )
    nacionalidad = models.CharField(
        null=True,
        blank=True,
        max_length=150
    )
    estado_civil = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        choices=estados_civiles
    )
    religion = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Religión"
    )
    direccion = models.CharField(
        max_length=500,
        verbose_name="Dirección"
    )
    telefono = models.CharField(
        max_length=15,
        verbose_name="Teléfono"
    )
    correo_electronico = models.EmailField(
        verbose_name="Correo electrónico"
    )
    antiguedad_docente_meses = models.PositiveIntegerField(
        verbose_name="Antiguedad del docente (en meses)"
    )
    fecha_ingreso_docente = models.DateField(
        verbose_name="Fecha de ingreso al Sistema Docente"
    )
    antiguedad_sea_meses = models.PositiveIntegerField(
        verbose_name="Antiguedad del funcionario en SEA (en meses)"
    )
    fecha_ingreso_sea = models.DateField(
        verbose_name="Fecha de ingreso al Sistema Educacional Adventista"
    )
    titulo = models.BooleanField(
        default=False,
        verbose_name="Título"
    )
    casa_formativa = models.CharField(
        max_length=1500
    )
    profesion = models.CharField(
        max_length=1500,
        verbose_name="Profesión"
    )

    def __str__(self):
        return u"{}".format(
            self.rut
        )

    class Meta:
        verbose_name = u'Funcionario'
        verbose_name_plural = u'Funcionarios'


class Perfeccionamiento(TimeStampModel):
    """
        Modelo para el registro del perfeccionamiento del funcionario ej. magister, postitulo, menciones, etc.
    """
    funcionario = models.ForeignKey(
        "Funcionario",
        on_delete=models.CASCADE
    )
    tipo_perfeccionamiento = models.CharField(
        max_length=150
    )
    perfeccionamiento = models.CharField(
        max_length=250
    )
    institucion = models.CharField(
        max_length=250
    )
    certificado = models.FileField()

    def __str__(self):
        return u"{} - {}".format(
            self.funcionario,
            self.tipo_perfeccionamiento
        )

    class Meta:
        verbose_name = u'Perfeccionamiento'
        verbose_name_plural = u'Perfeccionamientos'


class Documentacion(TimeStampModel):
    """
        Modelo para el registro de documentos de un funcionario
    """
    funcionario = models.ForeignKey(
        "Funcionario",
        on_delete=models.CASCADE
    )
    foto = models.FileField()
    titulo = models.FileField(
        verbose_name="Título"
    )
    curriculum = models.FileField(
        verbose_name="Currículum"
    )
    certificado_antecedentes = models.FileField(
        verbose_name="Certificado de Antecedentes"
    )

    def __str__(self):
        return u"{}".format(
            self.funcionario
        )

    class Meta:
        verbose_name = u'Documentación'
        verbose_name_plural = u'Documentación'


class FuncionarioUnion(TimeStampModel):
    """
        Modelo de registro de actividad de un funcionario en una unión
    """
    funcionario = models.ForeignKey(
        "Funcionario",
        null=True,
        on_delete=models.SET_NULL
    )
    union = models.ForeignKey(
        "gestion.Union",
        null=True,
        on_delete=models.SET_NULL
    )
    tipo_contrato = models.CharField(
        max_length=150,
        verbose_name="Tipo de contrato"
    )
    estado_funcionario = models.CharField(
        max_length=150,
        choices=estados_funcionario,
        default='contratado',
        verbose_name="Estado del funcionario"
    )
    funcion = models.CharField(
        max_length=250,
        verbose_name="Función"
    )
    horas_contrato = models.PositiveIntegerField(
        verbose_name="Horas de contrato"
    )
    fecha_inicio_contrato = models.DateField(
        verbose_name="Fecha de inicio de contrato"
    )
    fecha_termino_contrato = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de termino de contrato"
    )
    causa_termino_contrato = models.TextField(
        max_length=2500,
        null=True,
        blank=True,
        verbose_name="Causa de termino de contrato"
    )

    def __str__(self):
        return u"{} - {}".format(
            self.funcionario,
            self.union
        )

    class Meta:
        verbose_name = u'Funcionario de Unión'
        verbose_name_plural = u'Funcionarios de Uniones'


class FuncionarioFundacion(TimeStampModel):
    """
        Modelo de registro de actividad de un funcionario en una fundación
    """
    funcionario = models.ForeignKey(
        "Funcionario",
        null=True,
        on_delete=models.SET_NULL
    )
    fundacion = models.ForeignKey(
        "gestion.Fundacion",
        null=True,
        on_delete=models.SET_NULL
    )
    tipo_contrato = models.CharField(
        max_length=150,
        verbose_name="Tipo de contrato"
    )
    estado_funcionario = models.CharField(
        max_length=150,
        choices=estados_funcionario,
        default='contratado',
        verbose_name="Estado del funcionario"
    )
    funcion = models.CharField(
        max_length=250,
        verbose_name="Función"
    )
    horas_contrato = models.PositiveIntegerField(
        verbose_name="Horas de contrato"
    )
    fecha_inicio_contrato = models.DateField(
        verbose_name="Fecha de inicio de contrato"
    )
    fecha_termino_contrato = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de termino de contrato"
    )
    causa_termino_contrato = models.TextField(
        max_length=2500,
        null=True,
        blank=True,
        verbose_name="Causa de termino de contrato"
    )

    def __str__(self):
        return u"{} - {}".format(
            self.funcionario,
            self.fundacion
        )

    class Meta:
        verbose_name = u'Funcionario de Fundación'
        verbose_name_plural = u'Funcionarios de Fundaciones'


class FuncionarioColegio(TimeStampModel):
    """
        Modelo de registro de actividad de un funcionario en un colegio especifico
    """
    funcionario = models.ForeignKey(
        "Funcionario",
        null=True,
        on_delete=models.SET_NULL
    )
    colegio = models.ForeignKey(
        "gestion.Colegio",
        null=True,
        on_delete=models.SET_NULL
    )
    tipo_contrato = models.CharField(
        max_length=150,
        verbose_name="Tipo de contrato"
    )
    estado_funcionario = models.CharField(
        max_length=150,
        choices=estados_funcionario,
        default='contratado',
        verbose_name="Estado del funcionario"
    )
    funcion = models.CharField(
        max_length=250,
        verbose_name="Función"
    )
    sector_funcion = models.CharField(
        max_length=250,
        verbose_name="Sector de la función"
    )
    sub_sector_funcion = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Sub sector de la función"
    )
    funcion_secundaria = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Función secundaria"
    )
    sector_funcion_secundaria = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Sector de la función secundaria"
    )
    sub_sector_funcion_secundaria = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name="Sub sector de la función secundaria"
    )
    horas_contrato = models.PositiveIntegerField(
        verbose_name="Horas de contrato"
    )
    fecha_inicio_contrato = models.DateField(
        verbose_name="Fecha de inicio de contrato"
    )
    fecha_termino_contrato = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de término de contrato"
    )
    causa_termino_contrato = models.TextField(
        max_length=2500,
        null=True,
        blank=True,
        verbose_name="Causa de término de contrato"
    )

    def __str__(self):
        return u"{} - {}".format(
            self.funcionario,
            self.colegio
        )

    class Meta:
        verbose_name = u'Funcionario de Colegio'
        verbose_name_plural = u'Funcionarios de Colegios'


class Vacacion(TimeStampModel):
    """
        Modelo de registro de vacaciones del funcionario de colegio
    """
    funcionario = models.ForeignKey(
        "FuncionarioColegio",
        on_delete=models.CASCADE
    )
    total_dias = models.PositiveIntegerField(
        verbose_name="Total de días"
    )
    dias_pendientes = models.PositiveIntegerField(
        verbose_name="Días pendientes"
    )
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    anio = models.PositiveIntegerField(
        verbose_name="Año"
    )
    pendiente = models.BooleanField(
        default=False,
        verbose_name="¿Pertenece a vacaciones pendientes?"
    )

    def __str__(self):
        return u"{} - {}".format(
            self.funcionario,
            self.anio
        )

    class Meta:
        verbose_name = u'Vacación'
        verbose_name_plural = u'Vacaciones'


class Licencia(TimeStampModel):
    """
        Modelo de registro de las vacaciones del funcionario de colegio
    """
    funcionario = models.ForeignKey(
        "FuncionarioColegio",
        on_delete=models.CASCADE
    )
    tipo_licencia = models.CharField(
        max_length=150,
        verbose_name="Tipo de licencia"
    )
    total_dias = models.PositiveIntegerField(
        verbose_name="Total de días"
    )
    fecha_inicio = models.DateField(
        verbose_name="Fecha de inicio"
    )
    fecha_termino = models.DateField(
        verbose_name="Fecha de término"
    )

    def __str__(self):
        return u"{} - {} ({} días)".format(
            self.funcionario,
            self.tipo_licencia,
            self.total_dias
        )

    class Meta:
        verbose_name = u'Licencia'
        verbose_name_plural = u'Licencias'


class Asistencia(TimeStampModel):
    """
        Modelo para el registro de asistencia de un funcionario de colegio
    """
    funcionario = models.ForeignKey(
        "FuncionarioColegio",
        on_delete=models.CASCADE
    )
    tipo_registro = models.CharField(
        max_length=150,
        verbose_name="Tipo de registro"
    )
    fecha = models.DateField()
    horas = models.TimeField()

    def __str__(self):
        return u"{} - {}".format(
            self.funcionario,
            self.fecha
        )

    class Meta:
        verbose_name = u'Asistencia'
        verbose_name_plural = u'Asistencias'


class ObservacionEntrevista(TimeStampModel):
    """
        Modelo de registro de entrevistas de funcionarios de coelgios
    """
    funcionario = models.ForeignKey(
        "FuncionarioColegio",
        on_delete=models.CASCADE
    )
    fecha = models.DateField()
    observador = models.ForeignKey(
        "FuncionarioColegio",
        on_delete=models.CASCADE,
        related_name="observador"
    )
    observador_adjunto = models.ForeignKey(
        "FuncionarioFundacion",
        null=True,
        on_delete=models.SET_NULL
    )
    tipo = models.CharField(
        max_length=150
    )
    motivo = models.TextField(
        max_length=1250
    )
    acuerdos = models.TextField(
        max_length=2500
    )
    acta = models.FileField()

    def __str__(self):
        return u"{} - {} ({})".format(
            self.funcionario,
            self.tipo,
            self.fecha
        )

    class Meta:
        verbose_name = u'Observación o entrevista'
        verbose_name_plural = u'Observaciones o entrevistas'


class ObservadorAdjunto(TimeStampModel):
    """
        modelo para el registro de observadores adjuntos a una observación o entrevista
    """
    observacion_entrevista = models.ForeignKey(
        "ObservacionEntrevista",
        on_delete=models.CASCADE
    )
    observador = models.ForeignKey(
        "FuncionarioColegio",
        on_delete=models.CASCADE
    )
    funcion = models.CharField(
        max_length=150,
        null=True
    )

    def __str__(self):
        return u"{}".format(
            self.observacion_entrevista,
        )

    class Meta:
        verbose_name = u'Observador adjunto'
        verbose_name_plural = u'Observadores adjuntos'
