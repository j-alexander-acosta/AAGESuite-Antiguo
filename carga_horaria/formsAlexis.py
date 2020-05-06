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

class ProfesorForm(forms.ModelForm):
    """
        Formulario para crear y editar un profesor

    """

    class Meta:
        model = models.Profesor
        fields = [
            'nombre',
            'horas'
        ]
        help_texts = {
            'horas': u"Horas por la que se contrato al Profesor."
        }

    def __init__(self, *args, **kwargs):
        super(ProfesorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


# class CursoForm(forms.ModelForm):
#     """
#         Formulario para crear y editar un curso
#     """

#     class Meta:
#         model = models.Curso
#         fields = [
#             'periodo',
#             'letra'
#         ]

#     def __init__(self, *args, **kwargs):
#         super(CursoForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = False


class AsignaturaBaseForm(forms.ModelForm):
    """
        Formulario para crear y editar una asignatura base
    """

    class Meta:
        model = models.AsignaturaBase
        fields = [
            'nombre',
            'plan',
            'horas_jec',
            'horas_nec'
        ]

        labels = {
            'horas_jec': u'Horas con Jornada Escolar Completa',
            'horas_nec': u'Horas sin Jornada Escolar Completa',
        }

    def __init__(self, *args, **kwargs):
        super(AsignaturaBaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AsignaturaForm(forms.ModelForm):
    """
        Formulario para crear y editar una asignatura
    """

    class Meta:
        model = models.Asignatura
        fields = [
            'base',
            'periodo',
            'horas',
        ]

        labels = {
            'base': u'Asigantura Base',
            'periodo': u'Curso',
        }

    def __init__(self, *args, **kwargs):
        super(AsignaturaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
