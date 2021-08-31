from django.conf import settings
from django.conf.urls import url
from evado import views

app_name = 'evado'

urlpatterns = [
    url(r'^$', views.home, name='home_evado'),
    # Periodos
    url(r'^periodos/$', views.PeriodoEncuestaListView.as_view(), name='periodo_list'),
    url(r'^periodos/nuevo/$', views.PeriodoEncuestaCreateView.as_view(), name='periodo_create'),
    url(r'^periodos/<pk>/detalle/$', views.PeriodoEncuestaDetailView.as_view(), name='periodo_detail'),
    url(r'^periodos/<pk>/actualizar/$', views.PeriodoEncuestaUpdateView.as_view(), name='periodo_update'),
    # Encuestas
    url(r'^encuestas/$', views.EncuestaListView.as_view(), name='encuesta_list'),
    url(r'^encuesta/<pk>/detalle/$', views.EncuestaDetailView.as_view(), name='encuesta_detail'),
    url(r'^encuesta/nueva/$', views.EncuestaCreateView.as_view(), name='encuesta_create'),
    url(r'^encuesta/<str:hash>/$', views.tomar_encuesta, name='tomar_encuesta'),
    url(r'^encuesta/<str:hash>/finalizada/$', views.encuesta_finalizada, name='encuesta_finalizada'),
    url(r'^encuesta/<str:hash>/cerrada/$', views.encuesta_cerrada, name='encuesta_cerrada'),
    url(r'^encuesta/<id_persona>/enviar/<id_universo>/$', views.enviar_encuesta, name='enviar_encuesta'),
    url(r'^encuesta/enviar/<id_universo>/correos/$', views.enviar_todas_encuestas, name='enviar_todas_encuestas'),
    # Universo Correos
    url(r'^encuesta/correos/$', views.CorreoUniversoEncuestaListView.as_view(), name='correo_universo_list'),
    url(r'^encuesta/correo/<pk>/detalle/$', views.CorreoUniversoEncuestaDetailView.as_view(), name='correo_universo_detail'),
    url(r'^encuesta/correo/nuevo/$', views.CorreoUniversoEncuestaCreateView.as_view(), name='correo_universo_create'),
    url(r'^encuesta/correo/<pk>/actualizar/$', views.CorreoUniversoEncuestaUpdateView.as_view(), name='correo_universo_update'),
    # Categorias
    url(r'^encuestas/preguntas/categorias/$', views.CategoriaPreguntaListView.as_view(), name='categoria_pregunta_list'),
    url(r'^encuestas/preguntas/categoria/<pk>/$', views.CategoriaPreguntaDetailView.as_view(), name='categoria_pregunta_detail'),
    url(r'^encuestas/preguntas/categoria/<pk>/actualizar/$', views.CategoriaPreguntaUpdateView.as_view(), name='categoria_pregunta_update'),
    url(r'^encuestas/preguntas/categoria/nueva/$', views.CategoriaPreguntaCreateView.as_view(), name='categoria_pregunta_create'),
    # Preguntas
    url(r'^encuestas/preguntas/$', views.PreguntaEncuestaListView.as_view(), name='pregunta_encuesta_list'),
    url(r'^encuestas/pregunta/<pk>/$', views.PreguntaEncuestaListView.as_view(), name='pregunta_encuesta_detail'),
    # Universo Encuestas
    url(r'^universoencuestas/$', views.UniverEncuestaListView.as_view(), name='universo_encuesta_list'),
    url(r'^universoencuesta/<pk>/detalle/$', views.UniversoEncuestaDetailView.as_view(), name='universo_encuesta_detail'),
    url(r'^universoencuesta/nuevo/$', views.UniversoEncuestaCreateView.as_view(), name='universo_encuesta_create'),
    url(r'^universoencuesta/mail/universosencuestas/$', views.enviar_mail_universo_encuestas, name='enviar_mail_universo_encuestas'),
    url(r'^encuesta/<pk>/editar/$', views.EncuestaPreguntaFormSetView.as_view(), name='encuesta_preguntas_edit'),
    url(r'^encuesta/<pk>/pregunta/anadir/$', views.encuesta_crear_pregunta, name='encuesta_crear_pregunta'),
    url(r'^encuesta/<pk_pregunta>/pregunta/eliminar/$', views.encuesta_eliminar_pregunta, name='encuesta_eliminar_pregunta'),
    url(r'^universoencuesta/<id_universo>/actualizar/personas/$', views.actualizar_encuestas_universo, name='actualizar_encuestas_universo'),
    # Correos para enviar
    url(r'^encuesta/correos/<id_universo_correo>/enviar/$', views.enviar_recordar_contestar_encuestas, name='enviar_recordar_contestar_encuestas'),
    # Configurar Unierso Encuestas
    url(r'^encuesta/configurar/universo/$', views.configurar_universo_personas, name='configurar_universo_personas'),
    url(r'^encuesta/configurar/<pk>/eliminar/$', views.eliminar_configurar_universo_personas, name='eliminar_configurar_universo_personas'),
    # url(r'^encuesta/configurar/universo/persona_upload/$', persona_upload, name='persona_upload'),
    url(r'^encuesta/configurar/universo/export/excel/$', views.export_eup_xls, name='export_eup_xls'),
    url(r'^encuesta/configurar/universo/import/excel/$', views.import_eup_xls, name='persona_upload'),
    url(r'^encuesta/configurar/universo/delete/$', views.eliminar_todos_eup, name='eliminar_todos_eup'),
]

# add static
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)