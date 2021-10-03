from enum import Enum
from itertools import tee, islice, chain
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_HALF_UP, InvalidOperation
from simple_history.models import HistoricalRecords
from .templatetags.carga_filters import decimal_maybe, hhmm
from .fucklogic import Ley20903
from django.shortcuts import get_object_or_404



def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


class BaseModel(models.Model):
    history = HistoricalRecords(inherit=True)
    created_at = models.DateTimeField(_('created at'),
                                      auto_now_add=True)

    def action_log(self, just=[]):
        fields = self.__class__._meta.fields
        filtered_fields = list(filter(lambda f: f.get_attname() in just, fields) if just else fields)
        field_names = [f.get_attname() for f in filtered_fields]
        historic_field_names = (just or field_names) + ['history_user_id', 'history_date']
        users = {None: 'sistema'}
        users.update({u.pk: u.username for u in get_user_model().objects.filter(id__in=self.history.values_list('history_user_id', flat=True).distinct())})
        rx = self.history.values(*historic_field_names)
        changes = []

        
        for prev, record, nxt in previous_and_next(rx):
            if nxt:
                changed_fields = [f for f in filtered_fields if record[f.get_attname()] != nxt[f.get_attname()]]
                verbose_changed_fields = [f.verbose_name for f in changed_fields]
                if changed_fields:
                    changes.append({'user': users[record['history_user_id']],
                                    'action': "cambió", #_('changed'),
                                    'changes': verbose_changed_fields,
                                    'current_values': {field.attname: record[field.attname] for field in changed_fields},
                                    'previous_values': {field.attname: nxt[field.attname] for field in changed_fields},
                                    'dt': record['history_date']})
            else:
                if not just:
                    changes.append({'user': users[record['history_user_id']],
                                    'action': "creó", #_('created'),
                                    'dt': record['history_date']})
        return changes

    @property
    def agent(self):
        try:
            return self.history.earliest().history_user
        except:
            return None
    
    @property
    def last_edited_by(self):
        try:
            return self.history.latest().history_user
        except:
            return None

    class Meta:
        abstract = True



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
    colegio = models.ForeignKey('Colegio', null=True, on_delete=models.CASCADE)

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
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
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
    FINANCING_CHOICES = ((PAID, 'Particular pagado'),
                         (SHARED, 'Financiamiento compartido'),
                         (FREE, 'Gratuito'))
    
    nombre = models.CharField(max_length=255)
    logo = models.FileField(null=True, blank=True, upload_to="carga_horaria/colegio/logos/", verbose_name='Logo del Colegio')
    abrev = models.CharField(max_length=10, blank=True, null=True)
    fundacion = models.ForeignKey('Fundacion', on_delete=models.CASCADE, blank=True, null=True)
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

    class Meta:
        unique_together = ['rbd', 'periode']


class Periodo(BaseModel):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    jec = models.BooleanField('JEC', default=True)
    horas = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    horas_dif = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    horas_adicionales = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE)
    profesor_jefe = models.ForeignKey('Profesor', blank=True, null=True, on_delete=models.SET_NULL)

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
        return self.plan.nivel in ['M3', 'M4'] and self.used_dif < self.horas_dif

    @property
    def used_dif(self):
        return sum(self.asignatura_set.all().dif.values_list('horas', flat=True))

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
        return sum([aa.horas_asignadas for aa in self.asignatura_set.all()])

    @property
    def completion_percentage(self):
        try:
            return min(round(self.progress * 100 / self.ceiling), 100)
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

    @property
    def dif(self):
        return self.filter(diferenciada=True)


