from django import forms
from crispy_forms.helper import FormHelper
from guardian.shortcuts import get_objects_for_user
from .models import Asignacion, AsignacionExtra, AsignacionNoAula
from .models import Profesor

class AsignacionForm(forms.ModelForm):
    """
        Formulario para asignar una asignatura
    """

    class Meta:
        model = Asignacion
        fields = [
            'profesor',
            'horas',
        ]

    def clean_horas(self):
        horas = self.cleaned_data['horas']
        profesor = self.cleaned_data['profesor']
        if horas > profesor.horas_disponibles:
            raise forms.ValidationError("Excede las horas que {} tiene disponibles ({})".format(profesor, profesor.horas_disponibles))
        if self.asignatura and horas > self.asignatura.horas_disponibles:
            raise forms.ValidationError("Excede las horas que {} tiene disponibles ({})".format(self.asignatura, self.asignatura.horas_disponibles))
        return horas

    def __init__(self, *args, **kwargs):
        self.asignatura = kwargs.pop('asignatura', None)
        user = kwargs.pop('user', None)
        super(AsignacionForm, self).__init__(*args, **kwargs)

        if user:
            if not user.is_superuser:
                self.fields['profesor'].queryset = self.fields['profesor'].queryset.filter(fundacion__colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")])
        else:
            # del(self.fields['profesor'])
            self.fields['profesor'].disabled = True

        self.helper = FormHelper()
        self.helper.form_tag = False
        # profesores = [(p, "{} - {} horas".format(p, p.horas_disponibles)) for p in Profesor.objects.all()]
        # self.fields['profesor'] = forms.ChoiceField(choices=profesores)


class AsignacionFUAForm(forms.ModelForm):
    """
        Formulario para asignar lo que se proyecta hacia el universo

        https://youtu.be/SWOz-kIwDuU?t=81
    """

    class Meta:
        model = Asignacion
        fields = [
            'curso',
            'descripcion',
            'horas',
        ]

    def clean_horas(self):
        horas = self.cleaned_data['horas']
        profesor = self.profesor
        if horas > profesor.horas_disponibles:
            raise forms.ValidationError("Excede las horas que {} tiene disponibles ({})".format(profesor, profesor.horas_disponibles))
        return horas

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if not descripcion:
            raise forms.ValidationError("Debe ingresar alguna descripción")
        return descripcion

    def __init__(self, *args, **kwargs):
        self.profesor = kwargs.pop('profesor', None)
        user = kwargs.pop('user', None)
        super(AsignacionFUAForm, self).__init__(*args, **kwargs)

        if user:
            if not user.is_superuser:
                self.fields['curso'].queryset = self.fields['curso'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")])
        else:
            del(self.fields['curso'])

        self.helper = FormHelper()
        self.helper.form_tag = False
        # profesores = [(p, "{} - {} horas".format(p, p.horas_disponibles)) for p in Profesor.objects.all()]
        # self.fields['profesor'] = forms.ChoiceField(choices=profesores)
        self.fields['curso'].empty_label = "Todos"


class AsignacionExtraForm(forms.ModelForm):
    """
        Formulario para asignar una cosa extra
    """

    class Meta:
        model = AsignacionExtra
        fields = [
            'curso',
            'descripcion',
            'horas',
        ]

    def clean_horas(self):
        horas = self.cleaned_data['horas']
        profesor = self.profesor
        if horas > profesor.horas_no_lectivas_disponibles:
            raise forms.ValidationError("Excede las horas que {} tiene disponibles ({})".format(profesor, profesor.horas_no_lectivas_disponibles))
        return horas

    def __init__(self, *args, **kwargs):
        self.profesor = kwargs.pop('profesor', None)
        self.colegio = kwargs.pop('colegio', None)
        user = kwargs.pop('user', None)
        super(AsignacionExtraForm, self).__init__(*args, **kwargs)

        if user:
            if self.colegio:
                self.fields['curso'].queryset = self.fields['curso'].queryset.filter(colegio__pk__in=[self.colegio])
            else:
                if not user.is_superuser:
                    # cursos of owned colegios
                    self.fields['curso'].queryset = self.fields['curso'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")])
        else:
            del(self.fields['curso'])


        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['curso'].empty_label = "Todos"


class AsignacionNoAulaForm(forms.ModelForm):
    """
        Formulario para asignar una cosa NoAula
    """

    class Meta:
        model = AsignacionNoAula
        fields = [
            'curso',
            'descripcion',
            'horas',
        ]

    def clean_horas(self):
        horas = self.cleaned_data['horas']
        profesor = self.profesor
        if horas > profesor.horas_no_aula_disponibles:
            raise forms.ValidationError("Excede las horas que {} tiene disponibles ({})".format(profesor, profesor.horas_no_aula_disponibles))
        return horas

    def __init__(self, *args, **kwargs):
        self.profesor = kwargs.pop('profesor', None)
        user = kwargs.pop('user', None)
        super(AsignacionNoAulaForm, self).__init__(*args, **kwargs)

        if user:
            if not user.is_superuser:
                self.fields['curso'].queryset = self.fields['curso'].queryset.filter(colegio__pk__in=[c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")])
        else:
            del(self.fields['curso'])


        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['curso'].empty_label = "Todos"
