from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from carga_horaria.models import Profesor, AsignaturaBase, Asignatura, Asistente
from carga_horaria.formsAlexis import ProfesorForm, AsignaturaBaseForm, AsignaturaCreateForm, AsignaturaUpdateForm, AsistenteForm
from django.core.urlresolvers import reverse_lazy, reverse
from guardian.shortcuts import get_objects_for_user
from .models import Persona
from .models import Fundacion
from .models import Colegio
from .models import Periodo
from .models import Nivel


class LevelFilterMixin(object):
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel][::-1]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(plan__nivel=nivel)

        return qs



# FIXME: I will leave it like this for now,
# but it's still possible for somebody to poke object ids to see what shouldn't see
# fix this!!1


class SearchMixin(object):
    def get_queryset(self):
        qs = super(SearchMixin, self).get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            qs = qs.filter(persona__nombre__unaccent__icontains=q)
        return qs


def get_for_user(request, qs, lookup, user):
    periodo = request.session.get('periodo', 2020)

    if not user.is_superuser:
        colegios = [c.pk for c in get_objects_for_user(user, "carga_horaria.change_colegio")]
        
        # new logic for colegio switcher
        selected = request.session.get('colegio__pk', None)
        if selected:
            colegios = [selected]
        # end
            
        kwargs = {"{}__in".format(lookup): colegios,
                  "{}periode".format(lookup[:-2]): periodo}
        return qs.filter(**kwargs).distinct()
    else:
        colegios = [c.pk for c in Colegio.objects.all()]
        # new logic for colegio switcher
        selected = request.session.get('colegio__pk', None)
        if selected:
            colegios = [selected]
        # end
            
        kwargs = {"{}__in".format(lookup): colegios,
                  "{}periode".format(lookup[:-2]): periodo}
        return qs.filter(**kwargs).distinct()
        
    

class GetObjectsForUserMixin(object):
    def get_queryset(self):
        qs = super(GetObjectsForUserMixin, self).get_queryset()
        periodo = self.request.session.get('periodo', 2020)

        if not self.request.user.is_superuser:
            colegios = [c.pk for c in get_objects_for_user(self.request.user, "carga_horaria.change_colegio")]

            # new logic for colegio switcher
            selected = self.request.session.get('colegio__pk', None)
            if selected:
                colegios = [selected]
            # end
            
            kwargs = {"{}__in".format(self.lookup): colegios,
                      "{}periode".format(self.lookup[:-2]): periodo}
            return qs.filter(**kwargs).distinct()
        else:
            colegios = [c.pk for c in Colegio.objects.all()]
            # new logic for colegio switcher
            selected = self.request.session.get('colegio__pk', None)
            if selected:
                colegios = [selected]
            # end
            
            kwargs = {"{}__in".format(self.lookup): colegios,
                      "{}periode".format(self.lookup[:-2]): periodo}
            return qs.filter(**kwargs).distinct()


class ObjPermissionRequiredMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(ObjPermissionRequiredMixin, self).get_object(*args, **kwargs)
        if self.request.user.has_perm(self.permission, obj):
            return obj
        else:
            raise Http404


