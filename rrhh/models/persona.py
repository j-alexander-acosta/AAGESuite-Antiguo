from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rrhh.models.base import *
from rrhh.models.colegio import Colegio, ContratoColegio


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User)
    perfil = models.ForeignKey("Perfil", on_delete=models.CASCADE)
    nivel_acceso = models.PositiveSmallIntegerField(default=1, choices=NIVEL_ACCESO, verbose_name='Nivel de acceso')

    @property
    def es_admin_ue(self):
        return True if self.nivel_acceso >= 3 else False

    def __str__(self):
        return '{}, {} ({})'.format(
            self.usuario,
            self.perfil,
            self.nivel_acceso
        )

    class Meta:
        verbose_name = u'Perfil de usuario'
        verbose_name_plural = u'Perfiles de usuarios'


class Persona(models.Model):
    GENERO = (
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino')
    )
    NACIONALIDAD = (
        ('chilena', 'Chilena'),
        ('extranjera', 'Extranjera')
    )
    ESTADO_CIVIL = (
        ('soltero', 'Soltero'),
        ('casado', 'Casado'),
        ('divorsiado', 'Divorsiado'),
        ('viudo', 'Viudo')
    )

    rut = models.CharField(max_length=16, unique=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    genero = models.CharField(max_length=100, default='masculino', choices=GENERO, verbose_name='Género')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    nacionalidad = models.CharField(max_length=100, default='chilena', choices=NACIONALIDAD)
    estado_civil = models.CharField(max_length=100, default='soltero', choices=ESTADO_CIVIL)
    religion = models.BooleanField(default=True, verbose_name='Adventista del Séptimo día')
    direccion = models.CharField(max_length=255, verbose_name='Dirección')
    ciudad = models.ForeignKey('Ciudad', on_delete=models.SET_NULL, null=True, blank=True)
    telefono = models.PositiveIntegerField(verbose_name='Teléfono', help_text='Número de 9 dígitos')
    email = models.EmailField()
    titulado = models.BooleanField(default=False)
    profesion = models.CharField(max_length=255, null=True, blank=True, verbose_name='Título profesional', default='')
    usuario = models.OneToOneField(User, null=True, blank=True)
    foto = models.FileField(null=True, blank=True, upload_to="rrhh/fotos", verbose_name='Foto de perfil')
    curriculum = models.FileField(null=True, blank=True, upload_to="rrhh/curriculums")

    @property
    def get_name(self):
        return '{} {} {}'.format(
            self.nombres.split(' ')[0],
            self.apellido_paterno,
            self.apellido_materno
        )

    @property
    def get_short_name(self):
        return '{} {}'.format(
            self.nombres.split(' ')[0],
            self.apellido_paterno
        )

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
            if self.funcionario.contratocolegio_set.all():
                clasificacion = 'Postulante SEA'
            if self.funcionario.contratocolegio_set.filter(vigente=True):
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

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.title()
        self.apellido_paterno = self.apellido_paterno.capitalize()
        self.apellido_materno = self.apellido_materno.capitalize()
        self.direccion = self.direccion.title()
        self.profesion = self.profesion.title() if self.profesion else None
        self.email = self.email.lower()
        return super(Persona, self).save(*args, **kwargs)

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


class Perfeccionamiento(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, verbose_name='Nombre del título')
    es_educacion = models.BooleanField(default=True, verbose_name="Títulado en educación")
    area_titulo = models.ForeignKey(
        "AreaTitulo",
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Área del título"
    )
    especialidad = models.ForeignKey("Especialidad", on_delete=models.CASCADE, null=True, blank=True)
    mencion = models.ForeignKey("Mencion", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Mención")
    grado_academico = models.CharField(max_length=255, verbose_name='Grado académico')
    fecha_titulacion = models.DateField(verbose_name="Fecha de titulación")
    casa_formadora = models.CharField(max_length=255)

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
    tipo_misionero = models.PositiveSmallIntegerField(
        choices=TIPO_MISIONERO,
        null=True, blank=True,
        verbose_name='Tipo de Misionero'
    )
    puntos = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.persona)

    @staticmethod
    def contrato_vigente(id_colegio):
        colegio = get_object_or_404(
            Colegio,
            id=id_colegio
        )
        colegios = Colegio.objects.filter(fundacion=colegio.fundacion)

        return ContratoColegio.objects.filter(colegio__in=colegios, vigente=True).exists()

    class Meta:
        verbose_name = u'Funcionario'
        verbose_name_plural = u'Funcionarios'


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
            self.funcionario.persona,
            self.tipo_cuenta,
            self.banco
        )

    class Meta:
        verbose_name = u'Documento de funcionario'
        verbose_name_plural = u'Documentos de funcionarios'
