# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render

from cajas.models import Venta


def get_ventas_queryset(request,form):
    qs = Venta.objects.all()
    if form.cleaned_data.get('numero', ''):
        qs = qs.filter(Q(id__istartswith=form.cleaned_data['numero']) | Q(factura=form.cleaned_data['numero']))
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__nombre__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha__lte=form.cleaned_data.get('hasta', ''))
    return qs


