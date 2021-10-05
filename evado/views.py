# -*- coding: utf-8 -*-
import csv
import datetime
import io
import pandas as pd
import traceback
import xlwt
from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from extra_views import InlineFormSetView
from jsonview.decorators import json_view

from django.conf import settings
from evado.mixins import LoginRequired, SearchableListMixin
from evado.forms import *
from evado.models import *


@login_required
def home(request):
    context = {}
    now = timezone.now().date()
    two_days_before = now - datetime.timedelta(days=2)
    encuestas_habilitadas = UniversoEncuesta.objects.filter(fin__gte=now)
    context['encuestas_habilitadas'] = encuestas_habilitadas

    auep = AplicarUniversoEncuestaPersona.objects.all()
    context['encuestas_rendidas'] = auep.filter(finalizado__gte=two_days_before).order_by('-finalizado') if auep.exists() else None

    encuestas_finalizadas = []
    total_encuestas_finalizadas = 0
    for encuesta in encuestas_habilitadas:
        aueps = encuesta.aplicaruniversoencuestapersona_set.all().exclude(finalizado__isnull=True)
        total_encuestas_finalizadas += aueps.distinct('persona').count()
        for enc in aueps:
            encuestas_finalizadas.append(enc)
    context['encuestas_finalizadas'] = encuestas_finalizadas
    context['total_encuestas_finalizadas'] = total_encuestas_finalizadas
    return render(request, 'encuesta/home.html', context)


class EncuestaListView(LoginRequired, ListView):
    model = Encuesta
    template_name = 'encuesta/encuesta_list.html'
    search_fields = [('titulo', 'icontains',)]
    paginate_by = 10


