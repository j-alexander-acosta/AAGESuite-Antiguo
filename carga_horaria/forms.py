from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field, Submit
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import ModelChoiceField

from carga_horaria import models

class PeriodoForm(forms.ModelForm):
    """
        Formulario para crear y editar un periodo

    """

    class Meta:
        model = models.Periodo
        fields = [
            'nombre',
            'colegio',
            'plan'
        ]
        help_texts = {
            'nombre': u"Defina un nombre de periodo",
            'colegio': u"Establece si el periodo es el usado actualmente en la aplicación."
        }
        labels = {
            'plan': u"Plan"
        }

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)
#        self.fields['activo'].widget.attrs['class'] = ""
        self.helper = FormHelper()
        self.helper.form_id = 'id-periodoForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'nombre'
                    ),
                    css_class="col-md-6"
                ),
                Div(
                    Field(
                        'colegio'
                    ),
                    css_class="col-md-6"
                ),
                Div(
                    Field(
                        'plan'
                    ),
                    css_class="col-md-6"
                ),
                css_class="row",
            ),
            HTML(
                "<br>"
                "<div class='text-center'>"
                "<div class='btn-group'>"
                "<a href='{% url 'carga-horaria:periodos' %}' class='btn btn-lg btn-dark'>"
                "<i class='fa fa-arrow-left'></i> "
                "Volver</a>"
                "<button type='submit' class='btn btn-lg btn-info'>"
                "<i class='fa fa-save'></i> "
                "Guardar </button>"
                "</div>"
                "</div>"
            )
        )


class ColegioForm(forms.ModelForm):
    """
        Formulario para crear y editar un Colegio

    """

    class Meta:
        model = models.Colegio
        myBoolField = forms.BooleanField(
        label='jec', 
        required=False,
        initial=False
     )
        fields = [
            'nombre',
            'jec'
        ]
        help_texts = {
            'nombre': u"Defina un nombre para el colegio",
            'jec': u"Marque solo si el colegio tiene Jornada Escolar Completa."
        }


    def __init__(self, *args, **kwargs):
        super(ColegioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-colegioForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'nombre'
                    ),
                    css_class="col-md-6"
                ),
                Div(
                    Field(
                        'jec'
                    ),
                    css_class="col-md-6"
                ),
                css_class="row",
            ),
            HTML(
                "<br>"
                "<div class='text-center'>"
                "<div class='btn-group'>"
                "<a href='{% url 'carga-horaria:colegios' %}' class='btn btn-lg btn-dark'>"
                "<i class='fa fa-arrow-left'></i> "
                "Volver</a>"
                "<button type='submit' class='btn btn-lg btn-info'>"
                "<i class='fa fa-save'></i> "
                "Guardar </button>"
                "</div>"
                "</div>"
            )
        )


class PlanForm(forms.ModelForm):
    """
        Formulario para crear y editar un Plan

    """

    class Meta:
        model = models.Plan
        fields = [
            'nombre',
            'nivel'
        ]
        help_texts = {
            'nombre': u"Defina un nombre para el Plan",
            'nivel': u"Seleccione el nivel a Asociar a su Plan."
        }


    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-planForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'nombre'
                    ),
                    css_class="col-md-6"
                ),
                Div(
                    Field(
                        'nivel'
                    ),
                    css_class="col-md-6"
                ),
                css_class="row",
            ),
            HTML(
                "<br>"
                "<div class='text-center'>"
                "<div class='btn-group'>"
                "<a href='{% url 'carga-horaria:planes' %}' class='btn btn-lg btn-dark'>"
                "<i class='fa fa-arrow-left'></i> "
                "Volver</a>"
                "<button type='submit' class='btn btn-lg btn-info'>"
                "<i class='fa fa-save'></i> "
                "Guardar </button>"
                "</div>"
                "</div>"
            )
        )