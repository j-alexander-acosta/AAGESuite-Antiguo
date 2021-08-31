# -*- coding: utf-8 -*-
from django import forms
from parsley.decorators import parsleyfy
from django_summernote.widgets import SummernoteWidget
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Div

from rrhh.models import ContratoColegio, Persona
from evado.models import UniversoEncuesta, Encuesta, PreguntaEncuesta, Respuesta, PeriodoEncuesta
from evado.models import CorreoUniversoEncuesta, TipoUniversoEncuesta, ConfigurarEncuestaUniversoPersona


@parsleyfy
class UniversoEncuestaForm(forms.ModelForm):
    class Meta:
        model = UniversoEncuesta
        fields = '__all__'
        widgets = {
            'contenido_email': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(UniversoEncuestaForm, self).__init__(*args, **kwargs)
        self.fields['activar_campo_comentario'].label = "Activar Campo de Observaciones"
        self.fields['config_universo_persona'].queryset = ConfigurarEncuestaUniversoPersona.objects.all()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Configuración de la encuesta',
                'encuesta',
                'contenido_email',
                'tipo_encuesta',
                Field('activar_campo_comentario'),
            ),
            Fieldset(
                'Seleccione el universo de personas',
                Field('config_universo_persona', css_class='multiselect'),
            ),
            # Fieldset(
            #   'Seleccionar Cursos Disponibles',
            #   Field('cursos'),
            # ),
            Fieldset(
                'Tiempo disponible',
                Div(
                    Div(
                        Field('inicio', css_class='dateinput'),
                        css_class='col-md-5 col-md-offset-1',
                    ),
                    Div(
                        Field('fin', css_class='dateinput'),
                        css_class='col-md-5 col-md-offset-1',
                    ),
                    css_class='row',
                ),
            ),
            Div(
                StrictButton('Guardar', css_class='btn-success btn-lg', type="submit"),
                align="center",
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
    # respuesta_select = forms.ChoiceField(
    #     label="Respuesta",
    #     choices=Respuesta.objects.values_list('id', 'respuesta')
    # )

    def __init__(self, *args, **kwargs):
        super(RespuestaEncuestaItem, self).__init__(*args, **kwargs)
        self.fields['correlativo'].widget.attrs['disabled'] = True
        self.fields['pregunta'].widget.attrs['disabled'] = True
        self.fields['correlativo'].widget.attrs['class'] = ""
        self.fields['correlativo'].widget.attrs['style'] = "width: 100px"
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

    def __init__(self, *args, **kwargs):
        super(PeriodoEncuestaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "PeriodoEncuestaForm"
        self.helper._form_method = "POST"
        self.helper._form_action = "."
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-warning btn-lg'))


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
    pe = ContratoColegio.objects.all()
    persona = forms.ModelChoiceField(
        queryset=pe,
        label="Persona"
    )
    evaluados = forms.ModelMultipleChoiceField(
        queryset=pe,
        label="Evaluados",
    )
    tipo_encuesta = forms.ModelChoiceField(
        queryset=TipoUniversoEncuesta.objects.all()
    )
    periodo = forms.ModelChoiceField(
        queryset=PeriodoEncuesta.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(ConfigurarUniversoPersonaForm, self).__init__(*args, **kwargs)
        self.fields['persona'].widget.attrs = {"class": "select"}
        self.fields['evaluados'].widget.attrs = {"class": "multiselect"}
        self.fields['periodo'].widget.attrs = {"class": "select"}
        self.fields['tipo_encuesta'].widget.attrs = {"class": "select"}
        self.helper = FormHelper()
        self.helper.form_id = "configurarUniversoPersonaForm"
        self.helper._form_method = "POST"
        self.helper._form_action = "."
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-warning btn-lg'))


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