class EncuestaCreateView(LoginRequired, CreateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuesta/encuesta_create.html'


class EncuestaPreguntaFormSetView(LoginRequired, SearchableListMixin, InlineFormSetView):
    model = Encuesta
    extra = 1
    inline_model = PreguntaEncuesta
    form_class = PreguntaEncuestaItemForm
    template_name = 'encuesta/encuesta_pregunta_inline_formset.html'


class EncuestaDetailView(LoginRequired, DetailView):
    model = Encuesta
    template_name = 'encuesta/encuesta_detail.html'
    search_fields = [('titulo', 'icontains',)]

    def get_context_data(self, **kwargs):
        context = super(EncuestaDetailView, self).get_context_data(**kwargs)
        context['form_pregunta'] = PreguntaEncuestaForm()
        context['aplicar_encuestas'] = AplicarUniversoEncuestaPersona.objects.filter(universo_encuesta__encuesta=self.object).order_by('-finalizado')
        return context


@login_required
@json_view
def encuesta_crear_pregunta(request, pk):
    encuesta = get_object_or_404(Encuesta, id=pk)
    form = PreguntaEncuestaForm(request.POST or None)
    if form.is_valid():
        categoria = form.cleaned_data.get('categoria', None)
        pregunta = form.cleaned_data.get('pregunta', None)
        tipo_respuesta = form.cleaned_data.get('tipo_respuesta', None)
        PreguntaEncuesta.objects.create(encuesta=encuesta, categoria=categoria, pregunta=pregunta,
                                        tipo_respuesta=tipo_respuesta)
        return {'success': True}
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@login_required
def encuesta_eliminar_pregunta(request, pk_pregunta):
    pe = get_object_or_404(PreguntaEncuesta, id=pk_pregunta)
    id_encuesta = pe.encuesta.id
    pe.delete()
    return redirect('encuesta_detail', id_encuesta)


class CategoriaPreguntaListView(LoginRequired, SearchableListMixin, ListView):
    model = CategoriaPregunta
    template_name = 'encuesta/categoria_pregunta_list.html'
    search_fields = [('nombre', 'icontains',)]


class CategoriaPreguntaDetailView(LoginRequired, SearchableListMixin, DetailView):
    model = CategoriaPregunta
    template_name = 'encuesta/categoria_pregunta_detail.html'
    search_fields = [('nombre', 'icontains',)]


class CategoriaPreguntaCreateView(LoginRequired, SearchableListMixin, CreateView):
    model = CategoriaPregunta
    template_name = 'encuesta/categoria_pregunta_create.html'
    search_fields = [('nombre', 'icontains',)]


class CategoriaPreguntaUpdateView(LoginRequired, SearchableListMixin, UpdateView):
    model = CategoriaPregunta
    template_name = 'encuesta/categoria_pregunta_update.html'
    search_fields = [('nombre', 'icontains',)]


class PreguntaEncuestaListView(LoginRequired, SearchableListMixin, ListView):
    model = PreguntaEncuesta
    template_name = 'encuesta/pregunta_encuesta_list.html'
    search_fields = [('pregunta', 'icontains',)]


class TipoUniversoEncuestaListView(LoginRequired, ListView):
    model = TipoUniversoEncuesta
    template_name = 'encuesta/tipo_universo_encuesta/tipo_universo_encuesta_list.html'
    search_fields = ['nombre']
    paginate_by = 10


class TipoUniversoEncuestaDetailView(LoginRequired, DetailView):
    model = TipoUniversoEncuesta
    template_name = 'encuesta/tipo_universo_encuesta/tipo_universo_encuesta_detail.html'


class TipoUniversoEncuestaCreateView(LoginRequired, CreateView):
    model = TipoUniversoEncuesta
    form_class = TipoUniversoEncuestaForm
    template_name = 'encuesta/tipo_universo_encuesta/tipo_universo_encuesta_create.html'
    success_url = reverse_lazy('evado:tipo_universo_encuesta_list')

    # def get_success_url(self):
    #     return reverse_lazy(
    #         'evado:tipo_universo_encuesta_detail',
    #         kwargs={
    #             'pk': self.object.pk,
    #         }
    #     )


class TipoUniversoEncuestaUpdateView(LoginRequired, UpdateView):
    model = TipoUniversoEncuesta
    form_class = TipoUniversoEncuestaForm
    template_name = 'encuesta/tipo_universo_encuesta/tipo_universo_encuesta_create.html'
    success_url = reverse_lazy('evado:tipo_universo_encuesta_list')

    # def get_success_url(self):
    #     return reverse_lazy(
    #         'evado:tipo_universo_encuesta_detail',
    #         kwargs={
    #             'pk': self.object.pk,
    #         }
    #     )


class TipoUniversoEncuestaDeleteView(LoginRequired, DeleteView):
    model = TipoUniversoEncuesta
    success_url = reverse_lazy('evado:tipo_universo_encuesta_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UniversoEncuestaListView(LoginRequired, ListView):
    model = UniversoEncuesta
    template_name = 'encuesta/universo_encuesta_list.html'
    search_fields = [('encuesta__titulo', 'icontains')]
    paginate_by = 10


class UniversoEncuestaDetailView(LoginRequired, DetailView):
    model = UniversoEncuesta
    template_name = 'encuesta/universo_encuesta_detail.html'
    search_fields = [('encuesta_titulo', 'icontains')]

    def get_context_data(self, **kwargs):
        context = super(UniversoEncuestaDetailView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        filtro = False
        personas = self.get_object().itemes_personas
        if search:
            params = [x.strip() for x in search.split(',')]
            if len(params) == 3:
                personas = personas.filter(persona__nombres__icontains=params[0],
                                           persona__apellidos__icontains=params[1],
                                           persona__rut__icontains=params[2])
            elif len(params) == 2:
                personas = personas.filter(persona__nombres__icontains=params[0],
                                           persona__apellidos__icontains=params[1])
            elif len(params) == 1:
                personas = personas.filter(persona__rut__icontains=params[0])
            else:
                pass
            filtro = True
        paginator = Paginator(personas, 30)
        page = self.request.GET.get('page')
        try:
            personas = paginator.page(page)
        except PageNotAnInteger:
            personas = paginator.page(1)
        except EmptyPage:
            personas = paginator.page(paginator.num_pages)
        context['personas'] = personas
        context['filtro'] = filtro
        return context


@login_required
def actualizar_encuestas_universo(request, id_universo):
    universo = get_object_or_404(UniversoEncuesta, id=id_universo)
    # Generando encuestas para el universo
    universo.generar_encuestas_del_universo()
    messages.add_message(request, messages.INFO, 'Universo Actualizado')
    return redirect('universo_encuesta_detail', universo.id)


class UniversoEncuestaCreateView(LoginRequired, CreateView):
    model = UniversoEncuesta
    form_class = UniversoEncuestaForm
    template_name = 'encuesta/universo_encuesta_create.html'
    search_fields = [('encuesta_titulo', 'icontains')]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        for config_universo in form.cleaned_data['config_universo_persona']:
            self.object.config_universo_persona.add(config_universo)
            pue = PersonaUniversoEncuesta()
            pue.universo_encuesta = self.object
            pue.persona = config_universo.persona
            pue.save()

        # Generando encuestas para el universo
        self.object.generar_encuestas_del_universo()
        return super(ModelFormMixin, self).form_valid(form)


def guardar_respuestas(request, encuesta_aplicada, dic):
    """
        Esta función, se encarga de guardar las respuestas de la encuesta
    :return:
    """
    guardada = True
    try:
        # RespuestaAplicarUniversoEncuestaPersona.objects.filter(
        #     aplicar_universo_encuesta_persona=encuesta_aplicada,
        #     respuesta__isnull=False
        # ).filter(
        #     respuesta__check=True
        # ).delete()
        for k, v in dic.items():
            if "check_{}".format(encuesta_aplicada.id) in k:  # check
                id_pregunta = int(str(k).split('_')[2])
                ids_respuesta = map(lambda x: int(x), v)
                for x in ids_respuesta:
                    respuesta = Respuesta.objects.get(id=x)
                    res = RespuestaAplicarUniversoEncuestaPersona.objects.get(
                        aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta)
                    if not res.respuesta or respuesta != res.respuesta:
                        res.respuesta = respuesta
                        res.save()
            if "escrita_{}".format(encuesta_aplicada.id) in k:
                id_pregunta = int(str(k).split('_')[2])
                id_respuesta = int(str(k).split('_')[3])
                respuesta = Respuesta.objects.get(id=id_respuesta)
                escrita = v[0]
                lis_respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                    aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta,
                    respuesta__isnull=False).filter(respuesta__escrita=True)
                if lis_respuestas.exists():
                    ready = False
                    for x in lis_respuestas.exclude(respuesta__isnull=True):
                        if x.respuesta.columna == respuesta.columna:
                            x.respuesta_directa = escrita
                            x.save()
                            ready = True
                    if not ready:
                        obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                            aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta,
                            respuesta=respuesta, respuesta_directa=escrita)
                else:
                    obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                        aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta,
                        respuesta=respuesta, respuesta_directa=escrita)
            if "respuesta_{}".format(encuesta_aplicada.id) in k:
                id_pregunta = int(str(k).split('_')[2])
                id_respuesta = int(v[0])
                respuesta = Respuesta.objects.get(id=id_respuesta)
                listado_respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                    aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta,
                    pregunta__es_respuesta_directa=False)
                if listado_respuestas.exists():
                    if listado_respuestas.count() > 1:
                        ready = False
                        for r in listado_respuestas:
                            if r.respuesta:
                                if not r.respuesta.check and not r.respuesta.escrita:
                                    r.respuesta = respuesta
                                    r.save()
                                    ready = True
                            else:
                                r.respuesta = respuesta
                                r.save()
                                ready = True
                        if not ready:
                            obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=encuesta_aplicada,
                                pregunta_id=id_pregunta, respuesta=respuesta)
                    else:
                        obj = listado_respuestas[0]
                        obj.respuesta = respuesta
                        obj.save()
                else:
                    obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                        aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta,
                        respuesta=respuesta)
            if "preguntadirecta_{}".format(encuesta_aplicada.id) in k:
                id_pregunta = int(str(k).split('_')[2])
                res, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                    aplicar_universo_encuesta_persona=encuesta_aplicada, pregunta_id=id_pregunta,
                    pregunta__es_respuesta_directa=True)
                res.respuesta_directa = v[0]
                res.save()
    except:
        traceback.print_exc()
        guardada = False

    return guardada


