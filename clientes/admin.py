from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from clientes.models import DatoFacturacion, Cliente


class DatoFacturacionInline(admin.TabularInline):
    model = DatoFacturacion
    extra = 0


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre', )
    readonly_fields = ('puntos_acumulados', )
    list_display = ('nombre', 'documento', 'telefono', 'nacimiento', 'puntos_acumulados', 'acciones')
    inlines = (DatoFacturacionInline, )
    actions = None

    def acciones(self, obj):
        html = '<a href="/admin/clientes/cliente_detail/%s">Ver</a>'%obj.pk
        return mark_safe(html)
