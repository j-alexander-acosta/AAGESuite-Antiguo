from django import forms
from django.db.models import Sum, Count
from localflavor.cl.forms import CLRutField
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from rrhh.models.base import TipoLicencia, Funcion, AFP, Isapre
from rrhh.models.persona import Persona, Funcionario, DocumentoFuncionario
from rrhh.models.union import Union
from rrhh.models.fundacion import Fundacion
from rrhh.models.colegio import Colegio, Entrevista, VacacionFuncionarioColegio, EstadoContratacion, DocumentoPersonal
from rrhh.models.colegio import ContratoColegio, LicenciaFuncionarioColegio, PermisoFuncionarioColegio, FiniquitoColegio, Solicitud, EstadoSolicitud


class UnionForm(forms.ModelForm):
    class Meta:
        model = Union
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UnionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class FundacionForm(forms.ModelForm):
    class Meta:
        model = Fundacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FundacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ColegioForm(forms.ModelForm):
    class Meta:
        model = Colegio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ColegioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'

        help_texts = {
            'titulado': u"Marque si la persona tiene un título profesional"
        }
    rut  = CLRutField()

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_nacimiento'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('rut'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('fecha_nacimiento'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('nombres'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('apellido_paterno'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('apellido_materno'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('genero'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('nacionalidad'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('estado_civil'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            'religion',
            Div(
                Div(
                    Field('direccion'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('comuna'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('ciudad'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('telefono'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('email'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('titulado'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('profesion'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
        )


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['persona'].widget.attrs['readonly'] = True
        self.fields['fecha_ingreso_sea'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_ingreso_sea'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_ingreso_docente'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_ingreso_docente'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'persona',
            Div(
                Div(
                    Field('afp'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('salud'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('isapre'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('fecha_ingreso_docente'),
                    css_class="col-md-6"
                ),
                Div(
                    Field('fecha_ingreso_sea'),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('estado'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('tipo_misionero'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('puntos'),
                    css_class="col-md-4"
                ),
                css_class="row"
            ),
        )


class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = ('contrato',
                  'entrevistador',
                  'tipo',
                  'contenido',
                  'acuerdos')

    def __init__(self, *args, **kwargs):
        super(EntrevistaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class DocumentoFuncionarioForm(forms.ModelForm):
    class Meta:
        model = DocumentoFuncionario
        fields = (
            'funcionario',
            'tipo_documento',
            'descripcion',
            'documento'
        )

    def __init__(self, *args, **kwargs):
        super(DocumentoFuncionarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class VacacionFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = VacacionFuncionarioColegio
        fields = [
            'contrato',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'total_feriados',
            'fecha_retorno',
            'dias_pendiente',
            'es_pendiente'
        ]
        help_texts = {
            'total_feriados': u"Considerar dias que no se trabaja como dias feriados (ej. fin de semana)"
        }

    def __init__(self, *args, **kwargs):
        super(VacacionFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class VacacionTipoFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = VacacionFuncionarioColegio
        fields = [
            'contrato',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'fecha_retorno',
            'total_feriados',
            'dias_pendiente',
            'es_pendiente',
        ]
        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(VacacionTipoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'contrato',
            Div(
                Div(
                    Div(
                        Field('total_dias'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('es_pendiente'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('dias_pendiente'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('total_feriados'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('fecha_retorno'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            )
        )


class TipoLicenciaForm(forms.ModelForm):
    class Meta:
        model = TipoLicencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoLicenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class LicenciaFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = LicenciaFuncionarioColegio
        fields = [
            'contrato',
            'tipo_licencia',
            'tipo_licencia_descripcion',
            'folio_licencia',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'total_feriados',
            'fecha_retorno',
            'dias_habiles',
        ]

    def __init__(self, *args, **kwargs):
        super(LicenciaFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class LicenciaTipoFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = LicenciaFuncionarioColegio
        fields = [
            'contrato',
            'tipo_licencia',
            'tipo_licencia_descripcion',
            'folio_licencia',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'fecha_retorno',
            'total_feriados',
            'dias_habiles',
        ]
        help_texts = {
            'dias_habiles': u'Información necesaria para el cálculo de fechas'
        }
        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(LicenciaTipoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'contrato',
            'tipo_licencia',
            'tipo_licencia_descripcion',
            Div(
                Div(
                    Div(
                        Field('folio_licencia'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('total_dias'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('dias_habiles'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('total_feriados'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('fecha_retorno'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            )
        )


class PermisoFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = PermisoFuncionarioColegio
        fields = '__all__'
        help_texts = {
            'goce_sueldo': u'Marque si corresponde',
            'documento': u'Cargue el permiso firmado por ambas partes'
        }

    def __init__(self, *args, **kwargs):
        super(PermisoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_solicitud'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_solicitud'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class PermisoTipoFuncionarioColegioForm(forms.ModelForm):
    class Meta:
        model = PermisoFuncionarioColegio
        fields = '__all__'
        help_texts = {
            'dias_habiles': u'Información necesaria para el cálculo de fechas',
            'goce_sueldo': u'Marque si corresponde',
            'documento': u'Cargue el permiso firmado por ambas partes'
        }
        widgets = {
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(PermisoTipoFuncionarioColegioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_solicitud'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_solicitud'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'contrato',
            'observaciones',
            Div(
                Div(
                    Div(
                        Field('fecha_solicitud'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('total_dias'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('dias_habiles'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('total_feriados'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('fecha_retorno'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('voto'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('goce_sueldo'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            ),
            'documento'
        )


class ContratoColegioForm(forms.ModelForm):
    class Meta:
        model = ContratoColegio
        fields = [
            'funcionario',
            'colegio',
            'categoria',
            'funcion_principal',
            'funcion_secundaria',
            'tipo_contrato',
            'fecha_inicio',
            'fecha_termino',
            'reemplazando_licencia',
            'horas_total'
        ]

    def __init__(self, *args, **kwargs):
        super(ContratoColegioForm, self).__init__(*args, **kwargs)
        self.fields['funcionario'].widget.attrs['class'] = 'chosen'
        self.fields['colegio'].widget.attrs['class'] = 'chosen'
        self.fields['categoria'].widget.attrs['class'] = 'chosen'
        self.fields['funcion_principal'].widget.attrs['class'] = 'chosen'
        self.fields['funcion_secundaria'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_contrato'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            "<div class='checkbox pull-right'>" +
                            "<a href='/rrhh/personas/nuevo'><i class='uil-plus'></i> Agregar Persona</a>" +
                            "</div>"
                        ),
                        Field('funcionario'),
                        css_class='col-md-6',
                    ),
                    Div(
                        HTML(
                            "<div class='text-white'>" +
                            "<a><i class='text-white'></i>Colegio</a>" +
                            "</div>"
                        ),
                        Field('colegio'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('categoria'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('funcion_principal'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('funcion_secundaria'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('tipo_contrato'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('horas_total'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('reemplazando_licencia'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
            )
        )

    def clean(self):
        cleaned_data = super(ContratoColegioForm, self).clean()
        horas_total = self.cleaned_data.get('horas_total', 0)
        tipo_contrato = self.cleaned_data.get('tipo_contrato', 0)
        categoria = self.cleaned_data.get('categoria', 0)
        colegio = self.cleaned_data.get('colegio', None)
        funcionario = self.cleaned_data.get('funcionario', None)
        colegios = Colegio.objects.filter(fundacion=colegio.fundacion)
        contratos_funcionario = ContratoColegio.objects.filter(
            funcionario=funcionario,
            colegio__in=colegios,
            vigente=True,
            reemplazando_permiso=None,
            reemplazando_licencia=None
        )
        cfh = contratos_funcionario.values('funcionario').annotate(
            horas=Sum('horas_total')
        )

        if contratos_funcionario.exists():
            horas_total += cfh[0]['horas']

        horas_esperadas = 45
        if categoria == 2:
            horas_esperadas = 44

        if horas_total > horas_esperadas:
            msg = "Las horas contratadas para este Funcionario, supera el límite de {} horas, por {} horas".format(horas_esperadas, horas_total - horas_esperadas)
            self.add_error('horas_total', msg)

        if tipo_contrato == 2:
            cfc = contratos_funcionario.values_list('tipo_contrato')
            if cfc.count() >= 3:
                cfc = list(cfc)[-3:]
            cpf = 0
            for tp in cfc:
                if tp[0] == 2:
                    cpf += 1
            if cpf >= 3:
                msg = "Ya existen 3 contratos a plazo fijo"
                self.add_error('tipo_contrato', msg)

        return cleaned_data


class FuncionForm(forms.ModelForm):
    class Meta:
        model = Funcion
        fields = [
            'nombre',
            'descripcion',
            'tipo',
        ]

    def __init__(self, *args, **kwargs):
        super(FuncionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AFPForm(forms.ModelForm):
    class Meta:
        model = AFP
        fields = [
            'nombre',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs):
        super(AFPForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class IsapreForm(forms.ModelForm):
    class Meta:
        model = Isapre
        fields = [
            'nombre',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs):
        super(IsapreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class FiniquitoColegioForm(forms.ModelForm):
    class Meta:
        model = FiniquitoColegio
        fields = [
            'contrato',
            'razon_baja',
            'descripcion',
            'archivo'
        ]

        # widgets = {
        #     'contrato': forms.HiddenInput
        # }

    def __init__(self, *args, **kwargs):
        id_contrato = kwargs.pop('id_contrato', None)
        super(FiniquitoColegioForm, self).__init__(*args, **kwargs)
        self.fields['razon_baja'].widget.attrs['class'] = 'chosen'
        self.helper = FormHelper()
        self.helper.form_tag = False


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'tipo',
            'contrato',
            'colegio',
            'categoria',
            'cargo',
            'horas',
            'tipo_contrato',
            'reemplazando_licencia',
            'fecha_inicio',
            'fecha_termino',
            'justificacion'
        ]

        widgets = {
            'tipo': forms.HiddenInput,
            'contrato': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['colegio'].widget.attrs['class'] = 'chosen'
        self.fields['categoria'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_contrato'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['contrato'].queryset = ContratoColegio.objects.filter(vigente=True)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'tipo',
            'contrato',
            'colegio',
            Div(
                Div(
                    Div(
                        Field('categoria'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('cargo'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('horas'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('tipo_contrato'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_inicio'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('fecha_termino'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                )
            ),
            'reemplazando_licencia',
            'justificacion'
        )


class EstadoSolicitudForm(forms.ModelForm):
    class Meta:
        model = EstadoSolicitud
        fields = [
            'estado',
            'observaciones',
            'voto',
        ]

        widgets = {
            'estado': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(EstadoSolicitudForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'estado',
            'observaciones',
            'voto'
        )


class EstadoContratacionForm(forms.Form):
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea({'rows': 6})
    )
    documento = forms.FileField(
        required=False
    )
    estado = forms.IntegerField(
        required = True,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(EstadoContratacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'estado',
            'observaciones',
            'documento'
        )


class DocumentoPersonalForm(forms.ModelForm):
    class Meta:
        model = DocumentoPersonal
        fields = [
            'contrato',
            'documento'
        ]
        widgets = {
            'contrato': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(DocumentoPersonalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
