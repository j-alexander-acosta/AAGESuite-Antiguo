from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from django.contrib.auth.models import User

from rrhh.models.base import Perfil, Banco, AFP, Isapre, Funcion, TipoLicencia, TipoDocumento, TipoTitulo, AreaTitulo
from rrhh.models.base import Especialidad, Mencion
from rrhh.models.union import Union
from rrhh.models.fundacion import Fundacion
from rrhh.models.colegio import Colegio


class UnionForm(forms.ModelForm):
    class Meta:
        model = Union
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UnionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class FundacionForm(forms.ModelForm):
    class Meta:
        model = Fundacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FundacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ColegioForm(forms.ModelForm):
    class Meta:
        model = Colegio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ColegioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class UserForm(forms.ModelForm):
    """
        Formulario para crear un usuario
    """

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class UserUpdateForm(forms.ModelForm):
    """
        Formulario para editar un usuario
    """

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        help_texts = {
            'solo_lectura': u"Marque si el perfil que está creando, será solo para lectura",
        }

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BancoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AFPForm(forms.ModelForm):
    class Meta:
        model = AFP
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AFPForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class IsapreForm(forms.ModelForm):
    class Meta:
        model = Isapre
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IsapreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class FuncionForm(forms.ModelForm):
    class Meta:
        model = Funcion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FuncionForm, self).__init__(*args, **kwargs)
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


class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoDocumentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class TipoTituloForm(forms.ModelForm):
    class Meta:
        model = TipoTitulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoTituloForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AreaTituloForm(forms.ModelForm):
    class Meta:
        model = AreaTitulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AreaTituloForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EspecialidadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class MencionForm(forms.ModelForm):
    class Meta:
        model = Mencion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MencionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
