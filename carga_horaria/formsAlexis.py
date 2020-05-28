from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field, Submit
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import ModelChoiceField
from guardian.shortcuts import get_objects_for_user

from carga_horaria import models

class ProfesorForm(forms.ModelForm):
    """
        Formulario para crear y editar un profesor

    """

    class Meta:
        model = models.Profesor
        fields = [
            'nombre',
            'horas',
            'especialidad',
            'fundacion'
        ]
        labels = {
            'horas': u'Horas de contrato',
            'fundacion': 'Fundación que lo contrata'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfesorForm, self).__init__(*args, **kwargs)

        if user:
            if not user.is_superuser:
                self.fields['fundacion'].queryset = self.fields['fundacion'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")])
        else:
            del(self.fields['fundacion'])
        
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


class AsignaturaUpdateForm(forms.ModelForm):
    """
        Formulario para editar una asignatura
    """

    class Meta:
        model = models.Asignatura
        fields = [
            'horas',
        ]

    def __init__(self, *args, **kwargs):
        super(AsignaturaUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AsignaturaCreateForm(forms.ModelForm):
    """
        Formulario para crear una asignatura
    """

    class Meta:
        model = models.Asignatura
        fields = [
            'nombre',
            'horas',
        ]

        labels = {
            'nombre': u'Nombre de nueva asignatura',
        }
        # help_texts = {
        #     'base': u"Para crear una asignatura extra al plan original, deje este campo en blanco."
        # }

    def __init__(self, *args, **kwargs):
        super(AsignaturaCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
