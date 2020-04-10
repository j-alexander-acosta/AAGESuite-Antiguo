from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Periodo, Colegio, Plan
from carga_horaria.forms import PeriodoForm, ColegioForm, PlanForm
from django.core.urlresolvers import reverse_lazy


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
    paginate_by = 3


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
#    success_message = u"Periodo %(anio)s actualizado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class PeriodoDeleteView(DeleteView):
    model = Periodo
    success_url = reverse_lazy('carga-horaria:periodos')
    template_name = 'carga_horaria/periodo/eliminar_periodo.html'

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
    paginate_by = 3


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
#    success_message = u"Periodo %(anio)s actualizado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class ColegioDeleteView(DeleteView):
    model = Colegio
    success_url = reverse_lazy('carga-horaria:colegios')
    template_name = 'carga_horaria/colegio/eliminar_colegio.html'

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
    paginate_by = 3


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


class PlanUpdateView(UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = 'carga_horaria/plan/editar_plan.html'
#    success_message = u"Periodo %(anio)s actualizado satisfactoriamente."
#    error_message = "Revise que todos los campos del formulario hayan sido validados correctamente."


class PlanDeleteView(DeleteView):
    model = Plan
    success_url = reverse_lazy('carga-horaria:planes')
    template_name = 'carga_horaria/plan/eliminar_plan.html'

"""
    Fin Crud Planes
"""