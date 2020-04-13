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

]


