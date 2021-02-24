from __future__ import unicode_literals
from django import template

from cajas.templatetags.caja_tags import advanced_search_form

register = template.Library()


@register.inclusion_tag('admin/servicios/ordendetrabajo/ot_search_form.html', takes_context=True)
def ot_search_form(context, cl):
    return advanced_search_form(context, cl)