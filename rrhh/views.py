from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from jsonview.decorators import json_view, json
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from django.template.defaultfilters import yesno
from django.contrib.humanize.templatetags.humanize import naturalday
from rrhh.templatetags.rrhh_utils import *
from rrhh.models.base import Funcion, TipoLicencia, AFP, Isapre
from rrhh.models.persona import Persona, Funcionario, DocumentoFuncionario
from rrhh.models.union import Union
from rrhh.models.fundacion import Fundacion
from rrhh.models.colegio import Colegio, Entrevista, VacacionFuncionarioColegio, FiniquitoColegio, LicenciaFuncionarioColegio, ContratoColegio, SolicitudContratacion, EstadoSolicitud
from rrhh.forms import UnionForm, FundacionForm, ColegioForm, PersonaForm, FuncionarioForm, EntrevistaForm, DocumentoFuncionarioForm, VacacionFuncionarioColegioForm, FiniquitoColegioForm
from rrhh.forms import TipoLicenciaForm, LicenciaFuncionarioColegioForm, VacacionTipoFuncionarioColegioForm, IsapreForm, SolicitudContratacionForm, EstadoSolicitudForm
from rrhh.forms import LicenciaTipoFuncionarioColegioForm, ContratoColegioForm, FuncionForm, AFPForm, SolicitudRenovacionForm


@login_required
def home(request):
    contratos = ContratoColegio.objects.filter(vigente=True)
    contratos_expirar = []
    for c in contratos:
        if c.categoria == 2 and c.dias_termino_contrato <= 120:
            contratos_expirar.append(c)
        elif c.dias_termino_contrato <= 60:
            contratos_expirar.append(c)
    context = {
        'contratos_expirar': contratos_expirar
    }


    return render(request, 'rrhh/home.html', context)


class UnionListView(LoginRequiredMixin, ListView):
    model = Union
    template_name = 'rrhh/union/listado_union.html'
    paginate_by = 10


class UnionCreateView(LoginRequiredMixin, CreateView):
    model = Union
    form_class = UnionForm
    template_name = 'rrhh/union/nuevo_union.html'

    def get_success_url(self):
        return reverse(
            'rrhh:union',
            kwargs={
                'pk': self.object.pk,
            }
        )


class UnionDetailView(LoginRequiredMixin, DetailView):
    model = Union
    template_name = 'rrhh/union/detalle_union.html'


class UnionUpdateView(LoginRequiredMixin, UpdateView):
    model = Union
    form_class = UnionForm
    template_name = 'rrhh/union/editar_union.html'

    def get_success_url(self):
        return reverse(
            'rrhh:union',
            kwargs={
                'pk': self.object.pk,
            }
        )

