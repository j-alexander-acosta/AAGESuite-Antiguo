from django.conf import settings
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .viewsAlexis import *
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Periodo, Colegio, Plan
from carga_horaria.formsDani import PeriodoForm, ColegioForm, PlanForm
from django.core.urlresolvers import reverse_lazy, reverse
from guardian.shortcuts import get_objects_for_user
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from wkhtmltopdf.views import PDFTemplateResponse, PDFTemplateView
from .models import Nivel
from .models import Profesor
from .models import Periodo
from .models import Asignacion
from .models import AsignacionExtra
from .models import AsignacionNoAula
from .models import Colegio
from .forms import AsignacionForm
from .forms import AsignacionUpdateForm
from .forms import AsignacionFUAForm
from .forms import AsignacionNoAulaFUAForm
from .forms import AsignacionFUAUpdateForm
from .forms import AsignacionNoAulaFUAUpdateForm
from .forms import AsignacionExtraForm
from .forms import AsignacionExtraUpdateForm
from .forms import AsignacionNoAulaForm
from .forms import AsignacionNoAulaUpdateForm
from .forms import AssignPermForm
from .formsDani import PlantillaPlanForm


@login_required
def assign(request):
    if not request.user.is_superuser:
        raise Http404

    year = request.session.get('periodo', 2020)
    if request.method == 'POST':
        form = AssignPermForm(request.POST, year=year)
        if form.is_valid():
            user = form.cleaned_data['usuario']

            # clear perms first
            remove_perm('carga_horaria.change_colegio', user, get_objects_for_user(user, 'carga_horaria.change_colegio').filter(periode=year))

            for c in form.cleaned_data['colegios']:
                assign_perm('change_colegio', user, c)
        
    form = AssignPermForm(year=year)
    return render(request, 'carga_horaria/assign.html', {'form': form})



@login_required
def switch_periodo(request, year=2020):
    request.session['periodo'] = year
    try:
        del request.session['colegio__pk']
        del request.session['colegio__nombre']
    except KeyError:
        pass
    return redirect('carga-horaria:home')

@login_required
def switch(request, pk=None):
    if pk:
        colegio = get_object_or_404(Colegio, pk=pk)
        request.session['colegio__pk'] = colegio.pk
        request.session['colegio__nombre'] = colegio.nombre
        return redirect('carga-horaria:home')
    colegios = get_objects_for_user(request.user, "carga_horaria.change_colegio", Colegio.objects.filter(periode=request.session.get('periodo', 2020)))
    return render(request, 'carga_horaria/switch.html', {'colegios': colegios})

@login_required
def clear(request):
    del request.session['colegio__pk']
    del request.session['colegio__nombre']
    return redirect('carga-horaria:home')

@login_required
def home(request):
    return render(request, 'carga_horaria/home.html')



@login_required
def anexo(request, pk):
    p = get_object_or_404(Profesor, pk=pk)
    ax = [{'descripcion': 'Planificación', 'curso': '', 'horas': p.horas_planificacion},
          {'descripcion': 'Recreo', 'curso': '', 'horas': p.horas_recreo}] + list(p.asignacionextra_set.all())

    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/profesor/anexo_profesor.html',
                                   filename='anexo1.pdf',
                                   context={'asignaciones': p.asignacion_set.all(),
                                            'asignaciones_extra': ax,
                                            'profesor': p},
                                   show_content_in_browser=settings.DEBUG)
    return response


@login_required
def profesores_pdf(request):
    profesores = get_for_user(request, Profesor.objects.all(), 'fundacion__colegio__pk', request.user)
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/profesor/listado_profesor_pdf.html',
                                   filename='listado_profesores.pdf',
                                   context={'profesores': profesores},
                                   show_content_in_browser=settings.DEBUG)
    return response


@login_required
def asistentes_pdf(request):
    asistentes = get_for_user(request, Asistente.objects.all(), 'fundacion__colegio__pk', request.user)
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/asistente/listado_asistente_pdf.html',
                                   filename='listado_asistentes.pdf',
                                   context={'asistentes': asistentes},
                                   show_content_in_browser=settings.DEBUG)
    return response

