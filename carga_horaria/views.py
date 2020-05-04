from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .viewsAlexis import *
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Periodo, Colegio, Plan
from carga_horaria.formsDani import PeriodoForm, ColegioForm, PlanForm
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Profesor
from .models import Periodo
from .models import Asignacion
from .forms import AsignacionForm
from .formsDani import PlantillaPlanForm

def home(request):
    return render(request, 'carga_horaria/home.html')


"""
    Comienzo Crud Periodos
"""
class PeriodoListView(ListView):
    """
        Listado de periodos
    """
    model = Periodo
    template_name = 'carga_horaria/periodo/listado_periodos.html'
    search_fields = ['nombre', 'colegio']
    paginate_by = 6


class PeriodoDetailView(DetailView):
    """
        Detalle de Periodo
    """
    model = Periodo
    template_name = 'carga_horaria/periodo/detalle_periodo.html'


class PeriodoCreateView(CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/nuevo_periodo.html'
    success_url = reverse_lazy('carga-horaria:periodos')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class PeriodoUpdateView(UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'carga_horaria/periodo/editar_periodo.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.pk,
            }
        )


class PeriodoDeleteView(DeleteView):
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
class ColegioListView(ListView):
    """
        Listado de periodos
    """
    model = Colegio
    template_name = 'carga_horaria/colegio/listado_colegios.html'
    search_fields = ['nombre', 'jec']
    paginate_by = 6


class ColegioDetailView(DetailView):
    """
        Detalle de Colegio
    """
    model = Colegio
    template_name = 'carga_horaria/colegio/detalle_colegio.html'


class ColegioCreateView(CreateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'carga_horaria/colegio/nuevo_colegio.html'
    success_url = reverse_lazy('carga-horaria:colegios')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class ColegioUpdateView(UpdateView):
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



class ColegioDeleteView(DeleteView):
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
class PlanListView(ListView):
    """
        Listado de planes
    """
    model = Plan
    template_name = 'carga_horaria/plan/listado_planes.html'
    search_fields = ['nombre', 'nivel']
    paginate_by = 6


class PlanDetailView(DetailView):
    """
        Detalle de Plan
    """
    model = Plan
    template_name = 'carga_horaria/plan/detalle_plan.html'


class PlanCreateView(CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/nuevo_plan.html'
    success_url = reverse_lazy('carga-horaria:planes')
#    success_message = u"Nuevo periodo %(nombre)s creado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


def crear_desde_plantilla(request):
    if request.method == 'POST':
        form = PlantillaPlanForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            plantilla = form.cleaned_data['plan']

            nuevo = Plan.objects.create(nombre=nombre,
                                        nivel=plantilla.nivel)
            for ab in plantilla.asignaturabase_set.all():
                AsignaturaBase.objects.create(nombre=ab.nombre,
                                              plan=nuevo,
                                              horas_jec=ab.horas_jec,
                                              horas_nec=ab.horas_nec)
            return redirect('carga-horaria:planes')
    else:
        form = PlantillaPlanForm()
    return render(request, 'carga_horaria/plantilla.html', {'form': form})


class PlanUpdateView(UpdateView):
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


class PlanDeleteView(DeleteView):
    model = Plan
    success_url = reverse_lazy('carga-horaria:planes')
    template_name = 'carga_horaria/plan/eliminar_plan.html'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""
    Fin Crud Planes
"""

def asignar(request, pk):
    aa = get_object_or_404(Asignatura, pk=pk)

    if request.method == 'POST':
        form = AsignacionForm(request.POST, asignatura=aa)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignatura = aa
            asignacion.save()
            return redirect('carga-horaria:periodo', aa.periodo.pk)
    else:
        form = AsignacionForm()
    return render(request, 'carga_horaria/asignar.html', {'object': aa,
                                                          'form': form})


class AsignacionDeleteView(DeleteView):
    model = Asignacion
    success_url = reverse_lazy('carga-horaria:periodos')
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AsignacionUpdateView(UpdateView):
    model = Asignacion
    form_class = AsignacionForm
    template_name = 'carga_horaria/asignar.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.object.asignatura.periodo.pk,
            }
        )
