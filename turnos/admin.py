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
    list_display = ('id', 'fecha', 'hora_inicio', 'hora_finalizacion', 'categoria', 'cliente', 'responsable')
    list_filter = (('fecha', DateRangeFilter), 'categoria')
    autocomplete_fields = ('cliente', 'responsable')
    inlines = (DetalleTurnoInline,)
    form = TurnoForm
    actions = None

    def response_add(self, request, obj, post_url_continue=None):
        fecha = request.POST['fecha']
        return redirect('/admin/turnos/agenda/?fecha=' + fecha[0:2] + '%2F' + fecha[3:5] + '%2F' + fecha[6:10] )