from django.contrib import admin
from rrhh.models import *


@admin.register(persona.Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'rut',
        'get_full_name',
    )
    search_fields = ['rut', 'get_full_name']
    list_filter = ['religion', 'titulado', 'profesion', 'nacionalidad']


@admin.register(persona.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        'persona',
        'estado',
    )
    search_fields = ['persona__rut', 'persona__get_full_name']
    list_filter = ['afp', 'salud', 'isapre', 'estado', 'tipo_misionero']


@admin.register(colegio.VacacionFuncionarioColegio)
class VacacionFuncionarioColegioAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'total_dias',
        'fecha_inicio'
    )
    search_fields = ['contrato__persona__rut', 'contrato__persona__get_full_name']


@admin.register(base.TipoLicencia)
class TipoLicenciaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'total_dias',
    )
    search_fields = ['nombre']


@admin.register(colegio.LicenciaFuncionarioColegio)
class LicenciaFuncionarioColegioAdmin(admin.ModelAdmin):
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


@admin.register(colegio.ContratoColegio)
class ContratoColegioAdmin(admin.ModelAdmin):
    list_display = (
        'funcionario',
        'colegio',
        'categoria',
        #'vigente'
    )
    search_fields = [
        'funcionario__persona__rut',
        'funcionario__persona__get_full_name',
        'colegio__nombre'
    ]
    list_filter = [
        'colegio',
        'categoria',
        'tipo_contrato'
    ]


@admin.register(base.Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo',
        'descripcion'
    )
    search_fields = ['nombre']
    list_filter = ['tipo']


@admin.register(base.AFP)
class AFPAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
    )
    search_fields = ['nombre']


@admin.register(base.Isapre)
class IsapreAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
    )
    search_fields = ['nombre']


@admin.register(colegio.FiniquitoColegio)
class FiniquitoColegioAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'razon_baja',
    )
    search_fields = ['contrato__persona__rut']


@admin.register(colegio.Entrevista)
class EntrevistaAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'tipo',
    )
    search_fields = ['contrato__persona__rut']


@admin.register(colegio.Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'colegio',
        'cargo',
    )
    search_fields = ['colegio', 'cargo']
    list_filter = ['colegio']


@admin.register(colegio.EstadoSolicitud)
class EstadoSolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'solicitud',
        'estado',
    )
    search_fields = ['solicitud__colegio']
    list_filter = ['solicitud__colegio']


@admin.register(colegio.EstadoContratacion)
class EstadoContratacionAdmin(admin.ModelAdmin):
    list_display = (
        'contrato',
        'estado',
    )
    search_fields = ['contrato', 'contrato__colegio', 'contrato__funcionario']
    list_filter = ['contrato__colegio', 'estado']
