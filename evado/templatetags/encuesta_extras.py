from django import template
from django.shortcuts import get_object_or_404
from evado.models import RespuestaAplicarUniversoEncuestaPersona, AplicarUniversoEncuestaPersona

register = template.Library()


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def get_respuesta_directa(pregunta_id, aplicar_encuesta_id):
    aue = get_object_or_404(AplicarUniversoEncuestaPersona, pk=aplicar_encuesta_id)
    respuestas = aue.respuestaaplicaruniversoencuestapersona_set.filter(pregunta__id=pregunta_id)
    if respuestas.count() > 0:
        r = respuestas[0].respuesta_directa
        if r:
            return r
    return ""