def redirect_url_tomar_encuesta(hash, page):
    # base_url = reverse('evado:tomar_encuesta', kwargs={"hash": hash})  # 1 /products/
    base_url = reverse('evado:tomar_encuesta', args=[hash])  # 1 /products/
    url = '{}?page={}#categoria'.format(base_url, page)  # 3 /products/?category=42
    return url
    # return redirect('tomar_encuesta', hash)


def tomar_encuesta(request, hash):
    context = {}
    aeu = get_object_or_404(AplicarUniversoEncuestaPersona, hash=hash)
    request_page = request.GET.get('page')
    page = int(request_page) if request_page else 0
    # update
    todas_aeu_para_una_persona = AplicarUniversoEncuestaPersona.objects.filter(
        persona=aeu.persona,
        universo_encuesta=aeu.universo_encuesta
    )
    context.update({'todas_las_encuestas': todas_aeu_para_una_persona})

    if datetime.datetime.now().date() > aeu.universo_encuesta.fin:
        return redirect('evado:encuesta_cerrada', hash)
    if aeu.finalizado:
        return redirect('evado:encuesta_finalizada', hash)
    if request.method == "POST":
        dic = dict(request.POST.items())
        new_page = page
        if 'anterior' in dic:
            new_page -= 1
        elif 'siguiente' in dic:
            new_page += 1
        for i, encuesta_aplicada in enumerate(todas_aeu_para_una_persona):
            if 'profesor_nombre' in dic:  # No existe profesor en base de datos
                encuesta_aplicada.encuestado = dic['profesor_nombre']
                encuesta_aplicada.save()
            if "guardar" in dic or "anterior" in dic or "siguiente" in dic:
                guardada = guardar_respuestas(request, encuesta_aplicada, dic)
                if not guardada:
                    messages.add_message(request, messages.ERROR, "No se pudo guardar la encuesta para {}".format(
                        encuesta_aplicada.config_universo_persona.evaluado))
            # elif "enviar" in dic:
            #     estado = True
            #     for x in RespuestaAplicarUniversoEncuestaPersona.objects.filter(
            #             aplicar_universo_encuesta_persona=encuesta_aplicada):
            #         if not x.respuesta and x.pregunta.requerida:
            #             estado = False
            #             break
            #     if estado:
            #         for encuesta_aplicada in todas_aeu_para_una_persona:
            #             encuesta_aplicada.finalizado = timezone.now()
            #             encuesta_aplicada.save()
            #
            #         return redirect('encuesta_finalizada', hash)
            #     else:
            #         messages.add_message(request, messages.ERROR,
            #                              "No se pudo enviar la encuesta, asegurese de responder a todas las preguntas.")

            if encuesta_aplicada.universo_encuesta.activar_campo_comentario:
                if u'comentario_{}' in dic:
                    comentario = dic['comentario'][0]
                    encuesta_aplicada.comentario = comentario
                    encuesta_aplicada.save()

        estado = True
        for encuesta_aplicada in todas_aeu_para_una_persona:
            for x in RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                    aplicar_universo_encuesta_persona=encuesta_aplicada):
                if not x.respuesta and x.pregunta.requerida:
                    estado = False
                    break
        if estado:
            for encuesta_aplicada in todas_aeu_para_una_persona:
                encuesta_aplicada.finalizado = timezone.now()
                encuesta_aplicada.save()
                messages.add_message(request, messages.SUCCESS,
                                     "La encuesta a {} se ha finalizado, muchas gracias!".format(
                                         encuesta_aplicada.evaluado), 'success')
            return redirect('evado:encuesta_finalizada', hash)
        # else:
        #     messages.add_message(request, messages.ERROR,
        #                          "No se pudo enviar la encuesta, asegurese de responder a todas las preguntas.")

        redirect_url = redirect_url_tomar_encuesta(hash, new_page)
        return redirect(redirect_url)

    else:
        preguntas = aeu.universo_encuesta.encuesta.obtener_preguntas_no_respuesta_directa
        ultima_pregunta = aeu.universo_encuesta.ultima_pregunta_respondida
        if ultima_pregunta and not request_page:
            for index, pregunta in enumerate(preguntas):
                if pregunta == ultima_pregunta:
                    page = index

        context['pregunta'] = preguntas[page]
        context['total_preguntas'] = preguntas.count()
        context['previus'] = True if page - 1 >= 0 else False
        context['next'] = True if page + 1 < len(preguntas) else False

        if not request_page:
            redirect_url = redirect_url_tomar_encuesta(hash, page)
            return redirect(redirect_url)

    context['aplicar_encuesta'] = aeu
    return render(request, 'encuesta/encuesta_tomarAAGE.html', context)


