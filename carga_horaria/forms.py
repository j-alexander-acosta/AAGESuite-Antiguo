from django import forms
from crispy_forms.helper import FormHelper
from .models import Asignacion
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
        super(AsignacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # profesores = [(p, "{} - {} horas".format(p, p.horas_disponibles)) for p in Profesor.objects.all()]
        # self.fields['profesor'] = forms.ChoiceField(choices=profesores)
