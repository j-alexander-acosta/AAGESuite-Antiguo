from django.db import models
from .base import *


class Persona(models.Model):
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
    comuna = models.CharField(max_length=255, default='')
    ciudad = models.CharField(max_length=255, default='')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    email = models.EmailField()
    titulado = models.BooleanField(default=False)
    profesion = models.CharField(max_length=255, null=True, blank=True, verbose_name='Profesión', default='')

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

    @property
    def clasificacion(self):
        clasificacion = 'Postulante'
        try:
            if self.funcionario.contrato_set.all():
                clasificacion = 'Postulante SEA'
            if self.funcionario.contrato_set.filter(vigente=True):
                clasificacion = 'Funcionario'
        except:
            pass
        return clasificacion

    @property
    def historial(self):
        return {
            'union': self.funcionario.contratounion_set.all(),
            'fundacion': self.funcionario.contratofundacion_set.all(),
            'colegio': self.funcionario.contratocolegio_set.all()
        }


class Perfeccionamiento(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    casa_formadora = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255, verbose_name='Título')
    grado_academico = models.CharField(max_length=255, verbose_name='Grado académico')
    fecha_titulacion = models.DateField()
    documento_respaldo = models.FileField(verbose_name='Documento de respaldo')

    def __str__(self):
        return '{}, {}'.format(
            self.persona.get_full_name,
            self.titulo
        )

    class Meta:
        verbose_name = u'Perfeccionamiento de persona'
        verbose_name_plural = u'Perfeccionamientos de personas'


class Funcionario(models.Model):
    persona = models.OneToOneField('Persona', on_delete=models.CASCADE)
    salud = models.PositiveSmallIntegerField(default=1, choices=PREVISION_SALUD, verbose_name='Sistema de salud')
    isapre = models.ForeignKey('Isapre', on_delete=models.SET_NULL, null=True, blank=True)
    afp = models.ForeignKey('AFP', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='AFP')
    fecha_ingreso_docente = models.DateField(verbose_name='Fecha de ingreso como docente', null=True, blank=True)
    fecha_ingreso_sea = models.DateField(verbose_name='Fecha de ingreso al SEA', null=True, blank=True)
    estado = models.PositiveSmallIntegerField(default=1, choices=TIPO_FUNCIONARIO, verbose_name='Estado funcionario')
    tipo_misionero = models.PositiveSmallIntegerField(choices=TIPO_MISIONERO, null=True, blank=True, verbose_name='Tipo de Misionero')
    puntos = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.persona)

    def contrato_vigente(self, id_colegio):
        colegio = get_object_or_404(
            Colegio,
            id=id_colegio
        )
        colegios = Colegio.objects.filter(fundacion=colegio.fundacion)

        return ContratoColegio.objects.filter(colegio__in=colegios, vigente=True).exists()

    class Meta:
        verbose_name = u'Funcionario'
        verbose_name_plural = u'Funcionarios'


class DocumentoFuncionario(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    tipo_documento = models.ForeignKey(TipoDocumento, null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=255)
    documento = models.FileField()

    def __str__(self):
        return '{}, {}'.format(
            self.funcionario.persona.get_full_name,
            self.tipo_documento
        )

    class Meta:
        verbose_name = u'Documento de funcionario'
        verbose_name_plural = u'Documentos de funcionarios'


class DatosBancarios(models.Model):
    TIPO_CUENTA = (
        (1, 'Cuenta vista'),
        (2, 'Cuenta corriente'),
        (3, 'Chequera electrónica')
    )
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    tipo_cuenta = models.PositiveSmallIntegerField(default=1, choices=TIPO_CUENTA)
    numero = models.PositiveIntegerField()

    def __str__(self):
        return '{}, {} - {}'.format(
            self.funcionario.persona.get_full_name,
            self.tipo_cuenta,
            self.banco
        )

    class Meta:
        verbose_name = u'Documento de funcionario'
        verbose_name_plural = u'Documentos de funcionarios'
