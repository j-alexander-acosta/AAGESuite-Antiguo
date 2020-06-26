from django import forms
from crispy_forms.helper import FormHelper
from .models import Funcionario, Entrevista, Archivo, Vacacion, TipoLicencia, Licencia


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'

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


class VacacionForm(forms.ModelForm):
    class Meta:
        model = Vacacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class TipoLicenciaForm(forms.ModelForm):
    class Meta:
        model = TipoLicencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoLicenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LicenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
