from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from jsonview.decorators import json_view, json
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from django.template.defaultfilters import yesno
from django.contrib.humanize.templatetags.humanize import naturalday
from rrhh.templatetags.rrhh_utils import *
from .models import Persona, Entrevista, Archivo, Vacacion, Finiquito
from .models import TipoLicencia, Licencia, Contrato, Funcion, AFP, Isapre
from .forms import PersonaForm, EntrevistaForm, ArchivoForm, VacacionForm, FiniquitoForm
from .forms import TipoLicenciaForm, LicenciaForm, VacacionFuncionarioForm, IsapreForm
from .forms import LicenciaTipoFuncionarioForm, ContratoForm, FuncionForm, AFPForm


@login_required
def home(request):
    return render(request, 'rrhh/home.html')


class PersonaListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = Persona
    template_name = 'rrhh/persona/listado_persona.html'
    paginate_by = 10


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'rrhh/persona/nuevo_persona.html'

    def get_success_url(self):
        if self.request.POST.get('contrato'):
            return reverse_lazy('rrhh:contrato__nuevo')
        else:
            return reverse_lazy('rrhh:personas')


@login_required
def persona_detail(request, pk_persona):
    context = {}
    persona = get_object_or_404(
        Persona,
        pk=pk_persona
    )

    context['object'] = persona


    return render(
        request,
        'rrhh/persona/perfil.html',
        context
    )


class PersonaDetailView(LoginRequiredMixin, DetailView):
    model = Persona
    template_name = 'rrhh/persona/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lf_form'] = LicenciaTipoFuncionarioForm(instance=self)
        return context


class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'rrhh/persona/editar_persona.html'

    def get_success_url(self):
        return reverse(
            'rrhh:persona',
            kwargs={
                'pk_persona': self.object.pk,
            }
        )

class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    success_url = reverse_lazy('rrhh:personas')

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
    search_fields = ['contrato__persona__rut', 'contrato__persona']
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
    search_fields = ['contrato__persona', 'contrato__persona_rut']
    paginate_by = 10
    order_by = '-id'


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


@login_required
@json_view
def nuevo_licencia_tipo_funcionario(request):
    """
        Función para crear un nuevo registro de licencia a un uncionario

    :param request: Django Request
    :return: Json
    """
    data = {
        'success': False,
        'message': u"",
        'form_html': None
    }

    if request.is_ajax():
        if request.method == 'POST':
            form = LicenciaTipoFuncionarioForm(request.POST)
            print(form.is_valid())
            print(form)
            if form.is_valid():
                licencia = form.save()
                data['success'] = True
                data['message'] = u"la licencia fue agregada exitosamente"
                data['tipo_licencia'] = licencia.tipo_licencia.nombre if licencia.tipo_licencia else licencia.tipo_licencia_descripcion
                data['folio'] = beauty_none(licencia.folio_licencia)
                data['periodo'] = '{} - {}'.format(
                    naturalday(licencia.fecha_inicio),
                    naturalday(licencia.fecha_termino)
                )
                data['total_dias'] = licencia.total_dias
                data['fecha_retorno'] = naturalday(licencia.fecha_retorno)
                data['total_feriados'] = licencia.total_feriados
                data['dias_habiles'] = yesno(licencia.dias_habiles)
            else:
                form_html = render_crispy_form(
                    form,
                    context=csrf(request)
                )
                # Formulario con errores
                data['message'] = u"Complete la información requerida"
                data['form_html'] = form_html
        else:
            data['message'] = u"La solicitud debe ser POST"
    else:
        data['message'] = u"La solicitud debe ser ajax"

    return data


@login_required
@json_view
def nuevo_vacacion_funcionario(request):
    """
        Función para crear un nuevo registro de vacacion a un funcionario

    :param request: Django Request
    :return: Json
    """
    data = {
        'success': False,
        'message': u"",
        'form_html': None
    }

    if request.is_ajax():
        if request.method == 'POST':
            form = VacacionFuncionarioForm(request.POST)
            print(form.is_valid())
            print(form)
            if form.is_valid():
                vacacion = form.save()
                data['success'] = True
                data['message'] = u"la licencia fue agregada exitosamente"

                data['periodo'] = '{} - {}'.format(
                    naturalday(vacacion.fecha_inicio),
                    naturalday(vacacion.fecha_termino)
                )
                data['total_dias'] = vacacion.total_dias
                data['dias_pendiente'] = vacacion.dias_pendiente
                data['fecha_retorno'] = naturalday(vacacion.fecha_retorno)
                data['total_feriados'] = vacacion.total_feriados
                data['es_pendiente'] = yesno(vacacion.es_pendiente)
            else:
                form_html = render_crispy_form(
                    form,
                    context=csrf(request)
                )
                # Formulario con errores
                data['message'] = u"Complete la información requerida"
                data['form_html'] = form_html
        else:
            data['message'] = u"La solicitud debe ser POST"
    else:
        data['message'] = u"La solicitud debe ser ajax"

    return data


