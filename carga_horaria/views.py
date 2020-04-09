from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Periodo
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


"""
    Fin Crud Periodos
"""