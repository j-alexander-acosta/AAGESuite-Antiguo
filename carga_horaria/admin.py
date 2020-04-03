from django.contrib import admin
from .models import Curso
from .models import Asignatura
from .models import PlanEstudio
from .models import Semestre
from .models import AsignaturaExtra
from .models import CargaHoraria
from .models import TablaTiempoLectivo
from .models import DistribucionTiempoLectivo


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'tipo_ensenanza', 'nivel')
    list_filter = ('tipo_curso', 'periodo', 'nivel', 'jornada')

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_ensenanza', 'tipo_formacion', 'niveles')
    list_filter = ('tipo_ensenanza', 'lengua_indigena')
    search_fields = ('nombre',)

@admin.register(PlanEstudio)
class PlanEstudioAdmin(admin.ModelAdmin):
    list_display = ('curso', 'asignatura')

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'periodo', 'fecha_inicio', 'fecha_termino')
    list_filter = ('periodo',)
    date_hierarchy = 'fecha_inicio'

@admin.register(AsignaturaExtra)
class AsignaturaExtraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'semestre')
    list_filter = ('semestre',)

@admin.register(CargaHoraria)
class CargaHorariaAdmin(admin.ModelAdmin):
    list_display = ('docente', 'plan_estudio', 'asignatura_extra', 'horas_asignadas')
    list_filter = ('plan_estudio',)

@admin.register(TablaTiempoLectivo)
class TablaTiempoLectivoAdmin(admin.ModelAdmin):
    pass

@admin.register(DistribucionTiempoLectivo)
class DistribucionTiempoLectivoAdmin(admin.ModelAdmin):
    pass