def tomar_encuesta_original(request, hash):
    context = {}
    aeu = get_object_or_404(AplicarUniversoEncuestaPersona, hash=hash)
    if datetime.datetime.now().date() > aeu.universo_encuesta.fin:
        return redirect('encuesta_cerrada', hash)
    if aeu.finalizado:
        return redirect('encuesta_finalizada', hash)
    if request.method == "POST":
        dic = dict(request.POST.iterlists())
        if 'profesor_nombre' in dic:  # No existe profesor en base de datos
            aeu.encuestado = dic['profesor_nombre']
            aeu.save()
        if "guardar" in dic:
            try:
                RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                    aplicar_universo_encuesta_persona=aeu,
                    respuesta__isnull=False
                ).filter(
                    respuesta__check=True
                ).delete()
                for k, v in dic.items():
                    if "check" in k:  # check
                        id_pregunta = int(str(k).split('_')[1])
                        ids_respuesta = map(lambda x: int(x), v)
                        for x in ids_respuesta:
                            respuesta = Respuesta.objects.get(id=x)
                            res, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta)
                    if "escrita" in k:
                        id_pregunta = int(str(k).split('_')[1])
                        id_respuesta = int(str(k).split('_')[2])
                        respuesta = Respuesta.objects.get(id=id_respuesta)
                        escrita = v[0]
                        lis_respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                            aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                            respuesta__isnull=False).filter(respuesta__escrita=True)
                        if lis_respuestas.exists():
                            ready = False
                            for x in lis_respuestas.exclude(respuesta__isnull=True):
                                if x.respuesta.columna == respuesta.columna:
                                    x.respuesta_directa = escrita
                                    x.save()
                                    ready = True
                            if not ready:
                                obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                    aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta,
                                    respuesta_directa=escrita)
                        else:
                            obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta,
                                respuesta_directa=escrita)
                    if "respuesta" in k:
                        id_pregunta = int(str(k).split('_')[1])
                        id_respuesta = int(v[0])
                        respuesta = Respuesta.objects.get(id=id_respuesta)
                        listado_respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                            aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                            pregunta__es_respuesta_directa=False)
                        if listado_respuestas.exists():
                            if listado_respuestas.count() > 1:
                                ready = False
                                for r in listado_respuestas:
                                    if r.respuesta:
                                        if not r.respuesta.check and not r.respuesta.escrita:
                                            r.respuesta = respuesta
                                            r.save()
                                            ready = True
                                    else:
                                        r.respuesta = respuesta
                                        r.save()
                                        ready = True
                                if not ready:
                                    obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                        aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                                        respuesta=respuesta)
                            else:
                                obj = listado_respuestas[0]
                                obj.respuesta = respuesta
                                obj.save()
                        else:
                            obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta)
                    if "preguntadirecta" in k:
                        id_pregunta = int(str(k).split('_')[1])
                        res, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                            aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                            pregunta__es_respuesta_directa=True)
                        res.respuesta_directa = v[0]
                        res.save()
                messages.add_message(request, messages.SUCCESS, "Encuesta Guardada Satisfactoriamente!")
            except:
                traceback.print_exc()
                messages.add_message(request, messages.ERROR, "No se pudo guardar la encuesta correctamente.")
        elif "enviar" in dic:
            estado = True
            for x in RespuestaAplicarUniversoEncuestaPersona.objects.filter(aplicar_universo_encuesta_persona=aeu):
                if not x.respuesta and x.pregunta.requerida:
                    estado = False
            if estado:
                aeu.finalizado = timezone.now()
                aeu.save()
                return redirect('encuesta_finalizada', hash)
            else:
                messages.add_message(request, messages.ERROR,
                                     "No se pudo enviar la encuesta, asegurese de responder a todas las preguntas.")
        elif "guardar_enviar" in dic:
            try:
                RespuestaAplicarUniversoEncuestaPersona.objects.filter(aplicar_universo_encuesta_persona=aeu,
                                                                       respuesta__isnull=False).filter(
                    respuesta__check=True).delete()
                for k, v in dic.items():
                    if "check" in k:  # check
                        id_pregunta = int(str(k).split('_')[1])
                        ids_respuesta = map(lambda x: int(x), v)
                        for x in ids_respuesta:
                            respuesta = Respuesta.objects.get(id=x)
                            res, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta)
                    if "escrita" in k:
                        id_pregunta = int(str(k).split('_')[1])
                        id_respuesta = int(str(k).split('_')[2])
                        respuesta = Respuesta.objects.get(id=id_respuesta)
                        escrita = v[0]
                        lis_respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                            aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                            respuesta__isnull=False).filter(respuesta__escrita=True)
                        if lis_respuestas.exists():
                            ready = False
                            for x in lis_respuestas.exclude(respuesta__isnull=True):
                                if x.respuesta.columna == respuesta.columna:
                                    x.respuesta_directa = escrita
                                    x.save()
                                    ready = True
                            if not ready:
                                obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                    aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta,
                                    respuesta_directa=escrita)
                        else:
                            obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta,
                                respuesta_directa=escrita)
                    if "respuesta" in k:
                        id_pregunta = int(str(k).split('_')[1])
                        id_respuesta = int(v[0])
                        respuesta = Respuesta.objects.get(id=id_respuesta)
                        listado_respuestas = RespuestaAplicarUniversoEncuestaPersona.objects.filter(
                            aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                            pregunta__es_respuesta_directa=False)
                        if listado_respuestas.exists():
                            if listado_respuestas.count() > 1:
                                ready = False
                                for r in listado_respuestas:
                                    if r.respuesta:
                                        if not r.respuesta.check and not r.respuesta.escrita:
                                            r.respuesta = respuesta
                                            r.save()
                                            ready = True
                                    else:
                                        r.respuesta = respuesta
                                        r.save()
                                        ready = True
                                if not ready:
                                    obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                        aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                                        respuesta=respuesta)
                            else:
                                obj = listado_respuestas[0]
                                obj.respuesta = respuesta
                                obj.save()
                        else:
                            obj, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                                aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta, respuesta=respuesta)
                    if "preguntadirecta" in k:
                        id_pregunta = int(str(k).split('_')[1])
                        res, created = RespuestaAplicarUniversoEncuestaPersona.objects.get_or_create(
                            aplicar_universo_encuesta_persona=aeu, pregunta_id=id_pregunta,
                            pregunta__es_respuesta_directa=True)
                        res.respuesta_directa = v[0]
                        res.save()
                messages.add_message(request, messages.SUCCESS, "Encuesta Guardada Satisfactoriamente!")
            except:
                messages.add_message(request, messages.ERROR, "No se pudo guardar la encuesta correctamente.")
            estado = True
            for x in RespuestaAplicarUniversoEncuestaPersona.objects.filter(aplicar_universo_encuesta_persona=aeu):
                if not x.respuesta and x.pregunta.requerida:
                    estado = False
            if estado:
                aeu.finalizado = timezone.now()
                aeu.save()
                return redirect('encuesta_finalizada', hash)
            else:
                messages.add_message(request, messages.ERROR,
                                     "No se pudo enviar la encuesta, asegurese de responder a todas las preguntas.")
        if aeu.universo_encuesta.activar_campo_comentario:
            if u'comentario' in dic:
                comentario = dic['comentario'][0]
                aeu.comentario = comentario
                aeu.save()
        return redirect('tomar_encuesta', hash)
    context['aplicar_encuesta'] = aeu
    return render(request, 'encuesta/encuesta_tomar.html', context)


