from django.contrib import admin
from django.contrib.admin.decorators import register

from servicios.models import Servicio


@register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    search_fields = ('descripcion', )
    list_filter = ('categoria', )
    list_display = ('descripcion', 'categoria', 'precio')
    actions = None