class UnionDeleteView(LoginRequiredMixin, DeleteView):
    model = Union
    success_url = reverse_lazy('rrhh:uniones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FundacionListView(LoginRequiredMixin, ListView):
    model = Fundacion
    template_name = 'rrhh/fundacion/listado_fundacion.html'
    paginate_by = 10


class FundacionCreateView(LoginRequiredMixin, CreateView):
    model = Fundacion
    form_class = FundacionForm
    template_name = 'rrhh/fundacion/nuevo_fundacion.html'

    def get_success_url(self):
        return reverse(
            'rrhh:fundacion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class FundacionDetailView(LoginRequiredMixin, DetailView):
    model = Fundacion
    template_name = 'rrhh/fundacion/detalle_fundacion.html'


class FundacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Fundacion
    form_class = FundacionForm
    template_name = 'rrhh/fundacion/editar_fundacion.html'

    def get_success_url(self):
        return reverse(
            'rrhh:fundacion',
            kwargs={
                'pk': self.object.pk,
            }
        )

class FundacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Fundacion
    success_url = reverse_lazy('rrhh:fundaciones')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ColegioListView(LoginRequiredMixin, ListView):
    model = Colegio
    template_name = 'rrhh/colegio/listado_colegio.html'
    paginate_by = 10


class ColegioCreateView(LoginRequiredMixin, CreateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'rrhh/colegio/nuevo_colegio.html'

    def get_success_url(self):
        return reverse(
            'rrhh:colegio',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ColegioDetailView(LoginRequiredMixin, DetailView):
    model = Colegio
    template_name = 'rrhh/colegio/detalle_colegio.html'


class ColegioUpdateView(LoginRequiredMixin, UpdateView):
    model = Colegio
    form_class = ColegioForm
    template_name = 'rrhh/colegio/editar_colegio.html'

    def get_success_url(self):
        return reverse(
            'rrhh:colegio',
            kwargs={
                'pk': self.object.pk,
            }
        )

class ColegioDeleteView(LoginRequiredMixin, DeleteView):
    model = Colegio
    success_url = reverse_lazy('rrhh:colegios')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


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
        if self.request.POST.get('funcionario'):
            return reverse_lazy('rrhh:funcionario__nuevo')
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


# class FuncionarioListView(LoginRequiredMixin, ListView):
#     model = Funcionario
#     template_name = 'rrhh/funcionario/listado_funcionario.html'
#     paginate_by = 10
#
#
class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/nuevo_funcionario.html'

    def get_success_url(self):
        return reverse(
            'rrhh:persona',
            kwargs={
                'pk': self.object.persona.pk,
            }
        )


@login_required
def crear_funcionario(request, id_persona):
    persona = get_object_or_404(
        Persona,
        id=id_persona
    )
    context = {}

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('rrhh:persona', persona.id)
        else:
            # Formulario con errores
            context['message'] = u"Complete la información requerida"
            context['form'] = form

    else:
        form = FuncionarioForm(
            initial={
                'persona': persona
            },
        )
        context['form'] = form

    return render(
        request,
        'rrhh/funcionario/nuevo_funcionario.html',
        context
    )




# class FuncionarioDetailView(LoginRequiredMixin, DetailView):
#     model = Funcionario
#     template_name = 'rrhh/funcionario/detalle_funcionario.html'
#
#
class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'rrhh/funcionario/editar_funcionario.html'

    def get_success_url(self):
        return reverse(
            'rrhh:persona',
            kwargs={
                'pk': self.object.persona.pk,
            }
        )
#
# class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
#     model = Funcionario
#     success_url = reverse_lazy('rrhh:funcionarios')
#
#     def get(self, request, *args, **kwargs):
#        return self.post(request, *args, **kwargs)


@login_required
def postulantes(request):
    context = {}
    postulantes = { p for p in Persona.objects.all() if 'Postulante' in p.clasificacion }

    context['postulantes'] = postulantes

    return render(
        request,
        'rrhh/solicitud_contratacion/postulantes.html',
        context
    )


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


class DocumentoFuncionarioListView(LoginRequiredMixin, ListView):
    """
        Listado de periodos
    """
    model = DocumentoFuncionario
    template_name = 'rrhh/documento_funcionario/listado_documento_funcionario.html'
    paginate_by = 10


class DocumentoFuncionarioCreateView(LoginRequiredMixin, CreateView):
    model = DocumentoFuncionario
    form_class = DocumentoFuncionarioForm
    template_name = 'rrhh/documento_funcionario/nuevo_documento_funcionario.html'
    success_url = reverse_lazy('rrhh:documentos')


class DocumentoFuncionarioDetailView(LoginRequiredMixin, DetailView):
    model = DocumentoFuncionario
    template_name = 'rrhh/documento_funcionario/detalle_documento_funcionario.html'


class DocumentoFuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    model = DocumentoFuncionario
    form_class = DocumentoFuncionarioForm
    template_name = 'rrhh/documento_funcionario/editar_documento_funcionario.html'

    def get_success_url(self):
        return reverse(
            'rrhh:documento',
            kwargs={
                'pk': self.object.pk,
            }
        )

class DocumentoFuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    model = DocumentoFuncionario
    success_url = reverse_lazy('rrhh:documentos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class VacacionListView(LoginRequiredMixin, ListView):
    model = VacacionFuncionarioColegio
    template_name = 'rrhh/vacacion/listado_vacacion.html'
    search_fields = ['contrato__persona__rut', 'contrato__persona']
    paginate_by = 10


class VacacionDetailView(LoginRequiredMixin, DetailView):
    model = VacacionFuncionarioColegio
    template_name = 'rrhh/vacacion/detalle_vacacion.html'


class VacacionCreateView(LoginRequiredMixin, CreateView):
    model = VacacionFuncionarioColegio
    form_class = VacacionFuncionarioColegioForm
    template_name = 'rrhh/vacacion/nueva_vacacion.html'
    success_url = reverse_lazy('rrhh:vacaciones')


class VacacionUpdateView(LoginRequiredMixin, UpdateView):
    model = VacacionFuncionarioColegio
    form_class = VacacionFuncionarioColegioForm
    template_name = 'rrhh/vacacion/editar_vacacion.html'

    def get_success_url(self):
        return reverse(
            'rrhh:vacacion',
            kwargs={
                'pk': self.object.pk,
            }
        )


class VacacionDeleteView(LoginRequiredMixin, DeleteView):
    model = VacacionFuncionarioColegio
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
    model = LicenciaFuncionarioColegio
    template_name = 'rrhh/licencia/listado_licencia.html'
    search_fields = ['contrato__persona', 'contrato__persona_rut']
    paginate_by = 10
    order_by = '-id'


class LicenciaDetailView(LoginRequiredMixin, DetailView):
    model = LicenciaFuncionarioColegio
    template_name = 'rrhh/licencia/detalle_licencia.html'


class LicenciaCreateView(LoginRequiredMixin, CreateView):
    model = LicenciaFuncionarioColegio
    form_class = LicenciaFuncionarioColegioForm
    template_name = 'rrhh/licencia/nuevo_licencia.html'
    success_url = reverse_lazy('rrhh:licencias')


class LicenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = LicenciaFuncionarioColegio
    form_class = LicenciaFuncionarioColegioForm
    template_name = 'rrhh/licencia/editar_licencia.html'

    def get_success_url(self):
        return reverse(
            'rrhh:licencia',
            kwargs={
                'pk': self.object.pk,
            }
        )


class LicenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = LicenciaFuncionarioColegio
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
            form = LicenciaTipoFuncionarioColegioForm(request.POST)
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
            form = VacacionTipoFuncionarioColegioForm(request.POST)
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
    model = ContratoColegio
    template_name = 'rrhh/contrato/listado_contrato.html'
    search_fields = ['persona__rut', 'persona']
    paginate_by = 10
    ordering = '-vigente'


class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = ContratoColegio
    template_name = 'rrhh/contrato/detalle_contrato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lf_form'] = LicenciaTipoFuncionarioColegioForm(initial={'contrato':self})
        context['vf_form'] = VacacionTipoFuncionarioColegioForm(initial={'contrato':self})
        return context


class ContratoCreateView(LoginRequiredMixin, CreateView):
    model = ContratoColegio
    form_class = ContratoColegioForm
    template_name = 'rrhh/contrato/nuevo_contrato.html'
    success_url = reverse_lazy('rrhh:contratos')


class ContratoUpdateView(LoginRequiredMixin, UpdateView):
    model = ContratoColegio
    form_class = ContratoColegioForm
    template_name = 'rrhh/contrato/editar_contrato.html'

    def get_success_url(self):
        return reverse(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ContratoDeleteView(LoginRequiredMixin, DeleteView):
    model = ContratoColegio
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
        ContratoColegio,
        pk=id_contrato
    )
    context = {}

    if request.method == 'POST':
        form = FiniquitoColegioForm(
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
        form = FiniquitoColegioForm(
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
    model = FiniquitoColegio

    def get_success_url(self):
        return reverse(
            'rrhh:contrato',
            kwargs={
                'pk': self.object.contrato.pk,
            }
        )

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SolicitudContratacionListView(LoginRequiredMixin, ListView):
    model = SolicitudContratacion
    template_name = 'rrhh/solicitud_contratacion/listado_solicitudcontratacion.html'
    search_fields = ['nombre']
    paginate_by = 10


class SolicitudContratacionDetailView(LoginRequiredMixin, DetailView):
    model = SolicitudContratacion
    template_name = 'rrhh/solicitud_contratacion/detalle_solicitudcontratacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EstadoSolicitudForm()
        return context


class SolicitudContratacionCreateView(LoginRequiredMixin, CreateView):
    model = SolicitudContratacion
    form_class = SolicitudContratacionForm
    template_name = 'rrhh/solicitud_contratacion/nueva_solicitudcontratacion.html'
    #success_url = reverse_lazy('rrhh:solicitudes')

    def get_success_url(self):
        EstadoSolicitud.objects.create(
            solicitud=self.object,
            estado=2,
            observaciones='Se crea la solicitud de contratación',
            autor=self.request.user
        )
        return reverse(
            'rrhh:solicitud',
            kwargs={
                'pk': self.object.pk,
            }
        )


class SolicitudContratacionUpdateView(LoginRequiredMixin, UpdateView):
    model = SolicitudContratacion
    form_class = SolicitudContratacionForm
    template_name = 'rrhh/solicitud_contratacion/editar_solicitudcontratacion.html'

    def get_success_url(self):
        EstadoSolicitud.objects.create(
            solicitud=self.object,
            estado=2,
            observaciones='Los datos de la solicitud de contratación, fueron actualizados',
            autor=self.request.user
        )
        return reverse(
            'rrhh:solicitud',
            kwargs={
                'pk': self.object.pk,
            }
        )


class SolicitudContratacionDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudContratacion
    success_url = reverse_lazy('rrhh:solicitudes')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def cambiar_estado_solicitud(request):
    if request.method == 'POST':
        form = EstadoSolicitudForm(request.POST)
        if form.is_valid():
            id_solicitud = request.POST.get('solicitud', None)
            solicitud = get_object_or_404(
                SolicitudContratacion,
                id=id_solicitud
            )
            estado = request.POST.get('estado', None)
            voto = request.POST.get('voto', None)
            observaciones = request.POST.get('observaciones', None)

            texto_inicial = 'Se acepta la solicitud de contratación'

            if estado == '2':
                texto_inicial = 'Pendiente de aceptación u observaciones'
            elif estado == '3':
                texto_inicial = 'Se rechaza la solicitud de contratación'
            elif estado == '4':
                texto_inicial = 'En espera de selección de candidatos'
            elif estado == '5':
                texto_inicial = 'Pendiente de aprobación'
            elif estado == '6':
                texto_inicial = 'Se aprueba la solicitud de contratación con {} votos'.format(voto)

            observaciones_completo = '{}{} {}'.format(
                texto_inicial,
                ', con observaciones: <br>' if observaciones != '' else '',
                observaciones
            )

            es = EstadoSolicitud.objects.create(
                solicitud=solicitud,
                estado=estado,
                voto=voto,
                observaciones=observaciones_completo,
                autor=request.user
            )
            if estado == '1':
                EstadoSolicitud.objects.create(
                    solicitud=solicitud,
                    estado=4,
                    observaciones='En espera de selección de candidatos',
                    autor=request.user
                )

            return redirect('rrhh:solicitud', es.solicitud.pk)

        else:
            pass


@login_required
def seleccionar_candidatos(request, id_solicitud):
    context = {}
    postulantes = { p for p in Persona.objects.all() if 'Postulante' in p.clasificacion }

    context['postulantes'] = postulantes
    context['id_solicitud'] = id_solicitud

    return render(
        request,
        'rrhh/solicitud_contratacion/seleccionar_candidatos.html',
        context
    )


@login_required
@json_view
def guardar_candidato(request):
    persona = get_object_or_404(
        Persona,
        id=request.GET.get('id_persona')
    )
    solicitud = get_object_or_404(
        SolicitudContratacion,
        id=request.GET.get('id_solicitud')
    )
    index = request.GET.get('index')

    solicitud.postulantes.add(persona)

    if index == '0' :
        EstadoSolicitud.objects.create(
            solicitud=solicitud,
            estado=5,
            observaciones='Pendiente de aprobación <br>Candidatos seleccionados',
            autor=request.user
        )

    return {'mensaje': 'Todo bien'}


@login_required
def renovar_contrato(request, id_contrato):
    contrato = get_object_or_404(
        ContratoColegio,
        id=id_contrato
    )
    context = {}
    estado = request.GET.get('estado', None)
    observaciones = request.GET.get('observaciones', None)
    voto = request.GET.get('voto', None)


    if estado:
        if estado == 4:
            contrato.solicitudrenovacion.estado = estado
            contrato.solicitudrenovacion.save()
            return HttpResponse('rrhh:renovacion_contrato__contratar', contrato.id)

        contrato.solicitudrenovacion.estado = estado
        if voto:
            contrato.solicitudrenovacion.voto = voto
        if observaciones:
            contrato.solicitudrenovacion.observaciones += '<br>' + observaciones
        contrato.solicitudrenovacion.autor = request.user
        contrato.solicitudrenovacion.save()

        return redirect('rrhh:contrato', contrato.pk)

    else:
        if request.method == 'POST':
            form = SolicitudRenovacionForm(request.POST)
            if form.is_valid():
                sr = form.save()

                return redirect('rrhh:contrato', sr.contrato.pk)

        else:
            form = SolicitudRenovacionForm(
                initial={
                    'contrato': contrato,
                    'tipo_contrato':contrato.tipo_contrato,
                    'horas': contrato.horas_total,
                    'fecha_inicio': contrato.fecha_termino,
                    'estado': 1
                }
            )
            context['form'] = form

        return render(
            request,
            'rrhh/solicitud_contratacion/nueva_solicitudrenovacioncontratacion.html',
            context
        )


@login_required
def crear_contrato_colegio(request, id_funcionario, id_solicitud):
    funcionario = get_object_or_404(
        Funcionario,
        id=id_funcionario
    )
    solicitud = get_object_or_404(
        SolicitudContratacion,
        id=id_solicitud
    )

    context = crear_contrato_colegio_funcion(
        request,
        funcionario,
        solicitud.colegio,
        solicitud.categoria,
        solicitud.tipo_contrato,
        solicitud.horas,
        solicitud.fecha_inicio,
        solicitud.fecha_termino,
        solicitud.reemplazando_licencia,
    )
    if context['redirect']:
        return redirect('rrhh:contrato', context['redirect'].id)

    return render(
        request,
        'rrhh/contrato/nuevo_contrato.html',
        context
    )


@login_required
def renovar_contrato_colegio(request, id_contrato):
    contrato = get_object_or_404(
        ContratoColegio,
        id=id_contrato
    )

    contrato.vigente=False
    contrato.save()

    context = crear_contrato_colegio_funcion(
        request,
        contrato.funcionario,
        contrato.colegio,
        contrato.categoria,
        contrato.tipo_contrato,
        contrato.horas_total,
        contrato.fecha_termino,
        None,
        contrato.reemplazando_licencia,
    )
    nuevo_contrato = context['redirect']
    if nuevo_contrato:
        FiniquitoColegio.objects.create(
            contrato=contrato,
            descripcion='Se realizó la renovacion del contrato, a un contrato {} de {} horas'.format(nuevo_contrato.get_tipo_contrato_display(), nuevo_contrato.horas_total)
        )

        return redirect('rrhh:contrato', nuevo_contrato.id)
    else:
        contrato.vigente=True
        contrato.save()

    return render(
        request,
        'rrhh/contrato/nuevo_contrato.html',
        context
    )


login_required
def trasladar_funcionario(request, id_contrato):
    contrato = get_object_or_404(
        ContratoColegio,
        id=id_contrato
    )

    contrato.vigente=False
    contrato.save()

    context = crear_contrato_colegio_funcion(
        request,
        contrato.funcionario,
        None,
        contrato.categoria,
        contrato.tipo_contrato,
        contrato.horas_total,
        contrato.fecha_inicio,
        contrato.fecha_termino,
        None,
    )
    nuevo_contrato = context['redirect']
    if nuevo_contrato:
        FiniquitoColegio.objects.create(
            contrato=contrato,
            descripcion='Se realizó el traslado del funcionario, al {}'.format(nuevo_contrato.colegio)
        )

        return redirect('rrhh:contrato', nuevo_contrato.id)
    else:
        contrato.vigente=True
        contrato.save()

    return render(
        request,
        'rrhh/contrato/nuevo_contrato.html',
        context
    )


def crear_contrato_colegio_funcion(
    request,
    funcionario,
    colegio,
    categoria,
    tipo_contrato,
    horas_total,
    fecha_inicio,
    fecha_termino,
    reemplazando_licencia,
):

    context = {}
    context['redirect'] = False

    if request.method == 'POST':
        form = ContratoColegioForm(request.POST)
        if form.is_valid():
            c = form.save()

            context['redirect'] = c
        else:
            # Formulario con errores
            context['message'] = u"Complete la información requerida"
            context['form'] = form

    else:
        form = ContratoColegioForm(
            initial={
                'funcionario': funcionario,
                'colegio': colegio,
                'categoria': categoria,
                'tipo_contrato': tipo_contrato,
                'horas_total': horas_total,
                'fecha_inicio': fecha_inicio,
                'fecha_termino': fecha_termino,
                'reemplazando_licencia': reemplazando_licencia
            },
        )
        context['form'] = form

    return context