def encuesta_cerrada(request, hash):
    context = {}
    aue = get_object_or_404(AplicarUniversoEncuestaPersona, hash=hash)
    universo = aue.universo_encuesta
    context['universo'] = universo
    context['aplicar_encuesta'] = aue
    todas_aeu_para_una_persona = AplicarUniversoEncuestaPersona.objects.filter(persona=aue.persona,
                                                                               universo_encuesta=aue.universo_encuesta)
    context['todas_las_encuestas'] = todas_aeu_para_una_persona
    return render(request, 'encuesta/encuesta_cerrada2.html', context)


def encuesta_finalizada(request, hash):
    context = {}
    aeu = get_object_or_404(AplicarUniversoEncuestaPersona, hash=hash)
    universo = aeu.universo_encuesta
    p = aeu.persona
    encuestas = AplicarUniversoEncuestaPersona.objects.filter(universo_encuesta=universo, persona=p)
    restantes = encuestas.filter(finalizado=None).count()
    context['aplicar_encuesta'] = aeu
    context['encuestas'] = encuestas
    context['restantes'] = restantes
    todas_aeu_para_una_persona = AplicarUniversoEncuestaPersona \
        .objects.filter(persona=aeu.persona, universo_encuesta=aeu.universo_encuesta)
    context['todas_las_encuestas'] = todas_aeu_para_una_persona
    return render(request, 'encuesta/encuesta_finalizada2.html', context)


@login_required
def enviar_todas_encuestas(request, id_universo):
    universo = get_object_or_404(UniversoEncuesta, pk=id_universo)

    conexion = mail.get_connection()
    for x in universo.personas.all():
        try:
            enviar_encuesta(request, x.id, id_universo, unica=False, conexion=conexion)
        except:
            pass
    conexion.close()

    universo.correos_enviados = timezone.now()
    universo.save()
    messages.add_message(request, messages.SUCCESS, "Correos Enviados!")
    return redirect('universo_encuesta_detail', universo.id)


