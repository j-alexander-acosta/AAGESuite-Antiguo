from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from .models import Funcionario, Entrevista, Archivo, Vacacion, TipoLicencia, Licencia


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = ('funcionario',
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
                  'funcionario')

    def __init__(self, *args, **kwargs):
        super(ArchivoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class VacacionForm(forms.ModelForm):
    class Meta:
        model = Vacacion
        fields = [
            'funcionario',
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
        self.fields['funcionario'].widget.attrs['class'] = 'chosen'
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
            'funcionario',
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
        self.fields['funcionario'].widget.attrs['class'] = 'chosen'
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
            'funcionario',
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
            'funcionario': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(LicenciaTipoFuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['tipo_licencia'].widget.attrs['class'] = 'chosen'
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'funcionario',
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
            'funcionario',
            'total_dias',
            'fecha_inicio',
            'fecha_termino',
            'fecha_retorno',
            'total_feriados',
            'dias_pendiente',
            'es_pendiente',
        ]
        widgets = {
            'funcionario': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(VacacionFuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_termino'].widget.attrs['class'] = 'datepicker'
        self.fields['fecha_retorno'].widget.attrs['class'] = 'datepicker'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'funcionario',
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
