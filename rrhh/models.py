from django.db import models


class Persona(models.Model):
    ESTADO_CHOICES = (
        (1, 'Empleado'),
        (2, 'Misionero')
    )

    TIPO_MISIONERO_CHOICES = (
        (1, 'Licencia misionera'),
        (2, 'Credencial misionera'),
        (2, 'Credencial ministerial')
    )

    rut = models.CharField(max_length=16, unique=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    genero = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    nacionalidad = models.CharField(max_length=255, null=True, blank=True)
    estado_civil = models.CharField(max_length=255, null=True, blank=True)
    religion = models.CharField(max_length=255, verbose_name='Religión', null=True, blank=True)
    direccion = models.CharField(max_length=255, verbose_name='Dirección')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    email = models.EmailField()
    estado = models.PositiveSmallIntegerField(default=1, choices=ESTADO_CHOICES, verbose_name='Estado funcionario')
    tipo_misionero = models.PositiveSmallIntegerField(choices=TIPO_MISIONERO_CHOICES, null=True, blank=True, verbose_name='Tipo de Misionero')
    puntos = models.PositiveIntegerField(default=0, null=True, blank=True)
    fecha_ingreso_docente = models.DateField(verbose_name='Fecha de ingreso como docente', null=True, blank=True)
    fecha_ingreso_sea = models.DateField(verbose_name='Fecha de ingreso al SEA', null=True, blank=True)
    titulo = models.CharField(max_length=255, verbose_name='Título', null=True, blank=True)
    casa_formadora = models.CharField(max_length=255, null=True, blank=True)
    fecha_titulacion = models.DateField(verbose_name='Fecha de titulación', null=True, blank=True)
    # añadir listado de archivos

    def __str__(self):
        return '{} {} {} ({})'.format(
            self.nombres,
            self.apellido_paterno,
            self.apellido_materno,
            self.rut
        )

    class Meta:
        verbose_name = u'Persona'
        verbose_name_plural = u'Personas'

    @property
    def get_full_name(self):
        return '{} {} {}'.format(
            self.nombres,
            self.apellido_paterno,
            self.apellido_materno
        )


class Entrevista(models.Model):
    FELICITACIONES = 1
    RECOMENDACIONES = 2

    TIPO_CHOICES = ((FELICITACIONES, 'Felicitaciones'),
                    (RECOMENDACIONES, 'Recomendaciones'))

    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    entrevistador = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=FELICITACIONES, choices=TIPO_CHOICES)
    contenido = models.TextField()
    acuerdos = models.TextField()
    # añadir fecha

    def __str__(self):
        return self.contrato.persona

    class Meta:
        verbose_name = u'Entevista'
        verbose_name_plural = u'Entrevistas'


class Archivo(models.Model):
    descripcion = models.CharField(max_length=255)
    archivo = models.FileField()
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)


class Vacacion(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
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
        verbose_name = u'Vacación'
        verbose_name_plural = u'Vacaciones'

    @property
    def dias_correspondientes(self):
        # TODO crear funcion dias correspondientes, apartir de la antiguedad del funcionario
        dias = 0
        return dias


class TipoLicencia(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=500, verbose_name='Descripción')
    total_dias = models.IntegerField(verbose_name='Total de días correspondientes')
    dias_habiles = models.BooleanField(default=True, verbose_name='Corresponde a días hábiles')

    def __str__(self):
        return '{} ({}-{})'.format(
                self.nombre,
                self.total_dias,
                '1' if self.dias_habiles else '0'
            )

    class Meta:
        verbose_name = u'Tipo de licencia'
        verbose_name_plural = u'Tipos de licencia'


class Licencia(models.Model):
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE, )
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
            self.contarto,
            self.tipo_licencia
        )

    class Meta:
        verbose_name = u'Licencia'
        verbose_name_plural = u'Licencias'


class Contrato(models.Model):
    CATEGORIAS = (
        (1, 'Docente Directivo'),
        (2, 'Docente'),
        (3, 'Asistente de Educación'),
        (4, 'Personal de la Fundación'),
        (5, 'Otro Profesional'),
    )

    TIPO_CONTRATO = (
        (1, 'Indefinido'),
        (2, 'A plazo'),
        (3, 'Reemplazo'),
    )

    TIPO_HORAS = (
        (1, 'Sostenedor'),
        (2, 'PIE'),
        (3, 'SEP'),
    )

    SALUD = (
        (1, 'Fonasa'),
        (2, 'Isapre'),
    )

    JORNADA = (
        (1, 'Completa'),
        (2, 'Media'),
        (3, 'Noche'),
    )

    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    colegio = models.ForeignKey('carga_horaria.Colegio', on_delete=models.CASCADE)
    categoria = models.PositiveSmallIntegerField(choices=CATEGORIAS, verbose_name='Categoría')
    funcion_principal = models.ForeignKey('Funcion', on_delete=models.CASCADE, related_name='funcion_principal', verbose_name='Función principal')
    funcion_secundaria = models.ForeignKey('Funcion', on_delete=models.CASCADE, related_name='funcion_secundaria', verbose_name='Función secundaria')
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO, verbose_name='Tipo de contrato')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de Término')
    horas = models.PositiveIntegerField(verbose_name='Horas contratadas')
    tipo_horas = models.PositiveSmallIntegerField(default=1, choices=TIPO_HORAS, verbose_name='Tipo de horas')
    reemplazando = models.ForeignKey('Contrato', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='En reemplazo de')
    salud = models.PositiveSmallIntegerField(default=1, choices=SALUD, verbose_name='Sistema de salud')
    isapre = models.ForeignKey('Isapre', on_delete=models.SET_NULL, null=True, blank=True)
    afp = models.ForeignKey('AFP', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='AFP')
    jornada_trabajo = models.PositiveSmallIntegerField(default=1, choices=JORNADA, verbose_name='Jornada de trabajo')
    hora_inicio_jornada = models.TimeField(verbose_name='Inicio de jornada')
    hora_termino_jornada = models.TimeField(verbose_name='Término de jornada')
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return '{}, {}'.format(
            self.persona,
            'Contratado' if self.vigente else 'Desvinculado'
        )

    class Meta:
        verbose_name = u'Contrato'
        verbose_name_plural = u'Contratos'


class Funcion(models.Model):
    TIPO_FUNCION = (
        (1, 'Funcion principal'),
        (2, 'Función secundaria')
    )

    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_FUNCION, verbose_name='Tipo de función')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Función'
        verbose_name_plural = u'Funciones'


class AFP(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'AFP'
        verbose_name_plural = u'AFPs'


class Isapre(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Isapre'
        verbose_name_plural = u'Isapres'


class Finiquito(models.Model):
    RAZONES = (
        (1, 'Término de contrato'),
        (2, 'Finiquito de mutuo acuerdo'),
        (3, 'Finiquito por parte del empleador'),
        (4, 'Renuncia voluntaria'),
    )
    contrato = models.OneToOneField('Contrato', on_delete=models.CASCADE)
    razon_baja = models.PositiveSmallIntegerField(default=1, choices=RAZONES, verbose_name='Razón de baja')
    descripcion = models.TextField(max_length=1500, verbose_name='Descripción')
    archivo = models.FileField(upload_to="rrhh/finiquitos", verbose_name='Finiquito')

    def __str__(self):
        return '{} - {}'.format(
            self.contrato,
            self.razon_baja
        )

    class Meta:
        verbose_name = u'Finiquito'
        verbose_name_plural = u'Finiquitos'
