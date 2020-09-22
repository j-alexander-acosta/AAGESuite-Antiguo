from django.contrib import admin
from .models import Persona, Vacacion, TipoLicencia, Licencia
from .models import Contrato, Funcion, AFP, Isapre, Finiquito


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'rut',
        'get_full_name',
    )
    search_fields = ['rut', 'get_full_name']
    list_filter = ['religion', 'titulo', 'casa_formadora', 'nacionalidad']


@admin.register(Vacacion)
class VacacionAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'total_dias',
        'fecha_inicio'
    )
    search_fields = ['contrato__persona__rut', 'contrato__persona__get_full_name']


@admin.register(TipoLicencia)
class TipoLicenciaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'total_dias',
    )
    search_fields = ['nombre']


@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'tipo_licencia',
        'tipo_licencia_descripcion',
        'folio_licencia'
    )
    search_fields = [
        'contrato__persona__rut',
        'contrato__persona__get_full_name',
        'tipo_licencia__nombre',
        'tipo_licencia_descripcion'
    ]
    list_filter = ['tipo_licencia']


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'colegio',
        'categoria',
        #'vigente'
    )
    search_fields = [
        'persona__rut',
        'persona__get_full_name',
        'colegio__nombre'
    ]
    list_filter = [
        'colegio',
        'categoria',
        'tipo_contrato',
        'salud'
    ]


@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo',
        'descripcion'
    )
    search_fields = ['nombre']
    list_filter = ['tipo']


@admin.register(AFP)
class AFPAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
    )
    search_fields = ['nombre']


@admin.register(Isapre)
class IsapreAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
    )
    search_fields = ['nombre']


@admin.register(Finiquito)
class FiniquitoAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'razon_baja',
    )
    search_fields = ['contrato__persona__rut']