"""
    Comienzo Crud Profesor
"""
class ProfesorListView(LoginRequiredMixin, SearchMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de profesores
    """
    model = Profesor
    lookup = 'colegio__pk'
    template_name = 'carga_horaria/profesor/listado_profesor.html'
    search_fields = ['nombre', 'horas']
    paginate_by = 6



class ProfesorDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de Profesor
    """
    model = Profesor
    template_name = 'carga_horaria/profesor/detalle_profesor.html'


class ProfesorCreateView(LoginRequiredMixin, CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'carga_horaria/profesor/nuevo_profesor.html'
    success_url = reverse_lazy('carga-horaria:profesores')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProfesorCreateView, self).get_form_kwargs(*args, **kwargs)
        colegio_pk = self.request.session.get('colegio__pk', None)
        if colegio_pk:
            kwargs.update({'user': self.request.user,
                           'colegio': colegio_pk,
                           'fundacion': Colegio.objects.get(pk=self.request.session.get('colegio__pk', None)).fundacion.pk})
        else:
            kwargs.update({'user': self.request.user})

        return kwargs

    def form_valid(self, form):
        profesor = form.save(commit=False)
        profesor.persona, _ = Persona.objects.update_or_create(rut=form.cleaned_data['rut'],
                                                               defaults={'nombre': form.cleaned_data['nombre'],
                                                                         'adventista': form.cleaned_data['adventista'],
                                                                         'fecha_nacimiento': form.cleaned_data['fecha_nacimiento']})
        profesor.save()
        return redirect(reverse('carga-horaria:profesores'))


class ProfesorUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'carga_horaria/profesor/editar_profesor.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProfesorUpdateView, self).get_form_kwargs(*args, **kwargs)
        colegio_pk = self.request.session.get('colegio__pk', None)
        if colegio_pk:
            kwargs.update({'user': self.request.user,
                           'colegio': colegio_pk,
                           'fundacion': Colegio.objects.get(pk=self.request.session.get('colegio__pk', None)).fundacion.pk})
        else:
            kwargs.update({'user': self.request.user})

        return kwargs

    def form_valid(self, form):
        profesor = form.save(commit=False)
        profesor.persona, _ = Persona.objects.update_or_create(rut=form.cleaned_data['rut'],
                                                               defaults={'nombre': form.cleaned_data['nombre'],
                                                                         'adventista': form.cleaned_data['adventista'],
                                                                         'fecha_nacimiento': form.cleaned_data['fecha_nacimiento']})
        profesor.save()
        return redirect(self.get_success_url())


    def get_success_url(self):
        return reverse(
            'carga-horaria:profesor',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesor
    success_url = reverse_lazy('carga-horaria:profesores')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# """
#     Comienzo Crud Curso
# """
# class CursoListView(ListView):
#     """
#         Listado de cursos
#     """
#     model = Curso
#     template_name = 'carga_horaria/curso/listado_curso.html'
#     search_fields = ['periodo', 'letra']
#     paginate_by = 6


# class CursoDetailView(DetailView):
#     """
#         Detalle de curso
#     """
#     model = Curso
#     template_name = 'carga_horaria/curso/detalle_curso.html'


# class CursoCreateView(CreateView):
#     model = Curso
#     form_class = CursoForm
#     template_name = 'carga_horaria/curso/nuevo_curso.html'
#     success_url = reverse_lazy('carga-horaria:cursos')


# class CursoUpdateView(UpdateView):
#     model = Curso
#     form_class = CursoForm
#     template_name = 'carga_horaria/curso/editar_curso.html'

#     def get_success_url(self):
#         return reverse(
#             'carga-horaria:curso',
#             kwargs={
#                 'pk': self.object.pk,
#             }
#         )


# class CursoDeleteView(DeleteView):
#     model = Curso
#     success_url = reverse_lazy('carga-horaria:cursos')

#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


"""
    Comienzo Crud Asistente
"""
class AsistenteListView(LoginRequiredMixin, SearchMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de asistentes
    """
    model = Asistente
    lookup = 'colegio__pk'
    template_name = 'carga_horaria/asistente/listado_asistente.html'
    search_fields = ['nombre', 'horas']
    paginate_by = 6


class AsistenteDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de Asistente
    """
    model = Asistente
    template_name = 'carga_horaria/asistente/detalle_asistente.html'


class AsistenteCreateView(LoginRequiredMixin, CreateView):
    model = Asistente
    form_class = AsistenteForm
    template_name = 'carga_horaria/asistente/nuevo_asistente.html'
    success_url = reverse_lazy('carga-horaria:asistentes')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AsistenteCreateView, self).get_form_kwargs(*args, **kwargs)
        colegio_pk = self.request.session.get('colegio__pk', None)
        if colegio_pk:
            kwargs.update({'user': self.request.user,
                           'colegio': colegio_pk,
                           'fundacion': Colegio.objects.get(pk=self.request.session.get('colegio__pk', None)).fundacion.pk})
        else:
            kwargs.update({'user': self.request.user})

        return kwargs


    def form_valid(self, form):
        asistente = form.save(commit=False)
        asistente.persona, _ = Persona.objects.update_or_create(rut=form.cleaned_data['rut'],
                                                                defaults={'nombre': form.cleaned_data['nombre'],
                                                                          'adventista': form.cleaned_data['adventista'],
                                                                          'fecha_nacimiento': form.cleaned_data['fecha_nacimiento']})
        asistente.save()
        return redirect(reverse('carga-horaria:asistentes'))


class AsistenteUpdateView(LoginRequiredMixin, UpdateView):
    model = Asistente
    form_class = AsistenteForm
    template_name = 'carga_horaria/asistente/editar_asistente.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:asistente',
            kwargs={
                'pk': self.object.pk,
            }
        )

    def form_valid(self, form):
        asistente = form.save(commit=False)
        asistente.persona, _ = Persona.objects.update_or_create(rut=form.cleaned_data['rut'],
                                                                defaults={'nombre': form.cleaned_data['nombre'],
                                                                          'adventista': form.cleaned_data['adventista'],
                                                                          'fecha_nacimiento': form.cleaned_data['fecha_nacimiento']})
        asistente.save()
        return redirect(self.get_success_url())


class AsistenteDeleteView(LoginRequiredMixin, DeleteView):
    model = Asistente
    success_url = reverse_lazy('carga-horaria:asistentes')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)




