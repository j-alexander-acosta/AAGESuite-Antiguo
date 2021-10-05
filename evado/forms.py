# -*- coding: utf-8 -*-
from django import forms
from easy_select2.widgets import Select2, Select2Multiple
from parsley.decorators import parsleyfy
from django_summernote.widgets import SummernoteWidget
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Div, HTML

from rrhh.models import Contrato, Persona
from evado.models import UniversoEncuesta, Encuesta, PreguntaEncuesta, Respuesta, PeriodoEncuesta
from evado.models import CorreoUniversoEncuesta, TipoUniversoEncuesta, ConfigurarEncuestaUniversoPersona


@parsleyfy
class UniversoEncuestaForm(forms.ModelForm):
    class Meta:
        model = UniversoEncuesta
        fields = '__all__'
        # widgets = {
        #     'contenido_email': SummernoteWidget(),
        # }
        help_texts = {
            'activar_campo_comentario': u"Marque si desea habilitar el campo de comentarios"
                                        u"y observaciones para los encuestados"
        }

    def __init__(self, *args, **kwargs):
        super(UniversoEncuestaForm, self).__init__(*args, **kwargs)
        self.fields['encuesta'].widget.attrs['class'] = 'select2'
        self.fields['tipo_encuesta'].widget.attrs['class'] = 'select2'
        self.fields['activar_campo_comentario'].label = "Activar Campo de Observaciones"
        self.fields['config_universo_persona'].queryset = ConfigurarEncuestaUniversoPersona.objects.all()
        self.fields['inicio'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'type': 'date'}),
            input_formats=['%Y-%m-%d']
        )
        self.fields['fin'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'type': 'date'}),
            input_formats=['%Y-%m-%d']
        )
        self.fields['contenido_email'].widget.attrs = {'class': 'summernote'}
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Configuración de la encuesta',
                Div(
                    Div(Field('encuesta'), css_class="col-md-4"),
                    Div(Field('tipo_encuesta'), css_class="col-md-4"),
                    Div(Field('activar_campo_comentario'), css_class="col-md-4"),
                    css_class="row"
                ),
                'contenido_email',
            ),
            Fieldset(
                'Seleccione el universo de personas',
                Div(
                    HTML(
                        '<a href="javascript:void(0);" id="select_all" type="button" class="float-right">'
                        '<i class="uil-check"></i> Seleccionar todo</a>'
                    ),
                    Field('config_universo_persona', css_class='select2')
                ),
            ),
            # Fieldset(
            #   'Seleccionar Cursos Disponibles',
            #   Field('cursos'),
            # ),
            Fieldset(
                'Tiempo disponible',
                Div(
                    Div(
                        Field('inicio', css_class='datepicker'),
                        css_class='col-md-6',
                    ),
                    Div(
                        Field('fin', css_class='datepicker'),
                        css_class='col-md-6',
                    ),
                    css_class='row',
                ),
            ),
        )


class PreguntaEncuestaForm(forms.ModelForm):
    class Meta:
        model = PreguntaEncuesta
        exclude = ['encuesta']

    def __init__(self, *args, **kwargs):
        super(PreguntaEncuestaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'pregunta-encuesta-id'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


class PreguntaEncuestaItemForm(forms.ModelForm):
    class Meta:
        model = PreguntaEncuesta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PreguntaEncuestaItemForm, self).__init__(*args, **kwargs)
        self.fields['pregunta'].widget.attrs['rows'] = "4"
        self.fields['pregunta'].widget.attrs['class'] = "input-sm"
        self.fields['categoria'].widget.attrs['class'] = "input-sm"
        self.fields['tipo_respuesta'].widget.attrs['class'] = "input-sm"
        self.helper = FormHelper()
        self.helper.form_id = "formset_encuesta_preguntas"
        self.helper.template = 'encuesta/partials/table_inline_formset.html'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-info btn-lg'))


