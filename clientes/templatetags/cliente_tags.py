from django import template

register = template.Library()

@register.filter
def eliminar_separador_miles(numero):
    numero_str = str(numero)
    return numero_str