"""
    Comienzo Crud Asignatura Base
"""
class AsignaturaBaseListView(LoginRequiredMixin, GetObjectsForUserMixin, ListView):
    """
        Listado de asignatura base
    """
    model = AsignaturaBase
    lookup = 'plan__colegio__pk'
    template_name = 'carga_horaria/asignaturabase/listado_asignaturabase.html'
    search_fields = ['nombre', 'plan']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(plan__nivel=nivel)

        return qs


class AsignaturaBaseDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de asignatura base
    """
    model = AsignaturaBase
    template_name = 'carga_horaria/asignaturabase/detalle_asignaturabase.html'


class AsignaturaBaseCreateView(LoginRequiredMixin, CreateView):
    model = AsignaturaBase
    form_class = AsignaturaBaseForm
    template_name = 'carga_horaria/asignaturabase/nuevo_asignaturabase.html'
    success_url = reverse_lazy('carga-horaria:asignaturasbase')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AsignaturaBaseCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user,
                       'colegio': self.request.session.get('colegio__pk', None)})
        return kwargs


class AsignaturaBaseUpdateView(LoginRequiredMixin, UpdateView):
    model = AsignaturaBase
    form_class = AsignaturaBaseForm
    template_name = 'carga_horaria/asignaturabase/editar_asignaturabase.html'

    def get_success_url(self):
        return reverse(
            'carga-horaria:asignaturabase',
            kwargs={
                'pk': self.object.pk,
            }
        )


class AsignaturaBaseDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignaturaBase
    success_url = reverse_lazy('carga-horaria:asignaturasbase')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


"""
    Comienzo Crud Asignatura
"""
class AsignaturaListView(LoginRequiredMixin, ListView):
    """
        Listado de asignatura
    """
    model = Asignatura
    template_name = 'carga_horaria/asignatura/listado_asignatura.html'
    search_fields = ['base', 'periodo']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['levels'] = [(tag.name, tag.value) for tag in Nivel][::-1]
        ctx['nivel_actual'] = self.request.GET.get('nivel')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        nivel = self.request.GET.get('nivel')
        if nivel:
            qs = qs.filter(base__plan__nivel=nivel)

        periodo = self.request.GET.get('periodo')
        if periodo:
            qs = qs.filter(periodo__pk=periodo)
        return qs


class AsignaturaDetailView(LoginRequiredMixin, DetailView):
    """
        Detalle de asignatura
    """
    model = Asignatura
    template_name = 'carga_horaria/asignatura/detalle_asignatura.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['periodo'] = Periodo.objects.get(pk=self.kwargs['periodo_pk'])
        return ctx

class AsignaturaCreateView(LoginRequiredMixin, CreateView):
    model = Asignatura
    form_class = AsignaturaCreateForm
    template_name = 'carga_horaria/asignatura/nuevo_asignatura.html'

    def form_valid(self, form):
        # dirty validation
        periodo = Periodo.objects.get(pk=self.kwargs['pk'])
        horas = form.cleaned_data['horas']
        available = periodo.available
        if horas > available:
            form.add_error('horas', "Horas superan el tiempo disponible ({})".format(available))
            return self.form_invalid(form)
        else:
            self.object = form.save()
            self.object.periodos.add(periodo)
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.kwargs['pk'],
            }
        )



class AsignaturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Asignatura
    form_class = AsignaturaUpdateForm
    template_name = 'carga_horaria/asignatura/editar_asignatura.html'

    def get_success_url(self):
        return reverse('carga-horaria:periodo', kwargs={'pk': self.kwargs['periodo_pk']})

    def form_valid(self, form):
        # dirty validation
        periodo = Periodo.objects.get(pk=self.kwargs['periodo_pk'])
        horas = form.cleaned_data['horas']
        old_horas = Asignatura.objects.get(pk=self.object.pk).horas
        delta = horas - old_horas
        available = periodo.available

        if delta > available:
            form.add_error('horas', "Horas superan el tiempo disponible ({})".format(available + old_horas))
            return self.form_invalid(form)
        elif self.object.base:
            if periodo.colegio.jec:
                horas_base = self.object.base.horas_jec
            else:
                horas_base = self.object.base.horas_nec

            if horas < horas_base:
                form.add_error('horas', "Horas deben ser como mínimo las del plan de estudios original ({})".format(horas_base))
                return self.form_invalid(form)

        return super().form_valid(form)


class AsignaturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Asignatura

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'carga-horaria:periodo',
            kwargs={
                'pk': self.kwargs['periodo_pk'],
            }
        )