class Asignatura(BaseModel):
    base = models.ForeignKey('AsignaturaBase', on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    periodos = models.ManyToManyField('Periodo')
    horas = models.DecimalField(max_digits=4, decimal_places=2)
    diferenciada = models.BooleanField(default=False)
    combinable = models.BooleanField(default=False)

    objects = AsignaturaQuerySet.as_manager()

    @property
    def co_docencia(self):
        return (len(set(self.asignacion_set.values_list('profesor', flat=True))) > 1) or self.overflow

    @property
    def overflow(self):
        asignadas = sum(self.asignacion_set.values_list('horas', flat=True))
        if asignadas > self.horas:
            return asignadas - self.horas

    @property
    def is_vuln(self):
        return any([pp.is_vuln for pp in self.periodos.all()])

    @property
    def profesores(self):
        return self.asignacion_set.values('profesor', flat=True)

    def get_cursos_display(self):
        return ', '.join(map(str, self.periodos.all()))

    def get_horas_display(self):
        if self.base and self.base.get_horas(self.periodos.first().jec) != self.horas:
            # import locale
            # locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
            horas_base = self.base.get_horas(self.periodos.first().jec)
            horas_extra = self.horas - horas_base
            if horas_base == Decimal('0.5') or horas_extra == Decimal('0.5'):
                return "{:.1f} + {:.1f}".format(horas_base, horas_extra)
            else:
                return "{:n} + {:n}".format(int(horas_base), int(horas_extra))
        else:
            if self.horas % 1 == 0:
                return int(self.horas)
            else:
                return "{:.1f}".format(self.horas).replace('.', ',')

    @property
    def horas_asignadas(self):
        asignadas = sum(self.asignacion_set.values_list('horas', flat=True))
        if asignadas > self.horas:
            return self.horas
        else:
            return asignadas

    @property
    def horas_disponibles(self):
        if self.horas_asignadas > self.horas:
            return 0
        else:
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


class Profesor(BaseModel):
    DOCENTE = 1
    RECTOR = 2
    DIRECTOR = 3
    SUBDIRECTOR = 4
    INSPECTOR = 5
    UTP = 6
    CAPELLAN = 7
    FINANCIERO = 8
    ORIENTADOR = 9
    CARGO_CHOICES = ((DOCENTE, 'Docente'),
                     (RECTOR, 'Rector'),
                     (DIRECTOR, 'Director'),
                     (SUBDIRECTOR, 'Subdirector'),
                     (INSPECTOR, 'Inspector General'),
                     (UTP, 'Jefe de UTP'),
                     (CAPELLAN, 'Capellán'),
                     (FINANCIERO, 'Administrador Financiero'),
                     (ORIENTADOR, 'Orientador'))

    INDEFINIDO = 1
    FIJO = 2
    REEMPLAZO = 3
    TIPO_CHOICES = ((INDEFINIDO, 'Indefinido'),
                    (FIJO, 'Plazo fijo'),
                    (REEMPLAZO, 'Reemplazo'))

    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField('Tipo de contrato', default=INDEFINIDO, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField('fecha inicio contrato', null=True)
    horas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(44)])
    horas_indefinidas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(44)])
    horas_plazo_fijo = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(44)])
    especialidad = models.ForeignKey('Especialidad', verbose_name='título', blank=True, null=True, on_delete=models.SET_NULL)
    fundacion = models.ForeignKey('Fundacion', blank=True, null=True, on_delete=models.SET_NULL)
    colegio = models.ForeignKey('Colegio', null=True, on_delete=models.SET_NULL)
    cargo = models.PositiveSmallIntegerField(default=DOCENTE, choices=CARGO_CHOICES)
    observaciones = models.TextField(default='', blank=True)

    def generar_anexo_1(self):
        from wkhtmltopdf.utils import render_pdf_from_template
        from django.template.loader import get_template
        ctx = {'profesor': self,
               'colegio': self.colegio,
               'periodo': self.colegio.periode}
        return (f"{self.persona.rut}_{self.colegio}_{self.colegio.periode}.pdf", render_pdf_from_template(get_template('carga_horaria/profesor/anexo_profesor.html'), None, None, ctx))

    @property
    def jefatura(self):
        return str(self.periodo_set.first())

    @property
    def es_profesor_jefe(self):
        return bool(self.periodo_set.count())

    @property
    def nombre(self):
        return self.persona.nombre

    @property
    def direccion(self):
        return self.persona.direccion

    @property
    def rut(self):
        return self.persona.rut

    @property
    def adventista(self):
        return self.persona.adventista

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
    def asignacion_periodo_anterior(self):
        anio_anterior = int(self.colegio.periode) - 1
        colegio = Colegio.objects.filter(nombre=self.colegio.nombre, periode=anio_anterior).first()
        profesor = get_object_or_404(Profesor, persona=self.persona, colegio=colegio)
        return profesor

    @property
    def horas_asignadas(self):
        return sum(self.asignacion_set.values_list('horas', flat=True))

    @property
    def horas_asignadas_plan(self):
        return sum([aa.horas for aa in filter(lambda aa: not aa.is_vuln, self.asignacion_set.all().plan)])

    @property
    def horas_asignadas_plan_vulnerables(self):
         return sum([aa.horas for aa in filter(lambda aa: aa.is_vuln, self.asignacion_set.all().plan)])

    @property
    def horas_asignadas_pie(self):
        return sum(self.asignacion_set.all().pie.values_list('horas', flat=True))

    @property
    def horas_asignadas_sep(self):
        return sum(self.asignacion_set.all().sep.values_list('horas', flat=True))

    @property
    def horas_asignadas_sostenedor(self):
        return sum(self.asignacion_set.all().sostenedor.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return (self.horas or 44) - self.horas_semanales_total

    @property
    def horas_no_lectivas_asignadas(self):
        return float(sum(self.asignacionextra_set.values_list('horas', flat=True))) + self.horas_planificacion + self.horas_recreo_total

    @property
    def horas_no_lectivas_asignadas_anexo(self):
        return float(sum(self.asignacionextra_set.values_list('horas', flat=True))) + float(sum(self.asignacionnoaula_set.values_list('horas', flat=True))) + self.horas_planificacion + self.horas_recreo_total

    @property
    def horas_no_lectivas_disponibles(self):
        return self.horas_no_lectivas_total + self.horas_recreo - self.horas_no_lectivas_asignadas

    @property
    def horas_no_aula_asignadas(self):
        return sum(self.asignacionnoaula_set.values_list('horas', flat=True))

    @property
    def horas_no_aula_asignadas_pie(self):
        return sum(self.asignacionnoaula_set.all().pie.values_list('horas', flat=True))

    @property
    def horas_no_aula_asignadas_sep(self):
        return sum(self.asignacionnoaula_set.all().sep.values_list('horas', flat=True))

    @property
    def horas_no_aula_asignadas_ordinaria(self):
        return sum(self.asignacionnoaula_set.all().ordinaria.values_list('horas', flat=True))

    @property
    def total_sep(self):
        return Ley20903(self.horas_asignadas_sep).horas_semanales + self.horas_no_aula_asignadas_sep

    @property
    def total_sep2(self):
        return self.horas_asignadas_sep + self.horas_no_aula_asignadas_sep

    @property
    def total_pie(self):
        return Ley20903(self.horas_asignadas_pie).horas_semanales + self.horas_no_aula_asignadas_pie

    @property
    def total_pie2(self):
        return self.horas_asignadas_pie + self.horas_no_aula_asignadas_pie

    @property
    def total_horas_detalle_profesor(self):
        return self.total_sep + self.total_pie + self.horas_sbvg_total

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
    def horas_sbvg(self):
        return self.horas_asignadas_plan

    @property
    def horas_sbvg_vulnerables(self):
        return self.horas_asignadas_plan_vulnerables

    @property
    def horas_semanales_sbvg(self):
        return Ley20903(self.horas_sbvg+self.horas_asignadas_sostenedor).horas_semanales

    @property
    def horas_semanales_sbvg_vulnerables(self):
        return Ley20903(self.horas_sbvg_vulnerables).horas_semanales_vulnerables

    @property
    def horas_sbvg_total2(self):
        return self.horas_asignadas_sostenedor + self.horas_no_aula_asignadas_ordinaria

    @property
    def horas_sbvg_total(self):
        return self.horas_semanales_sbvg + self.horas_semanales_sbvg_vulnerables + self.horas_no_aula_asignadas_ordinaria

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
        ordering = ('persona__nombre',)


class AsignacionAsistenteQuerySet(models.QuerySet):
    @property
    def normal(self):
        return self.filter(tipo=AsignacionAsistente.NORMAL)

    @property
    def no_aula(self):
        return self.filter(tipo=AsignacionAsistente.NO_AULA)

    @property
    def sep(self):
        return self.filter(tipo=AsignacionAsistente.SEP)

    @property
    def pie(self):
        return self.filter(tipo=AsignacionAsistente.PIE)


class AsignacionAsistenteLog(BaseModel):
    asistente = models.ForeignKey('Asistente', on_delete=models.CASCADE)
    mensaje = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created_at',)


class AsignacionAsistente(BaseModel):
    NORMAL = 1
    NO_AULA = 2
    SEP = 3
    PIE = 4

    TIPO_CHOICES = ((NORMAL, 'normal'),
                    (NO_AULA, 'no aula'),
                    (SEP, 'SEP'),
                    (PIE, 'PIE'))
    asistente = models.ForeignKey('Asistente', on_delete=models.CASCADE)
    curso = models.ForeignKey('Periodo', null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=NORMAL)
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    objects = AsignacionAsistenteQuerySet.as_manager()

    def __str__(self): 
        return "{} - {} ({})".format(self.asistente, self.descripcion, self.horas)


class Asistente(BaseModel):
    INDEFINIDO = 1
    FIJO = 2
    REEMPLAZO = 3
    TIPO_CHOICES = ((INDEFINIDO, 'Indefinido'),
                    (FIJO, 'Plazo fijo'),
                    (REEMPLAZO, 'Reemplazo'))

    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    horas = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(45)])
    funcion = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField('Tipo de contrato', default=INDEFINIDO, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField('fecha inicio contrato', null=True)
    fundacion = models.ForeignKey('Fundacion', blank=True, null=True, on_delete=models.SET_NULL)
    colegio = models.ForeignKey('Colegio', null=True, on_delete=models.SET_NULL)
    observaciones = models.TextField(default='', blank=True)

    def generar_anexo_1(self):
        from wkhtmltopdf.utils import render_pdf_from_template
        from django.template.loader import get_template
        ctx = {'profesor': self,
               'colegio': self.colegio,
               'periodo': self.colegio.periode}
        return (f"{self.persona.rut}_{self.colegio}_{self.colegio.periode}.pdf", render_pdf_from_template(get_template('carga_horaria/asistente/anexo_asistente.html'), None, None, ctx))

    @property
    def horas_sep(self):
        return sum(self.asignacionasistente_set.filter(tipo=AsignacionAsistente.SEP).values_list('horas', flat=True))

    @property
    def horas_pie(self):
        return sum(self.asignacionasistente_set.filter(tipo=AsignacionAsistente.PIE).values_list('horas', flat=True))

    @property
    def horas_sostenedor(self):
        return sum(self.asignacionasistente_set.filter(tipo=AsignacionAsistente.NO_AULA).values_list('horas', flat=True))

    @property
    def horas_sbvg(self):
        return self.horas_semanales_total - self.horas_sep - self.horas_pie

    @property
    def horas_semanales_total(self):
        return sum(self.asignacionasistente_set.values_list('horas', flat=True))

    @property
    def horas_disponibles(self):
        return (self.horas or 44) - self.horas_semanales_total

    @property
    def nombre(self):
        return self.persona.nombre

    @property
    def direccion(self):
        return self.persona.direccion

    @property
    def rut(self):
        return self.persona.rut

    @property
    def adventista(self):
        return self.persona.adventista

    def __str__(self):
        return self.nombre


class AsignacionQuerySet(models.QuerySet):
    @property
    def sorted(self):
        ordering = {str(value): index for index, value in enumerate(Nivel)}
        def kei(x):
            try:
                return ordering["Nivel."+x.asignatura.periodos.first().plan.nivel]
            except AttributeError:
                return 14
        return sorted(self, key=kei)

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


class AsignacionLog(BaseModel):
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    mensaje = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created_at',)


class Asignacion(BaseModel):
    PLAN = 1
    SEP = 2
    PIE = 3
    SOSTENEDOR = 4

    TIPO_CHOICES = ((PLAN, 'plan'),
                    (SEP, 'SEP'),
                    (PIE, 'PIE'),
                    (SOSTENEDOR, 'Sostenedor'))

    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', null=True, blank=True, on_delete=models.SET_NULL)
    curso = models.ForeignKey('Periodo', null=True, blank=True, on_delete=models.SET_NULL)  # TODO: mark for deletion, this isn't used
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

    @property
    def desc(self):
        return self.descripcion or f"{self.asignatura} - {self.asignatura.get_cursos_display()}"

    def __str__(self): 
        return "horas lectivas ({} - {})".format(decimal_maybe(self.horas), self.desc)


class AsignacionExtra(BaseModel):
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    curso = models.ForeignKey('Periodo', null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=255)
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self): 
        return "horas no lectivas ({} - {}))".format(hhmm(self.horas), self.descripcion)


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


