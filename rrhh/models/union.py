from django.db import models
from .base import *
from .persona import Funcionario


class Union(models.Model):
    nombre = models.CharField(max_length=250)
    abrev = models.CharField(max_length=50,verbose_name="Abreviación")
    descripcion = models.TextField(max_length=2500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return '{}@{}'.format(
            self.nombre,
            self.abrev
        )

    class Meta:
        verbose_name = u'Unión'
        verbose_name_plural = u'Uniones'


class ContratoUnion(models.Model):
    CATEGORIAS = (
        (1, 'Personal de unión'),
        (2, 'Otro Profesional'),
    )

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    union = models.ForeignKey('Union', on_delete=models.CASCADE, verbose_name='Unión')
    categoria = models.PositiveSmallIntegerField(choices=CATEGORIAS, verbose_name='Categoría')
    tipo_contrato = models.PositiveSmallIntegerField(default=1, choices=TIPO_CONTRATO, verbose_name='Tipo de contrato')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_termino = models.DateField(null=True, blank=True, verbose_name='Fecha de Término')
    reemplazando = models.ForeignKey('ContratoUnion', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='En reemplazo de')
    horas_total = models.PositiveIntegerField(verbose_name='Horas contratadas')
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(
            self.funcionario,
            self.fundacion.abrev
        )

    @property
    def periodo_contrato(self):
        return '{} - {}'.format(
            self.fecha_inicio,
            self.fecha_termino if self.fecha_termino else 'indefinido'
        )

    class Meta:
        verbose_name = u'Contrato de unión'
        verbose_name_plural = u'Contratos de uniones'


class FiniquitoUnion(models.Model):
    contrato = models.OneToOneField('ContratoUnion', on_delete=models.CASCADE)
    razon_baja = models.PositiveSmallIntegerField(default=1, choices=RAZON_FINIQUITO, verbose_name='Razón de baja')
    descripcion = models.TextField(max_length=1500, verbose_name='Descripción')
    archivo = models.FileField(upload_to="rrhh/finiquitos", verbose_name='Finiquito')

    def __str__(self):
        return '{}, {}'.format(
            self.contrato,
            self.razon_baja
        )

    class Meta:
        verbose_name = u'Finiquito de empleado de unión'
        verbose_name_plural = u'Finiquitos de empleados de uniones'


class VacacionFuncionarioUnion(models.Model):
    contrato = models.ForeignKey('ContratoUnion', on_delete=models.CASCADE)
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
        verbose_name = u'Vacación de empleado de unión'
        verbose_name_plural = u'Vacaciones de empleados de uniones'

    @property
    def dias_correspondientes(self):
        # TODO crear funcion dias correspondientes, apartir de la antiguedad del funcionario
        dias = 0
        return dias


class LicenciaFuncionarioUnion(models.Model):
    contrato = models.ForeignKey('ContratoUnion', on_delete=models.CASCADE, )
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
        verbose_name = u'Licencia de empleado de unión'
        verbose_name_plural = u'Licencias de empleados de uniones'
