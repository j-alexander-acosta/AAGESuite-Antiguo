# coding: utf-8
from __future__ import unicode_literals
import hashlib
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from random import getrandbits
from rrhh.models import Persona


def generate_hash():
    hash = "%032x"
    return hashlib.sha512(hash.encode('utf-8') % getrandbits(160)).hexdigest()


class ConfigurarEncuestaUniversoPersona(models.Model):
    persona = models.ForeignKey(Persona, related_name="persona", on_delete=models.CASCADE, verbose_name='Evaluador')
    evaluados = models.ManyToManyField(Persona, related_name="evaluados")
    periodo = models.ForeignKey('PeriodoEncuesta', on_delete=models.CASCADE, null=True)
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} ({})'.format(
            self.persona,
            self.tipo_encuesta,
            self.periodo
        )


class Encuesta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name="Descripción")
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('encuesta_detail', kwargs={'pk': self.pk})

    @property
    def obtener_preguntas_no_respuesta_directa(self):
        return self.preguntaencuesta_set.filter(es_respuesta_directa=False).order_by('categoria', 'numero_pregunta')

    @property
    def obtener_preguntas_respuesta_directa(self):
        return self.preguntaencuesta_set.filter(es_respuesta_directa=True)

    def __str__(self):
        return '{}'.format(
            self.titulo,
        )


class CategoriaPregunta(models.Model):
    nombre = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('categoria_pregunta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(
            self.nombre,
        )


class TipoDescripcionItemPregunta(models.Model):
    nombre = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(
            self.nombre,
        )


class DescripcionItemPregunta(models.Model):
    descripcion = models.TextField(verbose_name="Descripción")
    tipo_descripcion = models.ForeignKey('TipoDescripcionItemPregunta', on_delete=models.CASCADE,
                                         verbose_name="Tipo de descripción")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(
            self.descripcion,
        )


