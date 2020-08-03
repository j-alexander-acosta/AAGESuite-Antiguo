"""carga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'carga-horaria'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^switch/$', views.switch, name='switch'),
    url(r'^switch/(?P<pk>\d+)/$', views.switch, name='switch'),
    url(r'^clear/$', views.clear, name='clear'),
    url(
        r'^profesores/$',
        views.ProfesorListView.as_view(),
        name='profesores'
    ),
    url(
        r'^profesores/pdf/$',
        views.profesores_pdf,
        name='profesores-pdf'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/$',
        views.ProfesorDetailView.as_view(),
        name='profesor'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/anexo/$',
        views.anexo,
        name='profesor__anexo'
    ),
    url(
        r'^profesores/nuevo/$',
        views.ProfesorCreateView.as_view(),
        name='profesor__nuevo'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/editar/$',
        views.ProfesorUpdateView.as_view(),
        name='profesor__editar'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/eliminar/$',
        views.ProfesorDeleteView.as_view(),
        name='profesor__eliminar'
    ),
    # url(
    #     r'^cursos/$',
    #     views.CursoListView.as_view(),
    #     name='cursos'
    # ),
    # url(
    #     r'^cursos/(?P<pk>\d+)/$',
    #     views.CursoDetailView.as_view(),
    #     name='curso'
    # ),
    # url(
    #     r'^cursos/nuevo/$',
    #     views.CursoCreateView.as_view(),
    #     name='curso__nuevo'
    # ),
    # url(
    #     r'^cursos/(?P<pk>\d+)/editar/$',
    #     views.CursoUpdateView.as_view(),
    #     name='curso__editar'
    # ),
    # url(
    #     r'^cursos/(?P<pk>\d+)/eliminar/$',
    #     views.CursoDeleteView.as_view(),
    #     name='curso__eliminar'
    # ),
    url(
        r'^asistentes/$',
        views.AsistenteListView.as_view(),
        name='asistentes'
    ),
    url(
        r'^asistentes/pdf/$',
        views.asistentes_pdf,
        name='asistentes-pdf'
    ),
    url(
        r'^asistentes/(?P<pk>\d+)/$',
        views.AsistenteDetailView.as_view(),
        name='asistente'
    ),
    url(
        r'^asistentes/nuevo/$',
        views.AsistenteCreateView.as_view(),
        name='asistente__nuevo'
    ),
    url(
        r'^asistentes/(?P<pk>\d+)/editar/$',
        views.AsistenteUpdateView.as_view(),
        name='asistente__editar'
    ),
    url(
        r'^asistentes/(?P<pk>\d+)/eliminar/$',
        views.AsistenteDeleteView.as_view(),
        name='asistente__eliminar'
    ),
    url(
        r'^asignaturasbase/$',
        views.AsignaturaBaseListView.as_view(),
        name='asignaturasbase'
    ),
    url(
        r'^asignaturasbase/(?P<pk>\d+)/$',
        views.AsignaturaBaseDetailView.as_view(),
        name='asignaturabase'
    ),
    url(
        r'^asignaturasbase/nuevo/$',
        views.AsignaturaBaseCreateView.as_view(),
        name='asignaturabase__nuevo'
    ),
    url(
        r'^asignaturasbase/(?P<pk>\d+)/editar/$',
        views.AsignaturaBaseUpdateView.as_view(),
        name='asignaturabase__editar'
    ),
    url(
        r'^asignaturasbase/(?P<pk>\d+)/eliminar/$',
        views.AsignaturaBaseDeleteView.as_view(),
        name='asignaturabase__eliminar'
    ),
    url(
        r'^asignaturas/$',
        views.AsignaturaListView.as_view(),
        name='asignaturas'
    ),
    url(
        r'^asignaturas/(?P<pk>\d+)/$',
        views.AsignaturaDetailView.as_view(),
        name='asignatura'
    ),
    url(
        r'^periodos/(?P<pk>\d+)/nueva-asignatura/$',
        views.AsignaturaCreateView.as_view(),
        name='asignatura__nuevo'
    ),
    url(
        r'^asignaturas/(?P<pk>\d+)/editar/$',
        views.AsignaturaUpdateView.as_view(),
        name='asignatura__editar'
    ),
    url(
        r'^asignaturas/(?P<pk>\d+)/eliminar/$',
        views.AsignaturaDeleteView.as_view(),
        name='asignatura__eliminar'
    ),

    url(
        r'^periodos/$',
        views.PeriodoListView.as_view(),
        name='periodos'
    ),
    url(
        r'^periodos/(?P<pk>\d+)/$',
        views.PeriodoDetailView.as_view(),
        name='periodo'
    ),
    url(
        r'^periodos/(?P<pk>\d+)/pdf/$',
        views.periodo_pdf,
        name='periodo-pdf'
    ),
    url(
        r'^periodos/nuevo/$',
        views.PeriodoCreateView.as_view(),
        name='periodo__nuevo'
    ),
    url(
        r'^periodos/(?P<pk>\d+)/editar/$',
        views.PeriodoUpdateView.as_view(),
        name='periodo__editar'
    ),
    url(
        r'^periodos/(?P<pk>\d+)/eliminar/$',
        views.PeriodoDeleteView.as_view(),
        name='periodo__eliminar'
    ),

    url(
        r'^colegios/$',
        views.ColegioListView.as_view(),
        name='colegios'
    ),
    url(
        r'^colegios/(?P<pk>\d+)/$',
        views.ColegioDetailView.as_view(),
        name='colegio'
    ),
    url(
        r'^colegios/nuevo/$',
        views.ColegioCreateView.as_view(),
        name='colegio__nuevo'
    ),
    url(
        r'^colegios/(?P<pk>\d+)/editar/$',
        views.ColegioUpdateView.as_view(),
        name='colegio__editar'
    ),
    url(
        r'^colegios/(?P<pk>\d+)/eliminar/$',
        views.ColegioDeleteView.as_view(),
        name='colegio__eliminar'
    ),
    url(
        r'^planes/$',
        views.PlanListView.as_view(),
        name='planes'
    ),
    url(
        r'^planes/(?P<pk>\d+)/$',
        views.PlanDetailView.as_view(),
        name='plan'
    ),
    url(
        r'^planes/nuevo/$',
        views.PlanCreateView.as_view(),
        name='plan__nuevo'
    ),
    url(
        r'^planes/(?P<pk>\d+)/editar/$',
        views.PlanUpdateView.as_view(),
        name='plan__editar'
    ),
    url(
        r'^planes/(?P<pk>\d+)/eliminar/$',
        views.PlanDeleteView.as_view(),
        name='plan__eliminar'
    ),
    url(
        r'^asignaturas/(?P<pk>\d+)/asignar/$',
        views.asignar,
        name='asignar'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/fua/(?P<tipo>\d+)/$',
        views.asignar_fua,
        name='asignar-fua'
    ),
    url(
        r'^asignaciones/(?P<pk>\d+)/editar/$',
        views.AsignacionUpdateView.as_view(),
        name='asignacion__editar'
    ),
    url(
        r'^asignaciones/(?P<pk>\d+)/eliminar/$',
        views.AsignacionDeleteView.as_view(),
        name='asignacion__eliminar'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/asignar-extra/$',
        views.asignar_extra,
        name='asignar-extra'
    ),
    url(
        r'^profesores/(?P<profesor_pk>\d+)/asignaciones-extra/(?P<pk>\d+)/editar/$',
        views.AsignacionExtraUpdateView.as_view(),
        name='asignacion-extra__editar'
    ),
    url(
        r'^asignaciones-extra/(?P<pk>\d+)/eliminar/$',
        views.AsignacionExtraDeleteView.as_view(),
        name='asignacion-extra__eliminar'
    ),
    url(
        r'^profesores/(?P<pk>\d+)/asignar-no-aula/$',
        views.asignar_no_aula,
        name='asignar-no-aula'
    ),
    url(
        r'^profesores/(?P<profesor_pk>\d+)/asignaciones-no-aula/(?P<pk>\d+)/editar/$',
        views.AsignacionNoAulaUpdateView.as_view(),
        name='asignacion-no-aula__editar'
    ),
    url(
        r'^asignaciones-no-aula/(?P<pk>\d+)/eliminar/$',
        views.AsignacionNoAulaDeleteView.as_view(),
        name='asignacion-no-aula__eliminar'
    ),
    url(
        r'^planes/plantila/$',
        views.crear_desde_plantilla,
        name='plan__plantilla'
    ),
]
