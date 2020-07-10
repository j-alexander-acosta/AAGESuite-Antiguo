from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
# from jsonview.decorators import json_view, json
from .models import Funcionario, Entrevista, Archivo, Vacacion, TipoLicencia, Licencia
from .forms import FuncionarioForm, EntrevistaForm, ArchivoForm, VacacionForm
from .forms import TipoLicenciaForm, LicenciaForm, LicenciaFuncionarioForm




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


class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/nuevo_funcionario.html'
    success_url = reverse_lazy('rrhh:funcionarios')


@login_required
def funcionario_detail(request, pk_funcionario):
    context = {}
    funcionario = get_object_or_404(
        Funcionario,
        pk=pk_funcionario
    )

    context['object'] = funcionario
    context['lf_form'] = LicenciaFuncionarioForm(instance=funcionario)

    return render(
        request,
        'rrhh/funcionario/perfil.html',
        context
    )


class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    model = Funcionario
    template_name = 'rrhh/funcionario/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lf_form'] = LicenciaFuncionarioForm(instance=self)
        return context


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
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


class EntrevistaCreateView(LoginRequiredMixin, CreateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'rrhh/entrevista/nueva_entrevista.html'
    success_url = reverse_lazy('rrhh:entrevistas')


class EntrevistaDetailView(LoginRequiredMixin, DetailView):
    model = Entrevista
    template_name = 'rrhh/entrevista/detalle_entrevista.html'


class EntrevistaUpdateView(LoginRequiredMixin, UpdateView):
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


class ArchivoCreateView(LoginRequiredMixin, CreateView):
    model = Archivo
    form_class = ArchivoForm
    template_name = 'rrhh/archivo/nuevo_archivo.html'
    success_url = reverse_lazy('rrhh:archivos')


class ArchivoDetailView(LoginRequiredMixin, DetailView):
    model = Archivo
    template_name = 'rrhh/archivo/detalle_archivo.html'


class ArchivoUpdateView(LoginRequiredMixin, UpdateView):
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


class VacacionListView(LoginRequiredMixin, ListView):
    model = Vacacion
    template_name = 'rrhh/vacacion/listado_vacacion.html'
    search_fields = ['funcionario__rut', 'funcionario']
    paginate_by = 10


class VacacionDetailView(LoginRequiredMixin, DetailView):
    model = Vacacion
    template_name = 'rrhh/vacacion/detalle_vacacion.html'


class VacacionCreateView(LoginRequiredMixin, CreateView):
    model = Vacacion
    form_class = VacacionForm
    template_name = 'rrhh/vacacion/nueva_vacacion.html'
    success_url = reverse_lazy('rrhh:vacaciones')


class VacacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacacion
    form_class = VacacionForm
    template_name = 'rrhh/vacacion/editar_vacacion.html'

    def get_success_url(self):
        return reverse(
            'rrhh:vacacion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class VacacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacacion
    success_url = reverse_lazy('rrhh:vacaciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TipoLicenciaListView(LoginRequiredMixin, ListView):
    model = TipoLicencia
    template_name = 'rrhh/tipo_licencia/listado_tipolicencia.html'
    search_fields = ['nombre']
    paginate_by = 10


class TipoLicenciaDetailView(LoginRequiredMixin, DetailView):
    model = TipoLicencia
    template_name = 'rrhh/tipo_licencia/detalle_tipolicencia.html'


class TipoLicenciaCreateView(LoginRequiredMixin, CreateView):
    model = TipoLicencia
    form_class = TipoLicenciaForm
    template_name = 'rrhh/tipo_licencia/nuevo_tipolicencia.html'
    success_url = reverse_lazy('rrhh:tiposlicencia')


class TipoLicenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoLicencia
    form_class = TipoLicenciaForm
    template_name = 'rrhh/tipo_licencia/editar_tipolicencia.html'

    def get_success_url(self):
        return reverse(
            'rrhh:tipolicencia',
            kwargs={
                'pk': self.object.pk,
            }
        )


class TipoLicenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoLicencia
    success_url = reverse_lazy('rrhh:tiposlicencia')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LicenciaListView(LoginRequiredMixin, ListView):
    model = Licencia
    template_name = 'rrhh/licencia/listado_licencia.html'
    search_fields = ['funcionario', 'funcionario_rut']
    paginate_by = 10


class LicenciaDetailView(LoginRequiredMixin, DetailView):
    model = Licencia
    template_name = 'rrhh/licencia/detalle_licencia.html'


class LicenciaCreateView(LoginRequiredMixin, CreateView):
    model = Licencia
    form_class = LicenciaForm
    template_name = 'rrhh/licencia/nuevo_licencia.html'
    success_url = reverse_lazy('rrhh:licencias')


class LicenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Licencia
    form_class = LicenciaForm
    template_name = 'rrhh/licencia/editar_licencia.html'

    def get_success_url(self):
        return reverse(
            'rrhh:licencia',
            kwargs={
                'pk': self.object.pk,
            }
        )


class LicenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Licencia
    success_url = reverse_lazy('rrhh:licencias')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# @login_required
# @json_view
# def nuevo_licencia_funcionario(request):
#     """
#         Función para crear un nuevo objetivo estrategico para un area en particular
#
#     :param request: Django Request
#     :return: Json
#     """
#     data = {
#         'success': False,
#         'message': u"",
#         'form_html': None
#     }
#
#     if request.is_ajax():
#         if request.method == 'POST':
#             form = LicenciaFuncionarioForm(request.POST)
#             if form.is_valid():
#                 licencia = form.save()
#                 data['success'] = True
#                 data['message'] = u"la licencia fue agregada exitosamente"
#                 data['tipo_licencia'] = licencia.tipo_licencia if licencia.tipo_licencia else licencia.tipo_licencia_descripcion
#                 data['folio'] = licencia.folio_licencia
#                 data['periodo'] = '{} - {}'.format(
#                     licencia.fecha_inicio,
#                     licencia.fecha_termino
#                 )
#                 data['fecha_retorno'] = licencia.fecha_retorno
#                 data['total_dias'] = licencia.total_dias
#                 data['total_feriados'] = licencia.total_feriados
#                 data['dias_habiles'] = licencia.dias_habiles
#             else:
#                 form_html = render_crispy_form(
#                     form,
#                     context=csrf(request)
#                 )
#                 # Formulario con errores
#                 data['message'] = u"Complete la información requerida"
#                 data['form_html'] = form_html
#         else:
#             data['message'] = u"La solicitud debe ser POST"
#     else:
#         data['message'] = u"La solicitud debe ser ajax"
#
#     return data
