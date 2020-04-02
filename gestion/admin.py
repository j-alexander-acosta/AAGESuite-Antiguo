from django.contrib import admin
from .models import Union
from .models import Fundacion
from .models import Colegio
from .models import ExcelenciaAcademica
from .models import Periodo

@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    pass

@admin.register(Fundacion)
class FundacionAdmin(admin.ModelAdmin):
    pass

@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    pass

@admin.register(ExcelenciaAcademica)
class ExcelenciaAcademicaAdmin(admin.ModelAdmin):
    pass

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    pass
