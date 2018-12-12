from django.contrib import admin
from django.contrib.admin.decorators import register
from daterange_filter.filter import DateRangeFilter

from turnos.models import DetalleTurno, Turno


class DetalleTurnoInline(admin.TabularInline):
    model = DetalleTurno
    autocomplete_fields = ('servicio',)
    extra = 0


@register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    search_fields = ('id', 'cliente')
    list_display = ('id', 'fecha', 'hora_inicio', 'hora_finalizacion', 'categoria', 'cliente', 'responsable')
    list_filter = (('fecha', DateRangeFilter), 'categoria')
    autocomplete_fields = ('cliente', 'responsable')
    inlines = (DetalleTurnoInline,)
    actions = None