@login_required
def enviar_encuesta(request, id_persona, id_universo, unica=True, conexion=None):
    p = get_object_or_404(Persona, pk=id_persona)
    universo = get_object_or_404(UniversoEncuesta, pk=id_universo)
    pue = PersonaUniversoEncuesta.objects.get(persona=p, universo_encuesta=universo)
    mail_valid = False
    email = ''

    if pue:
        if p.email:
            email = p.email
            mail_valid = True
        else:
            x = p
            if x.email:
                m = x.email
                correos = [x.strip() for x in m.split(',')]
                for c in correos:
                    try:
                        validate_email(c)
                        email = c
                        mail_valid = True
                        break
                    except ValidationError:
                        mail_valid = False
        if mail_valid:
            encuestas = AplicarUniversoEncuestaPersona.objects.filter(universo_encuesta=universo, persona=p)
            if encuestas.exists():
                plaintext = get_template('encuesta/enviar_encuesta2.txt')
                htmly = get_template('encuesta/enviar_encuesta2.html')

                d = {'rut': p.rut,
                     'nombre': p.get_name,
                     'encuestas': encuestas,
                     'dominio': settings.DOMINIO_DEL_SITIO,
                     'universo': universo
                     }

                subject, from_email, to = 'Encuesta %s' % universo.encuesta.titulo, settings.EMAIL_HOST_USER, email
                text_content = plaintext.render(d)
                html_content = htmly.render(d)

                if conexion is None:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                else:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], connection=conexion)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                if unica:
                    messages.add_message(request, messages.SUCCESS, 'Correo enviado satisfactoriamente a %s' % p, 'success')
                pue.correo_enviado = timezone.now()
                pue.save()
            else:
                messages.add_message(request, messages.ERROR, 'No se encontraron encuestas para la persona %s' % p, 'error')
        else:
            messages.add_message(request, messages.ERROR, 'No se encontro registro de correo para la persona %s' % p, 'error')
    else:
        messages.add_message(request, messages.ERROR, 'No se pudo enviar el correo a %s' % p, 'error')

    return redirect('evado:universo_encuesta_detail', universo.id)


class PeriodoEncuestaListView(LoginRequired, ListView):
    model = PeriodoEncuesta
    template_name = 'encuesta/periodo_list.html'
    search_fields = [('nombres', 'icontains',), ('apellidos', 'icontains',), ('rut', 'icontains',),
                     ('funcion', 'icontains',), ('email', 'icontains',)]
    paginate_by = 10


class PeriodoEncuestaDetailView(LoginRequired, DetailView):
    model = PeriodoEncuesta
    template_name = 'encuesta/periodo_detail.html'


class PeriodoEncuestaUpdateView(LoginRequired, UpdateView):
    model = PeriodoEncuesta
    form_class = PeriodoEncuestaForm
    template_name = 'encuesta/periodo_create.html'


class PeriodoEncuestaCreateView(LoginRequired, CreateView):
    model = PeriodoEncuesta
    form_class = PeriodoEncuestaForm
    template_name = 'encuesta/periodo_create.html'


# Correos del Universo de encuestas
class CorreoUniversoEncuestaListView(LoginRequired, SearchableListMixin, ListView):
    model = CorreoUniversoEncuesta
    template_name = 'encuesta/correo_universo_list.html'


class CorreoUniversoEncuestaDetailView(LoginRequired, SearchableListMixin, DetailView):
    model = CorreoUniversoEncuesta
    template_name = 'encuesta/correo_universo_detail.html'


class CorreoUniversoEncuestaCreateView(LoginRequired, SearchableListMixin, CreateView):
    model = CorreoUniversoEncuesta
    form_class = CorreoUniversoEncuestaForm
    template_name = 'encuesta/correo_universo_create.html'


class CorreoUniversoEncuestaUpdateView(LoginRequired, SearchableListMixin, UpdateView):
    model = CorreoUniversoEncuesta
    form_class = CorreoUniversoEncuestaForm
    template_name = 'encuesta/correo_universo_update.html'


@login_required
def enviar_recordar_contestar_encuestas(request, id_universo_correo):
    correo = get_object_or_404(CorreoUniversoEncuesta, id=id_universo_correo)
    for p in correo.universo_encuesta.personas.all():
        if AplicarUniversoEncuestaPersona.objects.filter(persona=p, universo_encuesta=correo.universo_encuesta,
                                                         finalizado__isnull=True).count() > 0:
            recordar_contestar_encuestas(request, p.id, correo.id, False)
    correo.enviado = datetime.datetime.now()
    correo.save()
    return redirect('correo_universo_detail', correo.id)


def recordar_contestar_encuestas(request, id_persona, id_universo_correo, unica=True):
    p = get_object_or_404(Persona, pk=id_persona)
    correo = get_object_or_404(CorreoUniversoEncuesta, id=id_universo_correo)
    universo = correo.universo_encuesta
    pue = PersonaUniversoEncuesta.objects.get(persona=p, universo_encuesta=universo)
    mail_valid = False
    email = ''
    persona_termino_encuesta = True
    if AplicarUniversoEncuestaPersona.objects.filter(persona=p, universo_encuesta=universo,
                                                     finalizado__isnull=True).count() > 0:
        persona_termino_encuesta = False
    if pue:
        if not persona_termino_encuesta:
            if p.email:
                email = p.email
                mail_valid = True
            else:
                x = p
                if x.email:
                    m = x.email
                    correos = [x.strip() for x in m.split(',')]
                    for c in correos:
                        try:
                            validate_email(c)
                            email = c
                            mail_valid = True
                            break
                        except ValidationError:
                            mail_valid = False
            if mail_valid:
                encuestas = AplicarUniversoEncuestaPersona.objects.filter(universo_encuesta=universo, persona=p,
                                                                          finalizado__isnull=True)
                plaintext = get_template('encuesta/recordar_encuesta2.txt')
                htmly = get_template('encuesta/recordar_encuesta2.html')

                d = Context({'rut': p.rut,
                             'nombres': p.nombres,
                             'apellidos': p.apellidos,
                             'encuestas': encuestas,
                             'dominio': settings.DOMINIO_DEL_SITIO,
                             'contenido': correo.correo})

                subject, from_email, to = '%s' % correo.encabezado, 'docencia.encuesta@unach.cl', email
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                if unica:
                    messages.add_message(request, messages.SUCCESS, 'Correo enviado satisfactoriamente a %s' % p)
                pue.correo_enviado = timezone.now()
                pue.save()
            else:
                messages.add_message(request, messages.ERROR,
                                     'No se encontro registro de correo para la persona %s' % p)
        else:
            messages.add_message(request, messages.INFO, 'La persona %s ya finalizo su/s encuestas.' % p)
    else:
        messages.add_message(request, messages.ERROR, 'No se pudo enviar el correo a %s' % p)