class RespuestaEncuestaItem(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    correlativo = forms.IntegerField(required=False)
    pregunta = forms.CharField(widget=forms.Textarea({'rows': 2}), required=False)
    respuesta_select = forms.ChoiceField(
        label="Respuesta"
    )

    def __init__(self, *args, **kwargs):
        super(RespuestaEncuestaItem, self).__init__(*args, **kwargs)
        self.fields['correlativo'].widget.attrs['disabled'] = True
        self.fields['pregunta'].widget.attrs['disabled'] = True
        self.fields['correlativo'].widget.attrs['class'] = ""
        self.fields['correlativo'].widget.attrs['style'] = "width: 100px"
        self.fields['respuesta_select'].queryset = Respuesta.objects.values_list('id', 'respuesta')
        self.fields['respuesta_select'].widget.attrs['data-bv-notempty'] = "true"
        self.fields['respuesta_select'].widget.attrs['data-bv-notempty-message'] = "Seleccione una opción válida."
        self.helper = FormHelper()
        self.helper.form_id = "encuestaForm"
        self.helper._form_method = "POST"
        self.helper._form_action = ""
        self.helper.template = 'encuesta/partials/table_inline_formset.html'
        self.helper.attrs['data-bv-feedbackicons-valid'] = "glyphicon glyphicon-ok"
        self.helper.attrs['data-bv-feedbackicons-invalid'] = "glyphicon glyphicon-remove"
        self.helper.attrs['data-bv-feedbackicons-validating'] = "glyphicon glyphicon-refresh"
        self.helper.add_input(Submit('submit', 'Enviar', css_class='btn btn-warning btn-lg'))


class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = '__all__'
        widgets = {
            'descripcion': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(EncuestaForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs['class'] = "form-control"


class PeriodoEncuestaForm(forms.ModelForm):
    class Meta:
        model = PeriodoEncuesta
        fields = '__all__'

        help_texts = {
            'activo': u"Marque si se lo permite, en caso contrario, utilice la opcion de cambio de periodo"
        }

    def __init__(self, *args, **kwargs):
        super(PeriodoEncuestaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class CorreoUniversoEncuestaForm(forms.ModelForm):
    class Meta:
        model = CorreoUniversoEncuesta
        exclude = ['enviado']

    def __init__(self, *args, **kwargs):
        super(CorreoUniversoEncuestaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "correoUniversoEncuestaForm"
        self.helper._form_method = "POST"
        self.helper._form_action = "."
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-warning btn-lg'))


class ConfigurarUniversoPersonaForm(forms.Form):
    pe = Persona.objects.all()
    persona = forms.ModelChoiceField(
        queryset=pe,
        label="Evaluador"
    )
    evaluados = forms.ModelMultipleChoiceField(
        queryset=pe,
        label="Evaluados"
    )
    tipo_encuesta = forms.ModelChoiceField(
        queryset=TipoUniversoEncuesta.objects.all(),
        label="Tipo de Universo de Encuesta"
    )
    periodo = forms.ModelChoiceField(
        queryset=PeriodoEncuesta.objects.all(),
        label="Periodo de Encuesta"
    )

    def __init__(self, *args, **kwargs):
        super(ConfigurarUniversoPersonaForm, self).__init__(*args, **kwargs)
        self.fields['persona'].widget.attrs['class'] = 'select2'
        self.fields['evaluados'].widget.attrs['class'] = 'select2'
        self.fields['periodo'].widget.attrs['class'] = 'select2'
        self.fields['tipo_encuesta'].widget.attrs['class'] = 'select2'
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.form_id = "configurarUniversoPersonaForm"
        # self.helper._form_method = "POST"
        # self.helper._form_action = "."
        # self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-success'))
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        Field('persona'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('periodo'),
                        css_class='col-md-6'
                    ),
                    css_class="row"
                ),
                Div(
                    Div(
                        Field('evaluados'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('tipo_encuesta'),
                        css_class='col-md-6'
                    ),
                    css_class="row"
                )
            )
        )


class ImportarConfiguracionUniversoPersonaForm(forms.Form):
    file = forms.FileField(
        label="Subir archivo de configuración",
        help_text="*Se admiten archivos XLS, XLSX (ver plantilla)"
    )
    periodo_encuesta = forms.ModelChoiceField(
        queryset=PeriodoEncuesta.objects.all(),
        label="Periodo de Encuesta"
    )
    tipo_universo_encuesta = forms.ModelChoiceField(
        queryset=TipoUniversoEncuesta.objects.all(),
        label="Tipo de Universo de Encuesta"
    )

    def __init__(self, *args, **kwargs):
        super(ImportarConfiguracionUniversoPersonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('file'), css_class='col-md-4'),
                Div(Field('periodo_encuesta'), css_class='col-md-4'),
                Div(Field('tipo_universo_encuesta'), css_class='col-md-4'),
                css_class="row"
            )
        )


class MailEncuestaUniversoForm(forms.Form):
    motivo = forms.CharField(label="Encabezado")
    contenido_mail = forms.CharField(label="Contenido Mail", widget=forms.Textarea())
    universo_encuesta = forms.ModelMultipleChoiceField(
        label="Universos Encuestas",
        queryset=UniversoEncuesta.objects.all()
    )
    personas = forms.ModelMultipleChoiceField(label="Personas", queryset=Persona.objects.all())

    def __init__(self, *args, **kwargs):
        super(MailEncuestaUniversoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('motivo'),
            Field('contenido_mail'),
            Fieldset('Seleccione el universo encuesta',
                     Field('universo_encuesta', css_class='shuttle_select'),
                     ),
            Fieldset('Personas',
                     Field('personas', css_class='shuttle_select'),
                     ),

            Div(
                StrictButton('Enviar', css_class='btn-danger btn-lg', type="submit"),
                align="center",
            ),
        )


class TipoUniversoEncuestaForm(forms.ModelForm):
    class Meta:
        model = TipoUniversoEncuesta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoUniversoEncuestaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
