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
        self.helper.form_tag = False
        


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
        self.helper.form_tag = False



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
        self.helper.form_tag = False