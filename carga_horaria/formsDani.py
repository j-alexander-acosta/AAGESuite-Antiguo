from itertools import chain
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
from .models import Colegio
from .models import Plan
from .models import Nivel

from carga_horaria import models

class PeriodoForm(forms.ModelForm):
    """
        Formulario para crear y editar un periodo

    """

    class Meta:
        model = models.Periodo
        fields = [
            'colegio',
            'plan',
            'nombre',
            'horas',
            'horas_dif',
            'horas_adicionales',
            'profesor_jefe'
        ]
        help_texts = {
            'nombre': u"Defina un nombre para el curso",
        }
        labels = {
            'plan': u"Plan",
            'horas': "Horas Libre Disposición",
            'horas_dif': "Horas Educación Diferenciada",
            'horas_adicionales': "Horas Adicionales",
            'profesor_jefe': "Profesor Jefe"
        }

    def clean_horas_dif(self):
        hd = self.cleaned_data['horas_dif']
        nivel = self.cleaned_data['plan'].nivel
        if hd != 0 and nivel not in [Nivel.M3.name, Nivel.M4.name]:
            raise forms.ValidationError("Sólo Tercero y Cuarto medio puede tener horas diferenciadas")
        else:
            return hd

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        colegio = kwargs.pop('colegio', None)
        super(PeriodoForm, self).__init__(*args, **kwargs)

        if colegio:
            self.fields['colegio'].initial = colegio
            self.fields['colegio'].disabled = True

        if colegio:
            cc = Colegio.objects.get(pk=colegio)
            if not cc.jec:
                self.fields['horas'].disabled = True


        if colegio:
            self.fields['plan'].queryset = self.fields['plan'].queryset.filter(colegio__pk=colegio)
        else:
            if user and not user.is_superuser:
                self.fields['plan'].queryset = self.fields['plan'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")]).distinct()

        if colegio:
            self.fields['profesor_jefe'].queryset = self.fields['profesor_jefe'].queryset.filter(colegio__pk=colegio)

            # if self.instance:
            #     assigned = list(chain.from_iterable(filter(None, [aa.asignacion_set.values_list('profesor', flat=True) for aa in self.instance.asignatura_set.all()])))
            #     self.fields['profesor_jefe'].queryset = base_qs.filter(pk__in=[assigned])
            # else:
            #     self.fields['profesor_jefe'].queryset = base_qs

        if user:
            if not user.is_superuser:
                self.fields['colegio'].queryset = get_objects_for_user(user, "carga_horaria.change_colegio")
        else:
            del(self.fields['colegio'])
            
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
            'abrev',
            'fundacion',
            'direccion',
            'ciudad',
            'comuna',
            'telefono',
            'rbd',
            'jec',
            'pie',
            'sep',
            'web',
            'financiamiento',
            'alumnos',
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
            'nivel',
            'colegio'
        ]
        help_texts = {
            'nivel': u"Seleccione el nivel a Asociar a su Plan."
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        colegio = kwargs.pop('colegio', None)
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        if colegio:
            self.fields['colegio'].initial = colegio
            self.fields['colegio'].disabled = True


class PlantillaPlanForm(forms.Form):
    plantilla = forms.ModelChoiceField(label="Plan de estudio que desea copiar", queryset=Plan.objects.all())
    nivel = forms.ChoiceField(label="Curso al que desea agregar el plan", choices=[(tag.name, tag.value) for tag in Nivel])

    def __init__(self, *args, **kwargs):
        super(PlantillaPlanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
