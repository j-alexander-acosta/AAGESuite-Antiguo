from django import forms
from localflavor.cl.forms import CLRutField
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from .models import Persona, Entrevista, Archivo, Vacacion, Contrato
from .models import TipoLicencia, Licencia, Funcion, AFP, Isapre, Finiquito


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'

    rut  = CLRutField()

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_misionero'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_titulacion'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_ingreso_sea'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_ingreso_docente'].widget.attrs['class'] = 'datepicker'
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
                    Field('telefono'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('email'),
                    css_class="col-md-4"
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
                    Field('titulo'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('casa_formadora'),
                    css_class="col-md-4"
                ),
                Div(
                    Field('fecha_titulacion'),
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


class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('descripcion',
                  'archivo',
                  'contrato')

    def __init__(self, *args, **kwargs):
        super(ArchivoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class VacacionForm(forms.ModelForm):
    class Meta:
        model = Vacacion
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
        super(VacacionForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class TipoLicenciaForm(forms.ModelForm):
    class Meta:
        model = TipoLicencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoLicenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
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
        super(LicenciaForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False


class LicenciaTipoFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Licencia
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
        super(LicenciaTipoFuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
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


class VacacionFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Vacacion
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
        super(VacacionFuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
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


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'persona',
            'colegio',
            'categoria',
            'funcion_principal',
            'funcion_secundaria',
            'tipo_contrato',
            'fecha_inicio',
            'fecha_termino',
            'horas',
            'tipo_horas',
            'reemplazando',
            'salud',
            'isapre',
            'afp',
            'jornada_trabajo',
            'hora_inicio_jornada',
            'hora_termino_jornada',
        ]

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.fields['persona'].widget.attrs['class'] = 'chosen'
        self.fields['colegio'].widget.attrs['class'] = 'chosen'
        self.fields['categoria'].widget.attrs['class'] = 'chosen'
        self.fields['funcion_principal'].widget.attrs['class'] = 'chosen'
        self.fields['funcion_secundaria'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_contrato'].widget.attrs['class'] = 'chosen'
        self.fields['tipo_horas'].widget.attrs['class'] = 'chosen'
        self.fields['reemplazando'].widget.attrs['class'] = 'chosen'
        self.fields['salud'].widget.attrs['class'] = 'chosen'
        self.fields['isapre'].widget.attrs['class'] = 'chosen'
        self.fields['afp'].widget.attrs['class'] = 'chosen'
        self.fields['jornada_trabajo'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['hora_inicio_jornada'].widget.attrs['class'] = 'timepicker'
        self.fields['hora_termino_jornada'].widget.attrs['class'] = 'timepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        HTML(
                            "<div class='checkbox pull-right'>" +
                            "<a href='/rrhh/personas/nuevo'><i class='fa fa-plus'></i> Agregar Persona</a>" +
                            "</div>"
                        ),
                        Field('persona'),
                        css_class='col-md-6',
                    ),
                    Div(
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
                        Field('horas'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('tipo_horas'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('reemplazando'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),

                Div(
                    Div(
                        Field('jornada_trabajo'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('hora_inicio_jornada'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('hora_termino_jornada'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('afp'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('salud'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('isapre'),
                        css_class='col-md-4'
                    ),
                    css_class='row'
                ),
            )
        )


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


class FiniquitoForm(forms.ModelForm):
    class Meta:
        model = Finiquito
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
        super(FiniquitoForm, self).__init__(*args, **kwargs)
        self.fields['razon_baja'].widget.attrs['class'] = 'chosen'
        self.helper = FormHelper()
        self.helper.form_tag = False
