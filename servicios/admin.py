import re

from django.contrib import admin
from django.contrib.admin.decorators import register
from django.db import models
from django.forms import Textarea, TextInput
from django.utils.safestring import mark_safe

from servicios.forms import DetalleOrdenDeTrabajoForm, OrdendetrabajoSearchForm
from servicios.models import Servicio, DetalleOrdenDeTrabajo, OrdenDeTrabajo
from servicios.views import get_ots_queryset


@register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    search_fields = ('descripcion', )
    list_filter = ('categoria', )
    list_display = ('descripcion', 'categoria', 'precio')
    actions = None


class DetalleOrdenDeTrabajoInline(admin.TabularInline):
    model = DetalleOrdenDeTrabajo
    form = DetalleOrdenDeTrabajoForm
    autocomplete_fields = ('servicio', )

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


@register(OrdenDeTrabajo)
class OrdenDeTrabajoAdmin(admin.ModelAdmin):
    class Media:
        js = ('orden_de_trabajo.js',)
    search_fields = ('id', 'cliente__nombre')
    list_display = ('id', 'fecha', 'hora', 'paciente', 'motivo_de_consulta', 'creado_por')
    autocomplete_fields = ('cliente', )
    actions = None

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 15,
                   'cols': 50,
                   'style': 'height: 4em;'})},
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    }

    def paciente(self, obj):
        html = f'<a href="/admin/clientes/cliente_detail/{obj.cliente.pk}">{obj.cliente.nombre}</a>'
        return mark_safe(html)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.save()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def add_view(self, request, form_url='', extra_context=None):
        template_response = super(OrdenDeTrabajoAdmin, self).add_view(
            request, form_url=form_url, extra_context=extra_context)
        # POST request won't have html response
        if request.method == 'GET':
            # removing Save and add another button: with regex
            template_response.content = re.sub("<input.*?_addanother.*?(/>|>)", "", template_response.rendered_content)
        return template_response

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset = self.model.objects.exclude(condicion='CO').exclude(estado='PG')

        return queryset, use_distinct

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(OrdenDeTrabajoAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def get_queryset(self, request):
        form = self.advanced_search_form
        qs = super(OrdenDeTrabajoAdmin, self).get_queryset(request)
        qs = get_ots_queryset(request, form)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):

        self.my_request_get = request.GET.copy()
        self.advanced_search_form = OrdendetrabajoSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        extra_context = extra_context or {}
        extra_context.update({'asf': OrdendetrabajoSearchForm,
                              'my_request_get': self.my_request_get,
                              'params': '?%s' % params[1].replace('%2F', '/') if len(params) > 1 else ''
                              })
        request.GET._mutable = True

        for key in self.advanced_search_form.fields.keys():
            try:
                temp = request.GET.pop(key)
            except KeyError:
                pass
            else:
                if temp != ['']:
                    self.other_search_fields[key] = temp
        request.GET_mutable = False

        return super(OrdenDeTrabajoAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)