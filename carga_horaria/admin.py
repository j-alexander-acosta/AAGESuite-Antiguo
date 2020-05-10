from django.contrib import admin
from .models import Plan
from .models import AsignaturaBase
from .models import Colegio
from .models import Periodo
from .models import Asignatura
#from .models import Curso
from .models import Profesor
from .models import Asignacion
from .models import AsignacionExtra
from .models import Especialidad


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_filter = ['nivel']
    list_display = (
        'nivel',
#        'creado_en',
#        'modificado_en'
    )

@admin.register(AsignaturaBase)
class AsignaturaBaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horas_jec', 'horas_nec')

@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_filter = ['nombre', 'jec']
    list_display = (
        'nombre',
        'jec',
#        'creado_en',
#        'modificado_en'
    )

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'colegio',
        'plan',
#        'creado_en',
#        'modificado_en'
    )
    search_fields = ['nombre']
    list_filter = ['nombre', 'colegio', 'plan']

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('base', 'horas')

# @admin.register(Curso)
# class CursoAdmin(admin.ModelAdmin):
#     pass

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    pass

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    pass

@admin.register(AsignacionExtra)
class AsignacionExtraAdmin(admin.ModelAdmin):
    pass

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    pass
