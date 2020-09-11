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
            'horas_no_aula',
            'especialidad',
            'fundacion',
            'colegio',
            'adventista',
            'directivo'
        ]
        labels = {
            'horas': u'Horas de contrato en docencia de aula',
            'horas_no_aula': u'Horas de contrato en docencia no aula',
            'fundacion': 'Fundación que lo contrata',
            'directivo': '¿Es directivo?'
        }
        widgets = {
            'horas': forms.NumberInput(attrs={'step': '1'}),
            'horas_no_aula': forms.NumberInput(attrs={'step': '1'}),
        }

    def clean(self):
        cleaned_data = super(ProfesorForm, self).clean()

        if self.instance and self.instance.asignacion_set.count() > 0:
            if self.fields['horas'].has_changed(self.instance.horas, cleaned_data['horas']):
                raise forms.ValidationError("No se pueden modificar horas de contrato mientras tenga asignaciones.")

        if self.instance and self.instance.asignacionnoaula_set.count() >0:
            if self.fields['horas_no_aula'].has_changed(self.instance.horas_no_aula, cleaned_data['horas_no_aula']):
                raise forms.ValidationError("No se pueden modificar horas de contrato mientras tenga asignaciones.")


        if cleaned_data['horas'] + cleaned_data['horas_no_aula'] > 44:
            raise forms.ValidationError("La suma de horas de aula y no aula no debe superar 44 horas.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        colegio = kwargs.pop('colegio', None)
        fundacion = kwargs.pop('fundacion', None)
        super(ProfesorForm, self).__init__(*args, **kwargs)

        if user:
            if not user.is_superuser:
                self.fields['fundacion'].queryset = self.fields['fundacion'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")])
        else:
            del(self.fields['fundacion'])
        
        if colegio:
            self.fields['fundacion'].initial = fundacion
            self.fields['fundacion'].disabled = True
            self.fields['colegio'].initial = colegio
            self.fields['colegio'].disabled = True

        self.helper = FormHelper()
        self.helper.form_tag = False


class AsistenteForm(forms.ModelForm):
    """
        Formulario para crear y editar un asistente

    """

    class Meta:
        model = models.Asistente
        fields = [
            'nombre',
            'horas',
            'funcion',
            'fundacion',
            'colegio',
            'adventista',
        ]
        labels = {
            'horas': u'Horas de contrato',
            'fundacion': 'Fundación que lo contrata'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        colegio = kwargs.pop('colegio', None)
        fundacion = kwargs.pop('fundacion', None)
        super(AsistenteForm, self).__init__(*args, **kwargs)

        if colegio:
            self.fields['fundacion'].initial = fundacion
            self.fields['fundacion'].disabled = True
            self.fields['colegio'].initial = colegio
            self.fields['colegio'].disabled = True

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
        user = kwargs.pop('user', None)
        colegio = kwargs.pop('colegio', None)
        super(AsignaturaBaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        if colegio:
            self.fields['plan'].queryset = self.fields['plan'].queryset.filter(colegio__pk=colegio)
        else:
            if user and not user.is_superuser:
                self.fields['plan'].queryset = self.fields['plan'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")]).distinct()


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
