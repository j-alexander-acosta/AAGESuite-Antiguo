from django import forms
from crispy_forms.helper import FormHelper
from .models import Asignacion

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

    def __init__(self, *args, **kwargs):
        super(AsignacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