class AsignacionNoAula(BaseModel):
    ORDINARIA = 1
    SEP = 2
    PIE = 3

    TIPO_CHOICES = ((ORDINARIA, 'ordinaria'),
                    (SEP, 'SEP'),
                    (PIE, 'PIE'))

    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    curso = models.ForeignKey('Periodo', null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(default=ORDINARIA)
    horas = models.DecimalField(max_digits=4, decimal_places=2)

    objects = AsignacionNoAulaQuerySet.as_manager()

    def __str__(self): 
        return "horas no lectivas ({} - {}))".format(hhmm(self.horas), self.descripcion)


class Especialidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre',)


class Persona(models.Model):
    SOLTERO = 1
    CASADO = 2
    SEPARADO = 3
    DIVORCIADO = 4
    VIUDO = 5

    ESTADO_CIVIL_CHOICES = ((SOLTERO, 'Soltero(a)'),
                            (CASADO, 'Casado(a)'),
                            (SEPARADO, 'Separado(a)'),
                            (DIVORCIADO, 'Divorciado(a)'),
                            (VIUDO, 'Viudo(a)'))

    rut = models.CharField(max_length=13, blank=True, null=True, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField('dirección', max_length=255)
    comuna = models.CharField('comuna', max_length=255)
    nacionalidad = models.CharField('nacionalidad', max_length=255)
    telefono = models.CharField('teléfono', max_length=255)
    email_personal = models.EmailField('email personal')
    email_institucional = models.EmailField('email institucional')
    estado_civil = models.PositiveSmallIntegerField(default=SOLTERO, choices=ESTADO_CIVIL_CHOICES)
    discapacidad = models.BooleanField('discapacidad', default=False)
    recibe_pension = models.BooleanField('recibe pensión', default=False)
    adventista = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField('fecha de nacimiento', null=True)

    def __str__(self):
        return "{} ({})".format(self.nombre, self.rut)

class Document(models.Model):
    title = models.CharField(max_length = 50)
    uploadedFile = models.FileField(upload_to = "Uploaded Files/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)