class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'rrhh/contrato/listado_contrato.html'
    search_fields = ['persona__rut', 'persona']
    paginate_by = 10


class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = Contrato
    template_name = 'rrhh/contrato/detalle_contrato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lf_form'] = LicenciaTipoFuncionarioForm(initial={'contrato':self})
        context['vf_form'] = VacacionFuncionarioForm(initial={'contrato':self})
        return context


class ContratoCreateView(LoginRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'rrhh/contrato/nuevo_contrato.html'
    success_url = reverse_lazy('rrhh:contratos')


class ContratoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'rrhh/contrato/editar_contrato.html'

    def get_success_url(self):
        return reverse(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ContratoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contrato
    success_url = reverse_lazy('rrhh:contratos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FuncionListView(LoginRequiredMixin, ListView):
    model = Funcion
    template_name = 'rrhh/funcion/listado_funcion.html'
    search_fields = ['nombre']
    paginate_by = 10


class FuncionDetailView(LoginRequiredMixin, DetailView):
    model = Funcion
    template_name = 'rrhh/funcion/detalle_funcion.html'


class FuncionCreateView(LoginRequiredMixin, CreateView):
    model = Funcion
    form_class = FuncionForm
    template_name = 'rrhh/funcion/nueva_funcion.html'
    success_url = reverse_lazy('rrhh:funciones')


class FuncionUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcion
    form_class = FuncionForm
    template_name = 'rrhh/funcion/editar_funcion.html'

    def get_success_url(self):
        return reverse(
            'rrhh:funcion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class FuncionDeleteView(LoginRequiredMixin, DeleteView):
    model = Funcion
    success_url = reverse_lazy('rrhh:funciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AFPListView(LoginRequiredMixin, ListView):
    model = AFP
    template_name = 'rrhh/afp/listado_afp.html'
    search_fields = ['nombre']
    paginate_by = 10


class AFPDetailView(LoginRequiredMixin, DetailView):
    model = AFP
    template_name = 'rrhh/afp/detalle_afp.html'


class AFPCreateView(LoginRequiredMixin, CreateView):
    model = AFP
    form_class = AFPForm
    template_name = 'rrhh/afp/nueva_afp.html'
    success_url = reverse_lazy('rrhh:afps')


class AFPUpdateView(LoginRequiredMixin, UpdateView):
    model = AFP
    form_class = AFPForm
    template_name = 'rrhh/afp/editar_afp.html'

    def get_success_url(self):
        return reverse(
            'rrhh:afp',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AFPDeleteView(LoginRequiredMixin, DeleteView):
    model = AFP
    success_url = reverse_lazy('rrhh:afps')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class IsapreListView(LoginRequiredMixin, ListView):
    model = Isapre
    template_name = 'rrhh/isapre/listado_isapre.html'
    search_fields = ['nombre']
    paginate_by = 10


class IsapreDetailView(LoginRequiredMixin, DetailView):
    model = Isapre
    template_name = 'rrhh/isapre/detalle_isapre.html'


class IsapreCreateView(LoginRequiredMixin, CreateView):
    model = Isapre
    form_class = IsapreForm
    template_name = 'rrhh/isapre/nueva_isapre.html'
    success_url = reverse_lazy('rrhh:isapres')


class IsapreUpdateView(LoginRequiredMixin, UpdateView):
    model = Isapre
    form_class = IsapreForm
    template_name = 'rrhh/isapre/editar_isapre.html'

    def get_success_url(self):
        return reverse(
            'rrhh:isapre',
            kwargs={
                'pk': self.object.pk,
            }
        )


class IsapreDeleteView(LoginRequiredMixin, DeleteView):
    model = Isapre
    success_url = reverse_lazy('rrhh:isapres')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def nuevo_finiquito(request, id_contrato):
    contrato = get_object_or_404(
        Contrato,
        pk=id_contrato
    )
    context = {}

    if request.method == 'POST':
        form = FiniquitoForm(
            request.POST,
            request.FILES,
            id_contrato=contrato.id
        )
        if form.is_valid():
            finiquito = form.save()
            contrato.vigente = False
            contrato.save()

            return redirect('rrhh:contrato', finiquito.contrato.pk)

        else:
            # Formulario con errores
            context['message'] = u"Complete la información requerida"
            context['form'] = form

    else:
        form = FiniquitoForm(
            initial={
                'contrato': contrato
            },
            id_contrato = id_contrato
        )
        context['form'] = form
        context['funcionario'] = '{} {} {} - {}'.format(
            contrato.persona.nombres,
            contrato.persona.apellido_paterno,
            contrato.persona.apellido_materno,
            contrato.funcion_principal
        )

    return render(
        request,
        'rrhh/finiquito/nuevo_finiquito.html',
        context
    )



class FiniquitoDeleteView(LoginRequiredMixin, DeleteView):
    model = Finiquito

    def get_success_url(self):
        return reverse(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.contrato.pk,
            }
        )

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
