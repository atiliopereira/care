from django.contrib import admin
from django.contrib.admin.decorators import register

from clientes.models import DatoFacturacion, Cliente


class DatoFacturacionInline(admin.TabularInline):
    model = DatoFacturacion
    extra = 0


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre', )
    list_display = ('nombre', 'telefono', 'nacimiento', 'puntos_acumulados')
    inlines = (DatoFacturacionInline, )
    actions = None
