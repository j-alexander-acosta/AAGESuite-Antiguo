from django.db import models


class Funcionario(models.Model):
    #TODO en la seccion del docente, donde hable del contrato, agregar si es misionero
    rut = models.CharField(max_length=16)
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
    antiguedad_docente_meses = models.PositiveIntegerField(verbose_name='Meses de antiguedad como docente', null=True, blank=True)
    fecha_ingreso_docente = models.DateField(verbose_name='Fecha de ingreso como docente', null=True, blank=True)
    antiguedad_sea_meses = models.PositiveIntegerField(verbose_name='Meses de antiguedad en el SEA', null=True, blank=True)
    fecha_ingreso_sea = models.DateField(verbose_name='Fecha de ingreso al SEA', null=True, blank=True)
    titulo = models.CharField(max_length=255, verbose_name='Título', null=True, blank=True)
    casa_formadora = models.CharField(max_length=255, null=True, blank=True)
    # añadir listado de archivos

    def __str__(self):
        return '{} {} {} ({})'.format(
            self.nombres,
            self.apellido_paterno,
            self.apellido_materno,
            self.rut
        )

    class Meta:
        verbose_name = u'Funcionario'
        verbose_name_plural = u'Funcionarios'

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

    funcionario = models.ForeignKey('Funcionario')
    entrevistador = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=FELICITACIONES, choices=TIPO_CHOICES)
    contenido = models.TextField()
    acuerdos = models.TextField()
    # añadir fecha

    def __str__(self):
        return self.funcionario

    class Meta:
        verbose_name = u'Funcionario'
        verbose_name_plural = u'Funcionarios'


class Archivo(models.Model):
    descripcion = models.CharField(max_length=255)
    archivo = models.FileField()
    funcionario = models.ForeignKey('Funcionario')


class Vacacion(models.Model):
    funcionario = models.ForeignKey('Funcionario')
    total_dias = models.IntegerField(verbose_name='Total de días de vacaciones')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    total_feriados = models.IntegerField(default=0, verbose_name='Total de feriados en el periodo de vacaciones')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de término')
    fecha_retorno = models.DateField(null=True, blank=True, verbose_name='Fecha de retorno')
    dias_pendiente = models.IntegerField(default=0, verbose_name='Días pendientes')
    es_pendiente = models.BooleanField(default=False, verbose_name='Corresponde a vacaciones pendientes')

    def __str__(self):
        return '{}, {}'.format(
            self.funcionario,
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
    funcionario = models.ForeignKey('Funcionario')
    tipo_licencia = models.ForeignKey('TipoLicencia', null=True, blank=True, verbose_name='Tipo de licencia')
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
            self.funcionario,
            self.tipo_licencia
        )

    class Meta:
        verbose_name = u'Licencia'
        verbose_name_plural = u'Licencias'