class PreguntaEncuesta(models.Model):
    encuesta = models.ForeignKey("Encuesta", on_delete=models.CASCADE)
    categoria = models.ForeignKey("CategoriaPregunta", on_delete=models.CASCADE)
    pregunta = models.TextField()
    es_respuesta_directa = models.BooleanField(default=False)
    no_mostrar_pregunta = models.BooleanField(default=False)
    requerida = models.BooleanField(default=True, verbose_name="Es requerida")
    tipo_respuesta = models.ForeignKey(
        "TipoRespuesta",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Tipo de respuesta"
    )
    descripcion_item_pregunta = models.ForeignKey(
        "TipoDescripcionItemPregunta", null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name="Descripción de ítem de pregunta"
    )
    numero_pregunta = models.PositiveIntegerField(verbose_name="Número de pregunta")
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('pregunta_encuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}. {} ({})'.format(
            self.numero_pregunta,
            self.pregunta,
            self.encuesta.titulo
        )


class TipoRespuesta(models.Model):
    nombre = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('tipo_respuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(
            self.nombre,
        )


class Respuesta(models.Model):
    respuesta = models.CharField(max_length=255)
    columna = models.PositiveIntegerField(default=1)
    peso = models.IntegerField(default=0)
    escrita = models.BooleanField(default=False, verbose_name="Es escrita")
    check = models.BooleanField(default=False, verbose_name="Es seleccionable")
    tipo_respuesta = models.ForeignKey('TipoRespuesta', on_delete=models.CASCADE, verbose_name="Tipo de respuesta")

    def get_absolute_url(self):
        return reverse('respuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(
            self.respuesta,
        )


class PeriodoEncuesta(models.Model):
    nombre = models.CharField(max_length=20)
    activo = models.BooleanField(default=False)

    def clean(self, *args, **kwargs):
        if self.activo and PeriodoEncuesta.objects.filter(activo=True).count() > 0:
            raise ValidationError('Ya existe un periodo activo.')
        super(PeriodoEncuesta, self).clean(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('periodo_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(
            self.nombre
        )


class TipoUniversoEncuesta(models.Model):
    CODIGO_NORMAL = "EN0000"
    CODIGO_DOCENTE = "EN0001"
    CODIGO_PERSONALIZADA = "EN0002"
    CODIGO_SUPERIOR = "EN0003"
    CODIGO_DOCENTE_CURSOS = "EN004"

    CODIGO_CHOICES = (
        (CODIGO_NORMAL, "Evaluación Normal"),
        (CODIGO_DOCENTE, "Evaluación Docente"),
        (CODIGO_PERSONALIZADA, "Evaluación Personalizada"),
        (CODIGO_SUPERIOR, "Evaluación desde Superiores"),
        (CODIGO_DOCENTE_CURSOS, "Evaluación Docente de sus cursos")
    )

    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10, unique=True, choices=CODIGO_CHOICES, verbose_name="Código")

    def __str__(self):
        return self.nombre


class UniversoEncuesta(models.Model):
    encuesta = models.ForeignKey("Encuesta", on_delete=models.CASCADE)
    config_universo_persona = models.ManyToManyField("ConfigurarEncuestaUniversoPersona", verbose_name='Evaluadores')
    contenido_email = models.TextField(verbose_name="Contenido del correo electrónico")
    inicio = models.DateField()
    fin = models.DateField()
    tipo_encuesta = models.ForeignKey('TipoUniversoEncuesta', on_delete=models.CASCADE, verbose_name="Tipo de encuesta")
    activar_campo_comentario = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    correos_enviados = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de envío de correos")
    creado = models.BooleanField(default=False)

    class Meta:
        ordering = ['creado_en']

    def generar_encuestas_del_universo(self):
        if not self.creado:
            self.generar_encuestas_segun_tipo(self)
            self.creado = True
            self.save()

    def generar_encuestas_segun_tipo(self, cursos_formulario=None):
        """
        <aues> tipo:list. Objetos AplicarUniversoEncuestaPersona.
        """
        aues = ''
        if self.config_universo_persona.tipo_encuesta.codigo == TipoUniversoEncuesta.CODIGO_NORMAL:
            aues = self.aplicar_encuesta_tipo_normal()

        elif self.config_universo_persona.tipo_encuesta.codigo == TipoUniversoEncuesta.CODIGO_PERSONALIZADA:
            aues = self.aplicar_encuesta_tipo_personalizada()

        self.generar_preguntas_para_aues(aues)

    def generar_preguntas_para_aues(self, aues):
        preguntas = self.encuesta.preguntaencuesta_set.all()
        for aue in aues:
            lista_respuestas = []
            for p in preguntas:
                if p.requerida:
                    lista_respuestas.append(
                        RespuestaAplicarUniversoEncuestaPersona(aplicar_universo_encuesta_persona=aue, pregunta=p))
            RespuestaAplicarUniversoEncuestaPersona.objects.bulk_create(lista_respuestas)

    def aplicar_encuesta_tipo_normal(self):
        # preguntas = self.encuesta.preguntaencuesta_set.all()
        aues = []
        for x in self.config_universo_persona.evaluados.all():
            aue, created = AplicarUniversoEncuestaPersona.objects.get_or_create(universo_encuesta=self, persona=x)
            if created:
                aues.append(aue)
        return aues

    def aplicar_encuesta_tipo_personalizada(self):
        # preguntas = self.encuesta.preguntaencuesta_set.all()
        aues = []
        for x in self.config_universo_persona.evaluados.all():
            query = ConfigurarEncuestaUniversoPersona.objects.filter(persona=x)
            for y in query:
                aue, created = AplicarUniversoEncuestaPersona.objects.get_or_create(universo_encuesta=self, persona=x,
                                                                                    config_universo_persona=y)
                if created:
                    aues.append(aue)
        return aues

    @property
    def itemes_personas(self):
        return self.personauniversoencuesta_set.all()

    def get_absolute_url(self):
        return reverse('universo_encuesta_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} ({})'.format(
            self.encuesta.titulo,
            self.inicio
        )


class PersonaUniversoEncuesta(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    universo_encuesta = models.ForeignKey("UniversoEncuesta", on_delete=models.CASCADE,
                                          verbose_name="Universo de encuestas")
    correo_enviado = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de envío de correo")
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def mail_enviado(self):
        if self.correo_enviado:
            return True
        else:
            return False

    def __str__(self):
        return '{}'.format(
            self.persona
        )


class AplicarUniversoEncuestaPersona(models.Model):
    universo_encuesta = models.ForeignKey('UniversoEncuesta', on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    encuestado = models.CharField(max_length=255, null=True, blank=True)
    hash = models.CharField('hash', max_length=128, default=generate_hash, unique=True, null=True)
    comentario = models.TextField(null=True, blank=True)
    finalizado = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def total_respuestas(self):
        return sum(map(lambda x: x.respuesta.peso,
                       self.respuestaaplicaruniversoencuestapersona_set.filter(pregunta__es_respuesta_directa=False,
                                                                               respuesta__isnull=False)))

    @property
    def respuestas_contestadas(self):
        return self.respuestaaplicaruniversoencuestapersona_set.exclude(respuesta=None)

    @property
    def respuestas_finalizado(self):
        return self.respuestaaplicaruniversoencuestapersona_set.filter(respuesta__isnull=False).filter(
            respuesta__check=False, respuesta__escrita=False)

    @property
    def nombre(self):
        code = self.universo_encuesta.tipo_encuesta.codigo
        name = ""
        if code == TipoUniversoEncuesta.CODIGO_NORMAL:
            name = u"%s" % self.universo_encuesta.encuesta.titulo
        elif code == TipoUniversoEncuesta.CODIGO_PERSONALIZADA:
            name = u""
        return name

    def get_absolute_url(self):
        return reverse('aplicar_universo_encuesta_persona_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} - {} > {}'.format(
            self.persona,
            self.universo_encuesta,
            self.universo_encuesta.tipo_encuesta
        )


class RespuestaAplicarUniversoEncuestaPersona(models.Model):
    aplicar_universo_encuesta_persona = models.ForeignKey('AplicarUniversoEncuestaPersona', on_delete=models.CASCADE)
    pregunta = models.ForeignKey('PreguntaEncuesta', on_delete=models.CASCADE)
    respuesta = models.ForeignKey('Respuesta', on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_directa = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('respuesta_aplicar_universo_encuesta_persona_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = u"Respuesta a Encuesta"
        verbose_name_plural = u"Respuestas a Encuestas"


class CorreoUniversoEncuesta(models.Model):
    encabezado = models.CharField(max_length=255)
    correo = models.TextField()
    universo_encuesta = models.ForeignKey('UniversoEncuesta', on_delete=models.CASCADE)
    enviado = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"Correo Universo Encuesta"
        verbose_name_plural = u"Correos de universos de encuestas"

    def __str__(self):
        return '{} - {}'.format(
            self.encabezado,
            self.universo_encuesta
        )

    def get_absolute_url(self):
        return reverse('correo_universo_detail', kwargs={'pk': self.pk})
