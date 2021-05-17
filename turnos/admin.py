import re

from django.contrib import admin
from django.contrib.admin.decorators import register
from daterange_filter.filter import DateRangeFilter
from django.shortcuts import redirect

from turnos.forms import TurnoForm, TurnoSearchForm
from turnos.models import DetalleTurno, Turno
from turnos.views import get_turnos_queryset


class DetalleTurnoInline(admin.TabularInline):
    model = DetalleTurno
    autocomplete_fields = ('servicio',)
    extra = 0


@register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    search_fields = ('cliente__nombre', 'id')
    list_display = ('id', 'fecha', 'hora_inicio', 'hora_finalizacion', 'cliente', 'box',)
    autocomplete_fields = ('cliente', )
    form = TurnoForm
    actions = None

    def response_add(self, request, obj, post_url_continue=None):
        fecha = request.POST['fecha']
        especialidad = request.POST['especialidad']
        return redirect(f'/admin/turnos/agenda/?fecha={fecha[6:10]}-{fecha[3:5]}-{fecha[0:2]}&especialidad={especialidad}')

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def add_view(self, request, form_url='', extra_context=None):
        template_response = super(TurnoAdmin, self).add_view(
            request, form_url=form_url, extra_context=extra_context)
        # POST request won't have html response
        if request.method == 'GET':
            # removing Save and add another button: with regex
            template_response.content = re.sub("<input.*?_addanother.*?(/>|>)", "", template_response.rendered_content)
        return template_response

    def has_delete_permission(self, request, obj=None):
        return False

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(TurnoAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def get_queryset(self, request):
        form = getattr(self, 'advanced_search_form', None)
        qs = super(TurnoAdmin, self).get_queryset(request)
        if form:
            qs = get_turnos_queryset(request, form)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):

        self.my_request_get = request.GET.copy()
        self.advanced_search_form = TurnoSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        extra_context = extra_context or {}
        extra_context.update({'asf': TurnoSearchForm,
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

        return super(TurnoAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)
