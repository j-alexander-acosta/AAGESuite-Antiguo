from django.contrib import admin
from rrhh.models import *


@admin.register(base.TipoLicencia)
class TipoLicenciaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'total_dias',
    )
    search_fields = ['nombre']


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


@admin.register(base.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'numero_romano',
        'nombre',
    )
    search_fields = ['nombre']


@admin.register(base.Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'region',
    )
    search_fields = ['nombre', 'region']
    list_filter = ['region']


@admin.register(base.Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'comuna',
    )
    search_fields = ['nombre']
    list_filter = ['comuna', 'comuna__region']


@admin.register(base.TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'indicaciones',
    )
    search_fields = ['nombre']