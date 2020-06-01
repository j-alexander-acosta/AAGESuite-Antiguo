from django import forms
from crispy_forms.helper import FormHelper
from .models import Funcionario
from .models import Entrevista
from .models import Archivo


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('nombre',
                  'rut',
                  'fecha_nacimiento',
                  'fecha_ingreso',
                  'titulo',
                  'religion',
                  'estado_civil',
                  'nacionalidad',
                  'sexo',
                  'email',
                  'direccion',
                  'telefono')

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        

class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = ('funcionario',
                  'entrevistador',
                  'tipo',
                  'contenido',
                  'acuerdos')

    def __init__(self, *args, **kwargs):
        super(EntrevistaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('descripcion',
                  'archivo',
                  'funcionario')

    def __init__(self, *args, **kwargs):
        super(ArchivoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
