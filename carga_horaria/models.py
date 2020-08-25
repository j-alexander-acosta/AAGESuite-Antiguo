from enum import Enum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP, InvalidOperation


class Nivel(Enum):
    PK = "Pre kinder"
    K = "Kinder"
    B1 = "Primero básico"
    B2 = "Segundo básico"
    B3 = "Tercero básico"
    B4 = "Cuarto básico"
    B5 = "Quinto básico"
    B6 = "Sexto básico"
    B7 = "Séptimo básico"
    B8 = "Octavo básico"
    M1 = "Primero medio"
    M2 = "Segundo medio"
    M3 = "Tercero medio"
    M4 = "Cuarto medio"


class Plan(models.Model):
    nivel = models.CharField(max_length=8, choices=[(tag.name, tag.value) for tag in Nivel])
    colegio = models.ForeignKey('Colegio', null=True)

    def __str__(self): 
        return "Plan de Estudios - {} (ID: {})".format(getattr(Nivel, self.nivel).value.title(), self.pk)

    class Meta:
        verbose_name = u"Plan"
        verbose_name_plural = u"Planes"
        ordering = ["nivel"]

    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del plan
        :return: url
        """
        return reverse('carga-horaria:plan', args=[str(self.pk)])


class AsignaturaBase(models.Model):
    nombre = models.CharField(max_length=255)
    plan = models.ForeignKey('Plan')
    horas_jec = models.DecimalField(max_digits=4, decimal_places=2)
    horas_nec = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self): 
        return self.nombre


class Fundacion(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Colegio(models.Model):
    PAID = 1
    SHARED = 2
    FREE = 3
    FINANCING_CHOICES = ((PAID, 'particular pagado'),
                         (SHARED, 'financiamiento compartido'),
                         (FREE, 'gratuito'))
    
    nombre = models.CharField(max_length=255)
    abrev = models.CharField(max_length=10, blank=True, null=True)
    fundacion = models.ForeignKey('Fundacion', blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    rbd = models.CharField(max_length=255, blank=True, null=True)
    jec = models.BooleanField('JEC', default=True)
    pie = models.BooleanField('PIE', default=True)
    sep = models.BooleanField('SEP', default=True)
    web = models.URLField(max_length=255, blank=True, null=True)
    financiamiento = models.PositiveSmallIntegerField(default=PAID, choices=FINANCING_CHOICES)
    
    def __str__(self): 
        return self.nombre

    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del colegio
        :return: url
        """
        return reverse('carga-horaria:colegio', args=[str(self.pk)])

class Periodo(models.Model):
    plan = models.ForeignKey('Plan')
    nombre = models.CharField(max_length=255, blank=True, null=True)
    horas = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    horas_dif = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(22)])
    colegio = models.ForeignKey('Colegio')

    @property
    def floor(self):
        if self.colegio.jec:
            lookup = 'base__horas_jec'
        else:
            lookup = 'base__horas_nec'
        return sum(filter(None, self.asignatura_set.values_list(lookup, flat=True)))

    @property
    def ceiling(self):
        if self.colegio.jec:
            return self.floor + self.horas_dif + self.horas
        else:
            return self.floor + self.horas_dif

    @property
    def capacity(self):
        return sum(self.asignatura_set.values_list('horas', flat=True))

    @property
    def available(self):
        return self.ceiling - self.capacity

    @property
    def progress(self):
        return sum(Asignacion.objects.filter(asignatura__in=self.asignatura_set.all()).values_list('horas', flat=True))

    @property
    def completion_percentage(self):
        try:
            return round(self.progress * 100 / self.ceiling)
        except:
            return 0

    def __str__(self): 
        return "{} {}".format(getattr(Nivel, self.plan.nivel).value.title(), str(self.nombre or '')).strip()

    class Meta:
        verbose_name = u"Curso"
        verbose_name_plural = u"Cursos"
        ordering = ["plan"]
    
    def get_absolute_url(self):
        """
            Propiedad que retorna la ruta específica del detalle del período
        :return: url
        """
        return reverse('carga-horaria:periodo', args=[str(self.pk)])


class AsignaturaQuerySet(models.QuerySet):
    @property
    def base(self):
        return self.filter(base__isnull=False)

    @property
    def custom(self):
        return self.filter(base__isnull=True)


