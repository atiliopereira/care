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

    def has_delete_permission(self, request, obj=None):
        return False