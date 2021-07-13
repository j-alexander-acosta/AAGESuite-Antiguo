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
from localflavor.cl.forms import CLRutField

from carga_horaria import models


class ProfesorForm(forms.ModelForm):
    """
        Formulario para crear y editar un profesor

    """
    rut = CLRutField(label="RUT")
    nombre = forms.CharField()
    direccion = forms.CharField()
    comuna = forms.CharField(required=False)
    nacionalidad = forms.CharField(required=False)
    telefono = forms.CharField(label='Teléfono', required=False)
    email_personal = forms.EmailField(required=False)
    email_institucional = forms.EmailField(required=False)
    estado_civil = forms.ChoiceField(choices=models.Persona.ESTADO_CIVIL_CHOICES)
    discapacidad = forms.BooleanField(required=False)
    recibe_pension = forms.BooleanField(required=False)
    adventista = forms.BooleanField(required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
    fecha_inicio = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])

    class Meta:
        model = models.Profesor
        fields = [
            'rut',
            'nombre',
            'direccion',
            'comuna',
            'nacionalidad',
            'telefono',
            'email_personal',
            'email_institucional',
            'estado_civil',
            'discapacidad',
            'recibe_pension',
            'adventista',
            'fecha_nacimiento',
            'tipo',
            'fecha_inicio',
            'horas',
            'horas_indefinidas',
            'horas_plazo_fijo',
            'especialidad',
            'fundacion',
            'colegio',
            'cargo',
            'observaciones'
        ]
        labels = {
            'horas': u'Horas contratadas',
            'fundacion': 'Fundación que lo contrata',
        }
        widgets = {
            'horas': forms.NumberInput(attrs={'step': '1'}),
        }

    def clean(self):
        cleaned_data = super(ProfesorForm, self).clean()

        # if cleaned_data['horas'] > 44:
        #     raise forms.ValidationError("La suma de horas de aula y no aula no debe superar 44 horas.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        colegio = kwargs.pop('colegio', None)
        fundacion = kwargs.pop('fundacion', None)
        super(ProfesorForm, self).__init__(*args, **kwargs)

        if colegio:
            self.fields['fundacion'].initial = fundacion
            self.fields['fundacion'].disabled = True
            self.fields['colegio'].initial = colegio
            self.fields['colegio'].disabled = True

        if user:
            if not user.is_superuser:
                self.fields['fundacion'].queryset = self.fields['fundacion'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")]).distinct()
        else:
            del(self.fields['fundacion'])
        
        if self.instance.pk:
            self.fields['nombre'].initial = self.instance.persona.nombre
            self.fields['direccion'].initial = self.instance.persona.direccion
            self.fields['comuna'].initial = self.instance.persona.comuna
            self.fields['nacionalidad'].initial = self.instance.persona.nacionalidad
            self.fields['telefono'].initial = self.instance.persona.telefono
            self.fields['email_personal'].initial = self.instance.persona.email_personal
            self.fields['email_institucional'].initial = self.instance.persona.email_institucional
            self.fields['estado_civil'].initial = self.instance.persona.estado_civil
            self.fields['discapacidad'].initial = self.instance.persona.discapacidad
            self.fields['recibe_pension'].initial = self.instance.persona.recibe_pension
            self.fields['rut'].initial = self.instance.persona.rut
            self.fields['adventista'].initial = self.instance.persona.adventista
            self.fields['fecha_nacimiento'].initial = self.instance.persona.fecha_nacimiento

        self.helper = FormHelper()
        self.helper.form_tag = False


class AsistenteForm(forms.ModelForm):
    """
        Formulario para crear y editar un asistente

    """
    rut = CLRutField(label="RUT")
    nombre = forms.CharField()
    direccion = forms.CharField()
    comuna = forms.CharField(required=False)
    nacionalidad = forms.CharField(required=False)
    telefono = forms.CharField(label='Teléfono', required=False)
    email_personal = forms.EmailField(required=False)
    email_institucional = forms.EmailField(required=False)
    estado_civil = forms.ChoiceField(choices=models.Persona.ESTADO_CIVIL_CHOICES, required=False)
    discapacidad = forms.BooleanField(required=False)
    recibe_pension = forms.BooleanField(required=False)
    adventista = forms.BooleanField(required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
    fecha_inicio = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])
    class Meta:
        model = models.Asistente
        fields = [
            'rut',
            'nombre',
            'direccion',
            'comuna',
            'nacionalidad',
            'telefono',
            'email_personal',
            'email_institucional',
            'estado_civil',
            'discapacidad',
            'recibe_pension',
            'adventista',
            'fecha_nacimiento',
            'direccion',
            'fecha_inicio',
            'horas',
            'funcion',
            'fundacion',
            'colegio',
            'observaciones'
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
                self.fields['fundacion'].queryset = self.fields['fundacion'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")]).distinct()
        else:
            del(self.fields['fundacion'])
        
        if self.instance.pk:
            self.fields['nombre'].initial = self.instance.persona.nombre
            self.fields['direccion'].initial = self.instance.persona.direccion
            self.fields['comuna'].initial = self.instance.persona.comuna
            self.fields['nacionalidad'].initial = self.instance.persona.nacionalidad
            self.fields['telefono'].initial = self.instance.persona.telefono
            self.fields['email_personal'].initial = self.instance.persona.email_personal
            self.fields['email_institucional'].initial = self.instance.persona.email_institucional
            self.fields['estado_civil'].initial = self.instance.persona.estado_civil
            self.fields['discapacidad'].initial = self.instance.persona.discapacidad
            self.fields['recibe_pension'].initial = self.instance.persona.recibe_pension
            self.fields['rut'].initial = self.instance.persona.rut
            self.fields['adventista'].initial = self.instance.persona.adventista
            self.fields['fecha_nacimiento'].initial = self.instance.persona.fecha_nacimiento


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
            'combinable',
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
