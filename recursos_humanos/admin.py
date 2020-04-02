from django.contrib import admin
from .models import Funcionario
from .models import Perfeccionamiento
from .models import Documentacion
from .models import FuncionarioUnion
from .models import FuncionarioFundacion
from .models import FuncionarioColegio
from .models import Vacacion
from .models import Licencia
from .models import Asistencia
from .models import ObservacionEntrevista
from .models import ObservadorAdjunto


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Perfeccionamiento)
class PerfeccionamientoAdmin(admin.ModelAdmin):
    pass

@admin.register(Documentacion)
class DocumentacionAdmin(admin.ModelAdmin):
    pass

@admin.register(FuncionarioUnion)
class FuncionarioUnionAdmin(admin.ModelAdmin):
    pass

@admin.register(FuncionarioFundacion)
class FuncionarioFundacionAdmin(admin.ModelAdmin):
    pass

@admin.register(FuncionarioColegio)
class FuncionarioColegioAdmin(admin.ModelAdmin):
    pass

@admin.register(Vacacion)
class VacacionAdmin(admin.ModelAdmin):
    pass

@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    pass

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    pass

@admin.register(ObservacionEntrevista)
class ObservacionEntrevistaAdmin(admin.ModelAdmin):
    pass

@admin.register(ObservadorAdjunto)
class ObservadorAdjuntoAdmin(admin.ModelAdmin):
    pass
