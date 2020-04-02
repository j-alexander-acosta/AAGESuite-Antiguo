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
    pass

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    pass

@admin.register(PlanEstudio)
class PlanEstudioAdmin(admin.ModelAdmin):
    pass

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    pass

@admin.register(AsignaturaExtra)
class AsignaturaExtraAdmin(admin.ModelAdmin):
    pass

@admin.register(CargaHoraria)
class CargaHorariaAdmin(admin.ModelAdmin):
    pass

@admin.register(TablaTiempoLectivo)
class TablaTiempoLectivoAdmin(admin.ModelAdmin):
    pass

@admin.register(DistribucionTiempoLectivo)
class DistribucionTiempoLectivoAdmin(admin.ModelAdmin):
    pass
