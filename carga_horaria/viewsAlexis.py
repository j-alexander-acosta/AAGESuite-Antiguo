from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Profesor, Curso, Asignatura
from carga_horaria.formsAlexis import ProfesorForm
from django.core.urlresolvers import reverse_lazy, reverse

"""
    Comienzo Crud Profesor
"""
class ProfesorListView(ListView):
    """
        Listado de profesores
    """
    model = Profesor
    template_name = 'carga_horaria/profesor/listado_profesor.html'
    search_fields = ['nombre', 'horas']
    paginate_by = 6


class ProfesorDetailView(DetailView):
    """
        Detalle de Profesor
    """
    model = Profesor
    template_name = 'carga_horaria/profesor/detalle_profesor.html'


class ProfesorCreateView(CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'carga_horaria/profesor/nuevo_profesor.html'
    success_url = reverse_lazy('carga-horaria:profesores')


class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'carga_horaria/profesor/editar_profesor.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ProfesorDeleteView(DeleteView):
    model = Profesor
    success_url = reverse_lazy('carga-horaria:profesores')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
