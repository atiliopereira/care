from decimal import Decimal
import datetime
from django import template
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.base import Node

from django.views.generic.dates import timezone_today

# Django template custom math filters
# Ref : https://code.djangoproject.com/ticket/361
# from postman.models import Message
from extra.globals import separador_de_miles

register = template.Library()


@register.filter
def paginator_delimiter(last, current):
    lista = []
    pages = int(15 / 2)
    for i in range(current - pages, current):
        if i >= 1:
            lista.append(i)

    for i in range(current, len(last)):
        if i < current + pages + 1:
            lista.append(i)
    return lista


@register.filter
def separador_miles(numero):
    return separador_de_miles(numero)
