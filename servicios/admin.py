from django.contrib import admin
from django.contrib.admin.decorators import register
from daterange_filter.filter import DateRangeFilter

from servicios.forms import DetalleOrdenDeTrabajoForm, OrdenDeTrabajoForm
from servicios.models import Servicio, DetalleOrdenDeTrabajo, OrdenDeTrabajo


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
    form = OrdenDeTrabajoForm
    search_fields = ('id', 'cliente')
    list_display = ('id', 'fecha', 'hora', 'cliente', 'total', 'facturado', 'creado_por')
    list_filter = (('fecha', DateRangeFilter), 'facturado')
    autocomplete_fields = ('cliente', )
    inlines = (DetalleOrdenDeTrabajoInline, )
    actions = None

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.save()
