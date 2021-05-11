import re

from django.contrib import admin
from django.contrib.admin.decorators import register
from daterange_filter.filter import DateRangeFilter
from django.shortcuts import redirect

from turnos.forms import TurnoForm
from turnos.models import DetalleTurno, Turno


class DetalleTurnoInline(admin.TabularInline):
    model = DetalleTurno
    autocomplete_fields = ('servicio',)
    extra = 0


@register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    search_fields = ('cliente__nombre', 'id')
    list_display = ('id', 'fecha', 'hora_inicio', 'hora_finalizacion', 'cliente', 'box')
    list_filter = (('fecha', DateRangeFilter), )
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