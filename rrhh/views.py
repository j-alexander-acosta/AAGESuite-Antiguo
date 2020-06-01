from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render
from .models import Funcionario
from .models import Entrevista
from .models import Archivo
from .forms import FuncionarioForm
from .forms import EntrevistaForm
from .forms import ArchivoForm


@login_required
def home(request):
    return render(request, 'rrhh/home.html')


class FuncionarioListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = Funcionario
    template_name = 'rrhh/funcionario/listado_funcionario.html'
    paginate_by = 10


class FuncionarioCreateView(CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/nuevo_funcionario.html'
    success_url = reverse_lazy('rrhh:funcionarios')


class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = 'rrhh/funcionario/detalle_funcionario.html'


class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/editar_funcionario.html'

    def get_success_url(self):
        return reverse(
            'rrhh:funcionario',
            kwargs={
                'pk': self.object.pk,
            }
        )

class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Funcionario
    success_url = reverse_lazy('rrhh:funcionarios')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EntrevistaListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = Entrevista
    template_name = 'rrhh/entrevista/listado_entrevista.html'
    paginate_by = 10


class EntrevistaCreateView(CreateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'rrhh/entrevista/nueva_entrevista.html'
    success_url = reverse_lazy('rrhh:entrevistas')


class EntrevistaDetailView(DetailView):
    model = Entrevista
    template_name = 'rrhh/entrevista/detalle_entrevista.html'


class EntrevistaUpdateView(UpdateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'rrhh/entrevista/editar_entrevista.html'

    def get_success_url(self):
        return reverse(
            'rrhh:entrevista',
            kwargs={
                'pk': self.object.pk,
            }
        )

class EntrevistaDeleteView(LoginRequiredMixin, DeleteView):
    model = Entrevista
    success_url = reverse_lazy('rrhh:entrevistas')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ArchivoListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = Archivo
    template_name = 'rrhh/archivo/listado_archivo.html'
    paginate_by = 10


class ArchivoCreateView(CreateView):
    model = Archivo
    form_class = ArchivoForm
    template_name = 'rrhh/archivo/nuevo_archivo.html'
    success_url = reverse_lazy('rrhh:archivos')


class ArchivoDetailView(DetailView):
    model = Archivo
    template_name = 'rrhh/archivo/detalle_archivo.html'


class ArchivoUpdateView(UpdateView):
    model = Archivo
    form_class = ArchivoForm
    template_name = 'rrhh/archivo/editar_archivo.html'

    def get_success_url(self):
        return reverse(
            'rrhh:archivo',
            kwargs={
                'pk': self.object.pk,
            }
        )

class ArchivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Archivo
    success_url = reverse_lazy('rrhh:archivos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
