from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Periodo
from carga_horaria.forms import PeriodoForm
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