class Asignatura(models.Model):
    base = models.ForeignKey('AsignaturaBase', null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    periodo = models.ForeignKey('Periodo')
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    objects = AsignaturaQuerySet.as_manager()

    @property
    def horas_asignadas(self):
        return sum(self.asignacion_set.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return self.horas - self.horas_asignadas

    @property
    def completa(self):
        return self.horas_asignadas >= self.horas

    @property
    def profesores(self):
        return {ax.profesor for ax in self.asignacion_set.all()}

    def __str__(self): 
        return str(self.base or self.nombre)

    class Meta:
        ordering = ['base']


class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    horas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(44)])
    horas_no_aula = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(44)], default=0)
    especialidad = models.ForeignKey('Especialidad', verbose_name='título', blank=True, null=True)
    fundacion = models.ForeignKey('Fundacion', blank=True, null=True)
    colegio = models.ForeignKey('Colegio', null=True)
    adventista = models.BooleanField(default=False)

    @property
    def ceiling(self):
        return self.horas_contratadas

    @property
    def progress(self):
        return self.horas_asignadas_total_crono

    @property
    def get_progress_display(self):
        hours = int(self.progress)
        minutes = int(self.progress*60) % 60
        return "%d:%02d" % (hours, minutes)

    @property
    def completion_percentage(self):
        try:
            return round(self.progress * 100 / self.ceiling)
        except InvalidOperation:
            return 0

    @property
    def horas_contratadas(self):
        return self.horas + self.horas_no_aula

    @property
    def horas_asignadas_crono(self):
        return self.horas_asignadas * 45 / 60

    @property
    def horas_asignadas_total_crono(self):
        return Decimal(self.horas_no_lectivas_asignadas_anexo) + Decimal(self.horas_asignadas_crono) + Decimal(self.horas_no_aula_asignadas)

    @property
    def horas_asignadas(self):
        return sum(self.asignacion_set.values_list('horas', flat=True))

    @property
    def horas_asignadas_plan(self):
        return sum(self.asignacion_set.all().plan.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return self.horas_docentes - self.horas_asignadas

    @property
    def horas_no_lectivas_asignadas(self):
        return sum(self.asignacionextra_set.values_list('horas', flat=True)) + self.horas_planificacion

    @property
    def horas_no_lectivas_asignadas_anexo(self):
        return sum(self.asignacionextra_set.values_list('horas', flat=True)) + self.horas_planificacion + self.horas_recreo

    @property
    def horas_no_lectivas_disponibles(self):
        return self.horas_no_lectivas - self.horas_no_lectivas_asignadas

    @property
    def horas_no_aula_asignadas(self):
        return sum(self.asignacionnoaula_set.values_list('horas', flat=True))

    @property
    def horas_no_aula_disponibles(self):
        return self.horas_no_aula - self.horas_no_aula_asignadas

    @property
    def horas_docentes(self):
        # considerar luego 60/40 colegios vulnerables
        return Decimal(self.horas * Decimal(60.0)/Decimal(45.0) * Decimal(.65)).quantize(Decimal(0), rounding=ROUND_HALF_DOWN)

    @property
    def horas_lectivas(self):
        return Decimal(self.horas_docentes * Decimal(45.0)/Decimal(60.0)).quantize(Decimal('0.0'), rounding=ROUND_HALF_DOWN)

    @property
    def horas_no_lectivas(self):
        return Decimal(self.horas - self.horas_lectivas - self.horas_recreo).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)

    @property
    def horas_no_lectivas_anexo(self):
        return Decimal(self.horas - self.horas_lectivas).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)

    @property
    def horas_planificacion(self):
        return Decimal(self.horas_no_lectivas * Decimal(.40)).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)

    # FIXME: verificar según la tabla (horas recreo), puta locura
    @property
    def horas_recreo(self):
        return Decimal(self.horas * Decimal(4.1)/Decimal(60.0)).quantize(Decimal('0.0'), rounding=ROUND_HALF_DOWN)

    def __str__(self): 
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Asistente(models.Model):
    nombre = models.CharField(max_length=255)
    horas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(45)])
    funcion = models.CharField(max_length=255)
    fundacion = models.ForeignKey('Fundacion', blank=True, null=True)
    colegio = models.ForeignKey('Colegio', null=True)
    adventista = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class AsignacionQuerySet(models.QuerySet):
    @property
    def plan(self):
        return self.filter(tipo=Asignacion.PLAN)

    @property
    def sep(self):
        return self.filter(tipo=Asignacion.SEP)

    @property
    def pie(self):
        return self.filter(tipo=Asignacion.PIE)

    @property
    def sostenedor(self):
        return self.filter(tipo=Asignacion.SOSTENEDOR)


class Asignacion(models.Model):
    PLAN = 1
    SEP = 2
    PIE = 3
    SOSTENEDOR = 4

    TIPO_CHOICES = ((PLAN, 'plan'),
                    (SEP, 'SEP'),
                    (PIE, 'PIE'),
                    (SOSTENEDOR, 'Sostenedor'))

    profesor = models.ForeignKey('Profesor')
    asignatura = models.ForeignKey('Asignatura', null=True, blank=True)
    curso = models.ForeignKey('Periodo', null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.PositiveSmallIntegerField(default=PLAN)
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    objects = AsignacionQuerySet.as_manager()

    @property
    def horas_crono(self):
        return self.horas * 45 / 60

    def __str__(self): 
        return "{} - {} ({})".format(self.profesor, self.asignatura, self.horas)


class AsignacionExtra(models.Model):
    profesor = models.ForeignKey('Profesor')
    curso = models.ForeignKey('Periodo', null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self): 
        return "{} - {} ({})".format(self.profesor, self.descripcion, self.horas)


class AsignacionNoAulaQuerySet(models.QuerySet):
    @property
    def ordinaria(self):
        return self.filter(tipo=AsignacionNoAula.ORDINARIA)

    @property
    def sep(self):
        return self.filter(tipo=AsignacionNoAula.SEP)

    @property
    def pie(self):
        return self.filter(tipo=AsignacionNoAula.PIE)


class AsignacionNoAula(models.Model):
    ORDINARIA = 1
    SEP = 2
    PIE = 3

    TIPO_CHOICES = ((ORDINARIA, 'ordinaria'),
                    (SEP, 'SEP'),
                    (PIE, 'PIE'))

    profesor = models.ForeignKey('Profesor')
    curso = models.ForeignKey('Periodo', null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=ORDINARIA)
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    objects = AsignacionNoAulaQuerySet.as_manager()

    def __str__(self): 
        return "{} - {} ({})".format(self.profesor, self.descripcion, self.horas)


class Especialidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
