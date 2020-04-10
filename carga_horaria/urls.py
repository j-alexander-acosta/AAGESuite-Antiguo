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


]


