from django.conf import settings
from django.conf.urls import url
from rrhh import views

app_name = 'rrhh'

urlpatterns = [
    url(r'^$', views.home, name='home_rrhh'),
    url(r'^hyper_index/$', views.hyper_index, name='hyper_index'),
    url(
        r'^personas/$',
        views.PersonaListView.as_view(),
        name='personas'
    ),
    url(
        r'^personas/nuevo/$',
        views.PersonaCreateView.as_view(),
        name='persona__nuevo'
    ),
    url(
        r'^personas/(?P<pk_persona>\d+)/$',
        views.persona_detail,
        name='persona'
    ),
    url(
        r'^personas/(?P<pk>\d+)/editar/$',
        views.PersonaUpdateView.as_view(),
        name='persona__editar'
    ),
    url(
        r'^personas/(?P<pk>\d+)/eliminar/$',
        views.PersonaDeleteView.as_view(),
        name='persona__eliminar'
    ),
    # url(
    #     r'^funcionarios/$',
    #     views.FuncionarioListView.as_view(),
    #     name='funcionarios'
    # ),
    url(
        r'^funcionarios/(?P<id_persona>\d+)/nuevo/$',
        views.crear_funcionario,
        name='funcionario__nuevo'
    ),
    # url(
    #     r'^funcionarios/(?P<pk>\d+)/$',
    #     views.FuncionarioDetailView.as_view(),
    #     name='funcionario'
    # ),
    url(
        r'^funcionarios/(?P<pk>\d+)/editar/$',
        views.FuncionarioUpdateView.as_view(),
        name='funcionario__editar'
    ),
    # url(
    #     r'^funcionarios/(?P<pk>\d+)/eliminar/$',
    #     views.FuncionarioDeleteView.as_view(),
    #     name='funcionario__eliminar'
    # ),
    url(
        r'^postulantes/$',
        views.postulantes,
        name='postulantes'
    ),
    url(
        r'^entrevistas/$',
        views.EntrevistaListView.as_view(),
        name='entrevistas'
    ),
    url(
        r'^entrevistas/nuevo/$',
        views.EntrevistaCreateView.as_view(),
        name='entrevista__nuevo'
    ),
    url(
        r'^entrevistas/(?P<pk>\d+)/$',
        views.EntrevistaDetailView.as_view(),
        name='entrevista'
    ),
    url(
        r'^entrevistas/nuevo/$',
        views.EntrevistaCreateView.as_view(),
        name='entrevista__nuevo'
    ),
    url(
        r'^entrevistas/(?P<pk>\d+)/editar/$',
        views.EntrevistaUpdateView.as_view(),
        name='entrevista__editar'
    ),
    url(
        r'^entrevistas/(?P<pk>\d+)/eliminar/$',
        views.EntrevistaDeleteView.as_view(),
        name='entrevista__eliminar'
    ),
    url(
        r'^documentos/$',
        views.DocumentoListView.as_view(),
        name='documentos'
    ),
    url(
        r'^documentos/nuevo/$',
        views.DocumentoCreateView.as_view(),
        name='documento__nuevo'
    ),
    url(
        r'^documentos/(?P<pk>\d+)/$',
        views.DocumentoDetailView.as_view(),
        name='documento'
    ),
    url(
        r'^documentos/nuevo/$',
        views.DocumentoCreateView.as_view(),
        name='documento__nuevo'
    ),
    url(
        r'^documentos/(?P<pk>\d+)/editar/$',
        views.DocumentoUpdateView.as_view(),
        name='documento__editar'
    ),
    url(
        r'^documentos/(?P<pk>\d+)/eliminar/$',
        views.DocumentoDeleteView.as_view(),
        name='documento__eliminar'
    ),
    url(
        r'^vacaciones/$',
        views.VacacionListView.as_view(),
        name='vacaciones'
    ),
    url(
        r'^vacaciones/nuevo/$',
        views.VacacionCreateView.as_view(),
        name='vacacion__nuevo'
    ),
    url(
        r'^vacaciones/(?P<pk>\d+)/$',
        views.VacacionDetailView.as_view(),
        name='vacacion'
    ),
    url(
        r'^vacaciones/(?P<pk>\d+)/editar/$',
        views.VacacionUpdateView.as_view(),
        name='vacacion__editar'
    ),
    url(
        r'^vacaciones/(?P<pk>\d+)/eliminar/$',
        views.VacacionDeleteView.as_view(),
        name='vacacion__eliminar'
    ),
    url(
        r'^licencias/$',
        views.LicenciaListView.as_view(),
        name='licencias'
    ),
    url(
        r'^licencias/nuevo/$',
        views.LicenciaCreateView.as_view(),
        name='licencia__nuevo'
    ),
    url(
        r'^licencias/(?P<pk>\d+)/$',
        views.LicenciaDetailView.as_view(),
        name='licencia'
    ),
    url(
        r'^licencias/(?P<pk>\d+)/editar/$',
        views.LicenciaUpdateView.as_view(),
        name='licencia__editar'
    ),
    url(
        r'^licencias/(?P<pk>\d+)/eliminar/$',
        views.LicenciaDeleteView.as_view(),
        name='licencia__eliminar'
    ),
    url(
        r'^licencias_funcionario/nuevo/$',
        views.nuevo_licencia_tipo_funcionario,
        name='licencia_funcionario__nuevo'
    ),
    url(
        r'^permisos/$',
        views.PermisoListView.as_view(),
        name='permisos'
    ),
    url(
        r'^permisos/nuevo/$',
        views.PermisoCreateView.as_view(),
        name='permiso__nuevo'
    ),
    url(
        r'^permisos/(?P<pk>\d+)/$',
        views.PermisoDetailView.as_view(),
        name='permiso'
    ),
    url(
        r'^permisos/(?P<pk>\d+)/editar/$',
        views.PermisoUpdateView.as_view(),
        name='permiso__editar'
    ),
    url(
        r'^permisos/(?P<pk>\d+)/eliminar/$',
        views.PermisoDeleteView.as_view(),
        name='permiso__eliminar'
    ),
    url(
        r'^permisos_funcionario/nuevo/$',
        views.nuevo_permiso_tipo_funcionario,
        name='permiso_funcionario__nuevo'
    ),
    url(
        r'^vacaciones_funcionario/nuevo/$',
        views.nuevo_vacacion_funcionario,
        name='vacacion_funcionario__nuevo'
    ),
    url(
        r'^contratos/nuevo/(?P<id_funcionario>\d+)/(?P<id_solicitud>\d+)/',
        views.crear_contrato_colegio,
        name='contrato_colegio__crear'
    ),
    url(
        r'^contratos/$',
        views.ContratoListView.as_view(),
        name='contratos'
    ),
    url(
        r'^contratos/nuevo/$',
        views.ContratoCreateView.as_view(),
        name='contrato__nuevo'
    ),
    url(
        r'^contratos/(?P<pk>\d+)/$',
        views.ContratoDetailView.as_view(),
        name='contrato'
    ),
    url(
        r'^contratos/(?P<pk>\d+)/editar/$',
        views.ContratoUpdateView.as_view(),
        name='contrato__editar'
    ),
    url(
        r'^contratos/(?P<pk>\d+)/eliminar/$',
        views.ContratoDeleteView.as_view(),
        name='contrato__eliminar'
    ),
    url(
        r'^contratos/(?P<pk>\d+)/contrato/$',
        views.detalle_contrato_pdf,
        name='detalle-contrato-pdf'
    ),
    url(
        r'^contratos/(?P<pk>\d+)/diezmo/$',
        views.detalle_trabajador_diezmo_pdf,
        name='detalle-trabajador-diezmo-pdf'
    ),
    # url(
    #     r'^contratos/(?P<pk>\d+)/pdf/$',
    #     views.detalle_conocimiento_pdf,
    #     name='detalle-conocimiento-pdf'
    # ),
    url(
        r'^estado-contratacion/cambiar/$',
        views.cambiar_estado_contratacion,
        name='estado_contratacion__cambiar'
    ),
    url(
        r'^finiquito/(?P<id_contrato>\d+)/$',
        views.nuevo_finiquito,
        name='finiquito__nuevo'
    ),
    url(
        r'^finiquitos/(?P<pk>\d+)/eliminar/$',
        views.FiniquitoDeleteView.as_view(),
        name='finiquito__eliminar'
    ),
    url(
        r'^solicitudes/$',
        views.SolicitudListView.as_view(),
        name='solicitudes'
    ),
    url(
        r'^solicitudes/nuevo/$',
        views.SolicitudCreateView.as_view(),
        name='solicitud__nuevo'
    ),
    url(
        r'^solicitudes/(?P<pk>\d+)/$',
        views.SolicitudDetailView.as_view(),
        name='solicitud'
    ),
    url(
        r'^solicitudes/(?P<pk>\d+)/editar/$',
        views.SolicitudUpdateView.as_view(),
        name='solicitud__editar'
    ),
    url(
        r'^solicitudes/(?P<pk>\d+)/eliminar/$',
        views.SolicitudDeleteView.as_view(),
        name='solicitud__eliminar'
    ),
    url(
        r'^estado-solicitud/cambiar/$',
        views.cambiar_estado_solicitud,
        name='estado_solicitud__cambiar'
    ),
    url(
        r'^solicitudes/(?P<id_solicitud>\d+)/seleccionar_cadidatos/$',
        views.seleccionar_candidatos,
        name='candidatos__seleccionar'
    ),
    url(
        r'^solicitudes/guardar_candidato/$',
        views.guardar_candidato,
        name='candidatos__guardar'
    ),
    url(
        r'^contratos/(?P<id_contrato>\d+)/renovar/$',
        views.renovar_contrato,
        name='contrato__renovar'
    ),
    url(
        r'^funcionario/(?P<id_contrato>\d+)/trasladar/$',
        views.trasladar_funcionario,
        name='funcionario__trasladar'
    ),
    url(
        r'^funcionario/cargar_documento/$',
        views.cargar_documento_personal,
        name='personal__cargar_documento'
    ),

]

# add static
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