@login_required
def enviar_mail_universo_encuestas(request):
    context = {
        'periodo': PeriodoEncuesta.objects.get(activo=True),
    }
    if request.method == 'POST':
        form = MailEncuestaUniversoForm(request.POST)
        if form.is_valid():
            personas = form.cleaned_data.get('personas', None)
            universo_encuesta = form.cleaned_data.get('universo_encuesta', None)
            contenido_mail = form.cleaned_data.get('contenido_mail', None)
            motivo = form.cleaned_data.get('motivo', None)
            enviar_correo_personalizado(personas, universo_encuesta, contenido_mail, motivo)
    else:
        form = MailEncuestaUniversoForm()
    context['form'] = form
    return render(request, 'encuesta/enviar_mail_universo_encuestas.html', context)


@login_required
def configurar_universo_personas(request):
    if request.method == 'POST':
        form = ConfigurarUniversoPersonaForm(request.POST)
        if form.is_valid():
            persona = form.cleaned_data.get('persona', None)
            evaluados = form.cleaned_data.get('evaluados', None)
            periodo = form.cleaned_data.get('periodo', None)
            tipo_encuesta = form.cleaned_data.get('tipo_encuesta', None)

            obj, created = ConfigurarEncuestaUniversoPersona.objects.get_or_create(
                persona=persona,
                periodo=periodo,
                tipo_encuesta=tipo_encuesta,
            )
            for x in evaluados:
                obj.evaluados.add(x)

            message = 'Configuracion {} agregada satisfactoriamente.'.format(obj)
            message_style = messages.INFO
            if not created:
                message = 'Configuracion {} actualizada satisfactoriamente.'.format(obj)
                message_style = messages.WARNING
            messages.add_message(request, message_style, message)
            return redirect('evado:configurar_universo_personas')
    else:
        form = ConfigurarUniversoPersonaForm()
    context = {
        'form': form,
        'formImport': ImportarConfiguracionUniversoPersonaForm(),
        'configuraciones': ConfigurarEncuestaUniversoPersona.objects.order_by('persona', 'tipo_encuesta', 'periodo')
    }
    return render(request, 'encuesta/configurar_universo_personas.html', context)


def enviar_correo_personalizado(personas, universos, contenido_mail, motivo):
    email = ''
    for x in personas:
        encuestas = AplicarUniversoEncuestaPersona.objects.filter(persona=x, universo_encuesta__in=universos,
                                                                  finalizado__isnull=True)
        if encuestas.exists():
            mail_valid = False
            if x.email:
                email = x.email
                mail_valid = True
            else:
                correo = x
                if correo.email:
                    m = correo.email
                    correos = [x.strip() for x in m.split(',')]
                    for c in correos:
                        try:
                            validate_email(c)
                            email = c
                            mail_valid = True
                            break
                        except ValidationError:
                            mail_valid = False
            if mail_valid:
                try:
                    plaintext = get_template('encuesta/recordar_encuesta2.txt')
                    htmly = get_template('encuesta/recordar_encuesta2.html')

                    d = Context({'rut': x.rut,
                                 'nombres': x.nombres,
                                 'apellidos': x.apellidos,
                                 'encuestas': encuestas,
                                 'dominio': settings.DOMINIO_DEL_SITIO,
                                 'contenido': contenido_mail})

                    subject, from_email, to = '%s' % motivo, settings.EMAIL_HOST_USER, email
                    text_content = plaintext.render(d)
                    html_content = htmly.render(d)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except:
                    pass


@login_required
def eliminar_configurar_universo_personas(request, pk):
    persona = get_object_or_404(Persona, id=pk)
    ConfigurarEncuestaUniversoPersona.objects.filter(persona=persona).delete()
    messages.add_message(request, messages.INFO,
                         'Configuracion de persona (%s) eliminada satisfactoriamente.' % persona)
    return redirect('configurar_universo_personas')


def eliminar_todos_eup(request):
    # persona = get_object_or_404(Persona)
    # ConfigurarEncuestaUniversoPersona.objects.filter(pk__in=[i.pk for i in persona]).delete()
    ConfigurarEncuestaUniversoPersona.objects.all().delete()
    messages.add_message(request, messages.INFO, 'Configuraciones de personas eliminadas satisfactoriamente')
    return redirect('configurar_universo_personas')