@login_required
def periodo_pdf(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    response = PDFTemplateResponse(request=request,
                                   template='carga_horaria/periodo/periodo_pdf.html',
                                   filename='carga_horaria.pdf',
                                   context={'object': periodo},
                                   show_content_in_browser=settings.DEBUG)
    return response

@login_required
def plan_refresh(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.refresh_asignaturas()
    messages.success(request, "Se han actualizado los cursos asociados al plan ID: {}".format(plan.pk))
    return redirect('carga-horaria:planes')

# class AnexoView(PDFTemplateView):
#     template_name = 'carga_horaria/profesor/anexo_profesor.html'
#     filename = 'anexo1.pdf'

#     def get(self, request, *args, **kwargs):
#         pk = kwargs.pop('pk')
#         self.p = get_object_or_404(Profesor, pk=pk)
#         self.ax = [{'descripcion': 'Planificación', 'curso': '', 'horas': self.p.horas_planificacion},
#                    {'descripcion': 'Recreo', 'curso': '', 'horas': self.p.horas_recreo}] + list(self.p.asignacionextra_set.all())
#         return super(AnexoView, self).get(request, *args, **kwargs)

#     def get_context_data(self, *args, **kwargs):
#         ctx = super(AnexoView, self).get_context_data(*args, **kwargs)
#         ctx.update({'asignaciones': self.p.asignacion_set.all(),
#                     'asignaciones_extra': self.ax,
#                     'profesor': self.p})

# anexo = AnexoView.as_view()


"""
    Comienzo Crud Periodos
"""
class PeriodoListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de periodos
    """
    model = Periodo
    lookup = 'colegio__pk'
    template_name = 'carga_horaria/periodo/listado_periodos.html'
    search_fields = ['nombre', 'colegio']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        ctx = super(PeriodoListView, self).get_context_data(*args, **kwargs)
        ox = ctx['object_list']
        ordering = {str(value): index for index, value in enumerate(Nivel)}
        ctx['object_list'] = sorted(ox, key=lambda x: ordering["Nivel."+x.plan.nivel])
        # added for convenience, pasted from AsignaturaBaseListView
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(plan__nivel=nivel)

        return qs




class PeriodoDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de Periodo
    """
    model = Periodo
    template_name = 'carga_horaria/periodo/detalle_periodo.html'


class PeriodoCreateView(LoginRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/nuevo_periodo.html'
    success_url = reverse_lazy('carga-horaria:periodos')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PeriodoCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs


class PeriodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/editar_periodo.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PeriodoUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PeriodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Periodo
    success_url = reverse_lazy('carga-horaria:periodos')
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""
    Fin Crud Periodos
"""

"""
    Comienzo Crud Colegios
"""
class ColegioListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de periodos
    """
    model = Colegio
    lookup = 'pk'
    template_name = 'carga_horaria/colegio/listado_colegios.html'
    search_fields = ['nombre', 'jec']
    paginate_by = 6


class ColegioDetailView(LoginRequiredMixin, ObjPermissionRequiredMixin, DetailView):
    """
        Detalle de Colegio
    """
    model = Colegio
    permission = 'carga_horaria.change_colegio'
    template_name = 'carga_horaria/colegio/detalle_colegio.html'


class ColegioCreateView(LoginRequiredMixin, CreateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'carga_horaria/colegio/nuevo_colegio.html'
    success_url = reverse_lazy('carga-horaria:colegios')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."

    def form_valid(self, form):
        colegio = form.save(commit=False)
        colegio.periode = self.request.session.get('periodo', 2020)
        colegio.save()
        return redirect(reverse('carga-horaria:colegios'))


class ColegioUpdateView(LoginRequiredMixin, UpdateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'carga_horaria/colegio/editar_colegio.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:colegio',
            kwargs={
                'pk': self.object.pk,
            }
        )



class ColegioDeleteView(LoginRequiredMixin, DeleteView):
    model = Colegio
    success_url = reverse_lazy('carga-horaria:colegios')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


"""
    Fin Crud Colegios
"""

"""
    Comienzo Crud Planes
"""
class PlanListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de planes
    """
    model = Plan
    lookup = 'colegio__pk'
    template_name = 'carga_horaria/plan/listado_planes.html'
    search_fields = ['nombre', 'nivel']
    paginate_by = 10
    ordering = ['-pk']


class PlanDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de Plan
    """
    model = Plan
    template_name = 'carga_horaria/plan/detalle_plan.html'


class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/nuevo_plan.html'
    success_url = reverse_lazy('carga-horaria:planes')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PlanCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs


@login_required
def crear_desde_plantilla(request):
    if request.method == 'POST':
        form = PlantillaPlanForm(request.POST)
        if form.is_valid():
            plantilla = form.cleaned_data['plantilla']
            nivel = form.cleaned_data['nivel']

            colegio_pk = request.session.get('colegio__pk', None)
            if colegio_pk:
                colegio = Colegio.objects.get(pk=colegio_pk)
                nuevo = Plan.objects.create(nivel=nivel, colegio=colegio)
            else:
                nuevo = Plan.objects.create(nivel=nivel)
            for ab in plantilla.asignaturabase_set.all():
                AsignaturaBase.objects.create(nombre=ab.nombre,
                                              plan=nuevo,
                                              horas_jec=ab.horas_jec,
                                              horas_nec=ab.horas_nec)
            return redirect('carga-horaria:planes')
    else:
        form = PlantillaPlanForm()
    return render(request, 'carga_horaria/plantilla.html', {'form': form})


class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/editar_plan.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:plan',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('carga-horaria:planes')
    template_name = 'carga_horaria/plan/eliminar_plan.html'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""
    Fin Crud Planes
"""

@login_required
def asignatura_limpiar(request, pk, periodo_pk):
    aa = get_object_or_404(Asignatura, pk=pk)
    aa.asignacion_set.all().delete()
    return redirect(reverse('carga-horaria:periodo', kwargs={'pk': periodo_pk}))


@login_required
def asignatura_dif(request, pk):
    pp = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        # check first if there are any candidates for merging
        nombre = request.POST['asignatura']
        colegio_pk = request.session.get('colegio__pk', None)
        can_confirm = request.POST.get('can_confirm', False)
        if colegio_pk and Asignatura.objects.filter(periodos__colegio=colegio_pk, nombre=nombre) and not can_confirm:
            ax = Asignatura.objects.filter(periodos__colegio=colegio_pk, nombre=nombre).distinct()
            return render(request, 'carga_horaria/asignatura/asignatura_dif_confirm.html', {'object': pp,
                                                                                            'candidatas': ax})
        else:
            aa = Asignatura.objects.create(nombre=request.POST['asignatura'],
                                           diferenciada=True,
                                           horas=6)
            aa.periodos.add(pp)
            return redirect('carga-horaria:periodo', pp.pk)
    return render(request, 'carga_horaria/asignatura/asignatura_dif.html', {'object': pp})


@login_required
def asignatura_merge(request, pk, asignatura_pk):
    pp = get_object_or_404(Periodo, pk=pk)
    aa = get_object_or_404(Asignatura, pk=asignatura_pk)
    aa.periodos.add(pp)
    return redirect('carga-horaria:periodo', pk)


@login_required
def asignatura_maybe(request, pk):
    pp = get_object_or_404(Periodo, pk=pk)
    candidatas = Asignatura.objects.filter(periodos__colegio=pp.colegio, combinable=True).exclude(periodos__pk__in=[pk]).distinct()
    if candidatas:
        return render(request, 'carga_horaria/asignatura/asignatura_maybe.html', {'object': pp, 'candidatas': candidatas})
    else:
        return redirect('carga-horaria:asignatura__nuevo', pk)


@login_required
def asignar(request, pk, periodo_pk):
    aa = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        form = AsignacionForm(request.POST, asignatura=aa, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignatura = aa
            asignacion.save()
            return redirect('carga-horaria:periodo', periodo_pk)
    else:
        form = AsignacionForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar.html', {'object': aa,
                                                          'form': form})


@login_required
def asignar_fua(request, pk, tipo):
    pp = get_object_or_404(Profesor, pk=pk)
    tipo_display = dict(Asignacion.TIPO_CHOICES)[int(tipo)]

    if request.method == 'POST':
        form = AsignacionFUAForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            asignacion.tipo = tipo
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionFUAForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_fua.html', {'object': pp,
                                                              'tipo': tipo_display,
                                                              'form': form})

@login_required
def asignar_no_aula_fua(request, pk, tipo):
    pp = get_object_or_404(Profesor, pk=pk)
    tipo_display = dict(AsignacionNoAula.TIPO_CHOICES)[int(tipo)]

    if request.method == 'POST':
        form = AsignacionNoAulaFUAForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            asignacion.tipo = tipo
            if asignacion.horas == 0:
                asignacion.horas = pp.horas_no_aula_disponibles
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionNoAulaFUAForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_no_aula_fua.html', {'profesor': pp,
                                                                      'tipo': tipo_display,
                                                                      'form': form})



@login_required
def asignar_extra(request, pk):
    pp = get_object_or_404(Profesor, pk=pk)

    if request.method == 'POST':
        form = AsignacionExtraForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            if asignacion.horas == 0:
                asignacion.horas = pp.horas_no_lectivas_disponibles
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionExtraForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_extra.html', {'profesor': pp,
                                                                'form': form})


@login_required
def asignar_no_aula(request, pk):
    pp = get_object_or_404(Profesor, pk=pk)

    if request.method == 'POST':
        form = AsignacionNoAulaForm(request.POST, profesor=pp, user=request.user, colegio=request.session.get('colegio__pk', None), periodo=request.session.get('periodo', 2020))
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.profesor = pp
            if asignacion.horas == 0:
                asignacion.horas = pp.horas_no_aula_disponibles
            asignacion.save()
            return redirect('carga-horaria:profesor', pp.pk)
    else:
        form = AsignacionNoAulaForm(user=request.user, colegio=request.session.get('colegio__pk', None))
    return render(request, 'carga_horaria/asignar_no_aula.html', {'profesor': pp,
                                                                  'form': form})

class AsignacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Asignacion
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get_success_url(self):
        return reverse('carga-horaria:profesor', kwargs={'pk': self.kwargs['profesor_pk']})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AsignacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Asignacion
    form_class = AsignacionUpdateForm
    template_name = 'carga_horaria/asignar_update.html'


    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


class AsignacionExtraUpdateView(LoginRequiredMixin, UpdateView):
    model = AsignacionExtra
    form_class = AsignacionExtraUpdateForm
    template_name = 'carga_horaria/asignar_extra.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(AsignacionExtraUpdateView, self).get_context_data(*args, **kwargs)
        ctx['profesor'] = self.object.profesor
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        pp = get_object_or_404(Profesor, pk=self.kwargs.get('profesor_pk'))

        kwargs = super(AsignacionExtraUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'profesor': pp,
                       'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs

    def form_valid(self, form):
        asignacion = form.save(commit=False)
        if asignacion.horas == 0:
            asignacion_old = Asignacion.objects.get(pk=asignacion.pk)
            asignacion.horas = asignacion.profesor.horas_no_lectivas_disponibles + float(asignacion_old.horas)
        asignacion.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


class AsignacionExtraDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionExtra
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )


class AsignacionNoAulaUpdateView(LoginRequiredMixin, UpdateView):
    model = AsignacionNoAula
    form_class = AsignacionNoAulaUpdateForm
    template_name = 'carga_horaria/asignar_no_aula.html'

    def form_valid(self, form):
        asignacion = form.save(commit=False)
        if asignacion.horas == 0:
            asignacion_old = AsignacionNoAula.objects.get(pk=asignacion.pk)
            asignacion.horas = asignacion.profesor.horas_no_aula_disponibles + asignacion_old.horas
        asignacion.save()
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(AsignacionNoAulaUpdateView, self).get_context_data(*args, **kwargs)
        ctx['profesor'] = self.object.profesor
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        pp = get_object_or_404(Profesor, pk=self.kwargs.get('profesor_pk'))

        kwargs = super(AsignacionNoAulaUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'profesor': pp,
                       'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )

class AsignacionNoAulaDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionNoAula
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.profesor.pk,
            }
        )
