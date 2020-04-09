from django.contrib import admin
from .models import Plan
from .models import AsignaturaBase
from .models import Colegio
from .models import Periodo
from .models import Asignatura
from .models import Curso
from .models import Profesor
from .models import Asignacion


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass

@admin.register(AsignaturaBase)
class AsignaturaBaseAdmin(admin.ModelAdmin):
    pass

@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    pass

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_filter = ['nombre', 'colegio', 'plan']
    list_display = (
        'nombre',
        'colegio',
        'plan',
#        'creado_en',
#        'modificado_en'
    )

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    pass

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    pass

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    pass

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    pass