@login_required
def persona_upload(request):
    prompt = {
        'order': 'El orden del CSV debería ser nombres de evaluador, nombres de evaluado'
    }

    if request.method == 'GET':
        # TODO Template no existe como variable
        return render(request, request.template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        persona = Persona.objects.filter(rut=column[0], nombres=column[1], apellidos=column[2]).last()
        evaluado = Persona.objects.filter(nombres=column[3], apellidos=column[4]).last()
        if persona and evaluado:
            eup, created = ConfigurarEncuestaUniversoPersona.objects.get_or_create(persona=persona, evaluado=evaluado)
    context = {}

    if request.method == 'POST':
        messages.add_message(request, messages.SUCCESS, 'Importación realizada correctamente')
        return redirect('configurar_universo_personas')

    return render(request, context)


@login_required
def export_eup_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="evaluadores.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Personas - Evaluados')

    # Header del archivo
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['RUT Evaluador',
               'Nombres Evaluador',
               'Apellidos Evaluador',
               'Correo Evaluador',
               'Funcion Evaluador',
               'RUT Evaluado',
               'Nombres Evaluado',
               'Apellidos Evaluado',
               'Correo Evaluado'
               'Funcion Evaluado']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # fila 0 columna 0

    # cuerpo del archivo
    font_style = xlwt.XFStyle()
    rows = ConfigurarEncuestaUniversoPersona.objects.all().values_list(
        'persona__rut',
        'persona__nombres',
        'persona__apellidos',
        'persona__email',
        'persona__funcion',
        'evaluado__rut',
        'evaluado__nombres',
        'evaluado__apellidos',
        'evaluado__email',
        'evaluado__funcion'
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


@login_required
def import_eup_xls(request):
    """
        Importación de excel con configuración del universo de evaluados
    :param request: Request de la función
    :return: HTML
    """
    form = ImportarConfiguracionUniversoPersonaForm(request.POST, request.FILES)
    print(form.is_valid())
    excel_file = form.cleaned_data.get('file')
    periodo = form.cleaned_data.get('periodo_encuesta', None)
    tipo_encuesta = form.cleaned_data.get('tipo_universo_encuesta', None)
    df = pd.read_excel(excel_file)

    for row in df.to_dict(orient="records"):
        # from pdb import set_trace; set_trace()
        rut_evaluador = row.get("RUT Evaluador")
        nombres_evaluador = row.get("Nombres Evaluador")
        apellidos_evaluador = row.get("Apellidos Evaluador")
        correo_evaluador = row.get("Correo Evaluador")
        funcion_evaluador = row.get("Funcion Evaluador")
        colegio_evaluador = row.get("Colegio Evaluador")
        fundacion_evaluador = row.get("Fundacion Evaluador")

        # evaluado
        rut_evaluado = row.get("RUT Evaluado")
        nombres_evaluado = row.get("Nombres Evaluado")
        apellidos_evaluado = row.get("Apellidos Evaluado")
        correo_evaluado = row.get("Correo Evaluado")
        funcion_evaluado = row.get("Funcion Evaluado")
        colegio_evaluado = row.get("Colegio Evaluado")
        fundacion_evaluado = row.get("Fundacion Evaluado")

        try:
            p_new = Persona.objects.filter(rut=rut_evaluador).first()
            apellidos_evaluador_array = apellidos_evaluador.split(' ')
            if not p_new:
                p_new = Persona.objects.create(
                    rut=rut_evaluador,
                    nombres=nombres_evaluador,
                    apellido_paterno=apellidos_evaluador_array[0],
                    apellido_materno=apellidos_evaluador_array[1] if apellidos_evaluador_array[1] else '',
                )

            e_new = Persona.objects.filter(rut=rut_evaluado).first()
            apellidos_evaluado_array = apellidos_evaluado.split(' ')
            if not e_new:
                e_new = Persona.objects.create(
                    rut=rut_evaluado,
                    nombres=nombres_evaluado,
                    apellido_paterno=apellidos_evaluado_array[0],
                    apellido_materno=apellidos_evaluado_array[1] if apellidos_evaluado_array[1] else '',
                )

            if correo_evaluador is not None:
                p_new.email = correo_evaluador
                p_new.save()

            if correo_evaluado is not None:
                e_new.email = correo_evaluado
                e_new.save()

            ip, created = InfoPersona.objects.get_or_create(
                persona=p_new
            )
            ip.funcion = funcion_evaluador
            ip.colegio = colegio_evaluador
            ip.fundacion = fundacion_evaluador
            ip.save()

            ie, created = InfoPersona.objects.get_or_create(
                persona=e_new
            )
            ie.funcion = funcion_evaluado
            ie.colegio = colegio_evaluado
            ie.fundacion = fundacion_evaluado
            ie.save()

            if p_new and e_new:
                eup, eup_created = ConfigurarEncuestaUniversoPersona.objects.get_or_create(
                    persona=p_new,
                    periodo=periodo,
                    tipo_encuesta=tipo_encuesta
                )
                eup.evaluados.add(e_new)
                messages.add_message(request, messages.SUCCESS, 'Relación realizada correctamente', 'success')

        except MultipleObjectsReturned:
            p_new = Persona.objects.filter(rut=rut_evaluador).first()
            e_new = Persona.objects.filter(rut=rut_evaluado).first()

            if correo_evaluador is not None:
                p_new.email = correo_evaluador
                p_new.save()

            if correo_evaluado is not None:
                e_new.email = correo_evaluado
                e_new.save()

            if p_new and e_new:
                eup, eup_created = ConfigurarEncuestaUniversoPersona.objects.get_or_create(
                    persona=p_new,
                    evaluado=e_new
                )
                if eup_created:
                    messages.add_message(request, messages.SUCCESS, 'Relación realizada correctamente')

    return redirect('evado:configurar_universo_personas')
