from enum import Enum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP, InvalidOperation
from .fucklogic import Ley20903


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

    def refresh_asignaturas(self):
        for periodo in self.periodo_set.all():
            periodo.refresh()

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

    def get_horas(self, jec=True):
        if jec:
            return self.horas_jec
        else:
            return self.horas_nec

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
    rbd = models.CharField(max_length=255, blank=True, null=True, unique=True)
    jec = models.BooleanField('JEC', default=True)
    pie = models.BooleanField('PIE', default=True)
    sep = models.BooleanField('SEP', default=True)
    web = models.URLField(max_length=255, blank=True, null=True)
    financiamiento = models.PositiveSmallIntegerField(default=PAID, choices=FINANCING_CHOICES)
    alumnos = models.PositiveIntegerField(default=0)
    prioritarios = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    periode = models.PositiveSmallIntegerField(default=2020)
    
    @property
    def is_vuln(self):
        return self.prioritarios >= 80

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
    jec = models.BooleanField('JEC', default=True)
    horas = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    horas_dif = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    horas_adicionales = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    colegio = models.ForeignKey('Colegio')
    profesor_jefe = models.ForeignKey('Profesor', blank=True, null=True)

    @property
    def is_vuln(self):
        return self.colegio.is_vuln and self.plan.nivel in ['PK', 'K', 'B1', 'B2', 'B3', 'B4']

    def refresh(self):
        own = {aa.pop('base__pk'): aa for aa in self.asignatura_set.filter(base__isnull=False).values('pk', 'base__pk', 'horas')}
        plan = {ab.pop('pk'): ab for ab in self.plan.asignaturabase_set.values('pk', 'horas_jec', 'horas_nec')}

        # delete if not found in plan
        to_delete = own.keys() - plan.keys()
        for base__pk in to_delete:
            Asignatura.objects.get(pk=own[base__pk]['pk']).delete()
            del own[base__pk]

        # update hours if different with plan hours
        for base_pk, values in own.items():
            current_hours = values['horas']
            if self.jec:
                base_hours = plan[base_pk]['horas_jec']
            else:
                base_hours = plan[base_pk]['horas_nec']

            if current_hours != base_hours:
                aa = Asignatura.objects.get(pk=values['pk'])
                aa.asignacion_set.all().delete()
                aa.horas = base_hours
                aa.save()

        # add new asignaturas if not found in periodo
        to_add = plan.keys() - own.keys()
        for base_pk in to_add:
            if self.jec:
                horas = plan[base_pk]['horas_jec']
            else:
                horas = plan[base_pk]['horas_nec']

            base = AsignaturaBase.objects.get(pk=base_pk)
            aa = Asignatura.objects.create(base=base, horas=horas)
            aa.periodos.add(self)

    @property
    def used_ld_hours(self):
        return min(self.base_capacity - self.floor, self.horas)

    @property
    def used_additional_hours(self):
        return max(0, min(self.capacity - self.horas - self.floor, self.horas_adicionales))

    @property
    def can_dif(self):
        return self.plan.nivel in ['M3', 'M4']

    @property
    def floor(self):
        if self.jec:
            lookup = 'base__horas_jec'
        else:
            lookup = 'base__horas_nec'
        return sum(filter(None, self.asignatura_set.values_list(lookup, flat=True)))

    @property
    def ceiling(self):
        if self.jec:
            return self.floor + self.horas_dif + self.horas_adicionales + self.horas
        else:
            return self.floor + self.horas_dif + self.horas_adicionales

    @property
    def base_capacity(self):
        return sum(self.asignatura_set.exclude(diferenciada=True).values_list('horas', flat=True))

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
    periodos = models.ManyToManyField('Periodo')
    horas = models.DecimalField(max_digits=4, decimal_places=2)
    diferenciada = models.BooleanField(default=False)

    objects = AsignaturaQuerySet.as_manager()

    @property
    def is_vuln(self):
        return any([pp.is_vuln for pp in self.periodos.all()])

    @property
    def profesores(self):
        return self.asignacion_set.values('profesor', flat=True)

    def get_horas_display(self):
        if self.base and self.base.get_horas(self.periodos.first().jec) != self.horas:
            # import locale
            # locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
            horas_base = self.base.get_horas(self.periodos.first().jec)
            horas_extra = self.horas - horas_base
            return "{:n} + {:n}".format(int(horas_base), int(horas_extra))
        else:
            return int(self.horas)

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
    DOCENTE = 1
    RECTOR = 2
    DIRECTOR = 3
    SUBDIRECTOR = 4
    INSPECTOR = 5
    UTP = 6
    CAPELLAN = 7
    CARGO_CHOICES = ((DOCENTE, 'Docente'),
                     (RECTOR, 'Rector'),
                     (DIRECTOR, 'Director'),
                     (SUBDIRECTOR, 'Subdirector'),
                     (INSPECTOR, 'Inspector General'),
                     (UTP, 'Jefe de UTP'),
                     (CAPELLAN, 'Capellán'))

    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=13, blank=True, null=True, unique=True)
    horas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(44)])
    especialidad = models.ForeignKey('Especialidad', verbose_name='título', blank=True, null=True)
    fundacion = models.ForeignKey('Fundacion', blank=True, null=True)
    colegio = models.ForeignKey('Colegio', null=True)
    adventista = models.BooleanField(default=False)
    directivo = models.BooleanField(default=False)
    cargo = models.PositiveSmallIntegerField(default=DOCENTE, choices=CARGO_CHOICES)

    @property
    def ceiling(self):
        return self.horas_contratadas or 44

    @property
    def progress(self):
        return self.horas_semanales_total

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
        return self.horas

    @property
    def horas_asignadas_crono(self):
        return self.horas_asignadas * 45 / 60

    @property
    def horas_asignadas(self):
        return sum(self.asignacion_set.values_list('horas', flat=True))

    @property
    def horas_asignadas_plan(self):
        return sum(self.asignacion_set.all().plan.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return (self.horas or 44) - self.horas_semanales_total

    @property
    def horas_no_lectivas_asignadas(self):
        return float(sum(self.asignacionextra_set.values_list('horas', flat=True))) + self.horas_planificacion

    @property
    def horas_no_lectivas_asignadas_anexo(self):
        return float(sum(self.asignacionextra_set.values_list('horas', flat=True))) + self.horas_planificacion + self.horas_recreo

    @property
    def horas_no_lectivas_disponibles(self):
        return self.horas_no_lectivas_total - self.horas_no_lectivas_asignadas

    @property
    def horas_no_aula_asignadas(self):
        return sum(self.asignacionnoaula_set.values_list('horas', flat=True))

    @property
    def horas_no_aula_disponibles(self):
        return self.horas_disponibles

    @property
    def horas_semanales_total(self):
        return self.horas_semanales + self.horas_semanales_vulnerables + self.horas_no_aula_asignadas

    @property
    def horas_semanales(self):
        return Ley20903(self.horas_docentes).horas_semanales

    @property
    def horas_semanales_vulnerables(self):
        return Ley20903(self.horas_docentes_vulnerables).horas_semanales_vulnerables

    @property
    def horas_docentes_total(self):
        return self.horas_docentes + self.horas_docentes_vulnerables

    @property
    def horas_docentes(self):
        return sum([aa.horas for aa in filter(lambda aa: not aa.is_vuln, self.asignacion_set.all())])

    @property
    def horas_docentes_vulnerables(self):
        return sum([aa.horas for aa in filter(lambda aa: aa.is_vuln, self.asignacion_set.all())])

    @property
    def horas_lectivas_total(self):
        return self.horas_lectivas + self.horas_lectivas_vulnerables

    @property
    def horas_lectivas(self):
        return Ley20903(self.horas_docentes).horas_lectivas

    @property
    def horas_lectivas_vulnerables(self):
        return Ley20903(self.horas_docentes_vulnerables).horas_lectivas_vulnerables

    @property
    def horas_recreo_total(self):
        return self.horas_recreo + self.horas_recreo_vulnerables
        
    @property
    def horas_recreo(self):
        return Ley20903(self.horas_docentes).horas_recreo

    @property
    def horas_recreo_vulnerables(self):
        return Ley20903(self.horas_docentes_vulnerables).horas_recreo_vulnerables

    @property
    def horas_no_lectivas_total(self):
        return self.horas_no_lectivas + self.horas_no_lectivas_vulnerables

    @property
    def horas_no_lectivas(self):
        return Ley20903(self.horas_docentes).horas_no_lectivas

    @property
    def horas_no_lectivas_vulnerables(self):
        return Ley20903(self.horas_docentes_vulnerables).horas_no_lectivas_vulnerables

    @property
    def horas_no_lectivas_anexo(self):
        return Decimal(float(self.horas) - self.horas_lectivas_total)

    @property
    def horas_planificacion(self):
        return self.horas_no_lectivas_total * 0.4

    def __str__(self): 
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Asistente(models.Model):
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=13, blank=True, null=True, unique=True)
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
    def sorted(self):
        ordering = {str(value): index for index, value in enumerate(Nivel)}
        return sorted(self, key=lambda x: ordering["Nivel."+x.asignatura.periodos.first().plan.nivel])

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
    horas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.5)])

    objects = AsignacionQuerySet.as_manager()

    @property
    def is_vuln(self):
        if self.asignatura:
            return self.asignatura.is_vuln
        else:
            return False

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
