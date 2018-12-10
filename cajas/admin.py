# -*- coding: utf-8 -*-
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.contrib.admin.utils import quote


from cajas.constants import TipoFlujoCaja
from cajas.forms import CierreCajaForm, DetalleVentaForm, VentaForm, PagoForm
from cajas.models import CategoriaFlujoCaja, RetiroDinero, IngresoDinero, FormaPago, Caja, MovimientoCaja, \
    AperturaCaja, CierreCaja, DetalleVenta, Venta, Pago, get_siguiente_numero
from nutrifit.globales import separar
from cajas.servicios import get_sesion_abierta


@admin.register(CategoriaFlujoCaja)
class CategoriaFlujoCajaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ['nombre', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'nombre_comprobante']
    search_fields = ['nombre', ]

    def has_delete_permission(self, request, obj=None):
        return False


class FlujoCajaAdmin(admin.ModelAdmin):
    readonly_fields = ['fecha']
    list_display = ['fecha', 'sesion_', '_monto', 'motivo']
    fields = [
        'categoria',
        'motivo',
        'monto',
        'fecha'
        'forma_pago'
    ]
    actions = None

    def sesion_(self, obj):

        return mark_safe(obj.sesion or '')
    sesion_.short_description = u'Sesión'

    def _monto(self, obj):
        return str(separar(int(round(obj.monto)))) +' Gs.'

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['fecha']
        self.fields = [
            'categoria',
            'motivo',
            'monto',
            'fecha',
            'forma_pago'
            ]
        return super(FlujoCajaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super(FlujoCajaAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = [
            'categoria',
            'motivo',
            'monto',
            'fecha',
            'sesion'
        ]
        self.readonly_fields = self.fields

        return super(FlujoCajaAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        return super(FlujoCajaAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        form = getattr(self,'advanced_search_form',None)
        qs = super(FlujoCajaAdmin, self).get_queryset(request)
        if form:
            if form.cleaned_data.get('motivo', ''):
                qs = qs.filter(motivo__icontains=form.cleaned_data['motivo'])
            if form.cleaned_data.get('caja', ''):
                qs = qs.filter(sesion__caja_id=form.cleaned_data['caja'].pk)
            if form.cleaned_data.get('desde', ''):
                qs = qs.filter(fecha__gte=form.cleaned_data['desde'])
            if form.cleaned_data.get('hasta', ''):
                qs = qs.filter(fecha__lte=form.cleaned_data['hasta'])
        return qs

    other_search_fields = {}

    # standard search

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(FlujoCajaAdmin, self).lookup_allowed(lookup, *args, **kwargs)


@admin.register(RetiroDinero)
class RetiroDineroAdmin(FlujoCajaAdmin):
    autocomplete_fields = ['categoria', 'forma_pago']

    def add_view(self, request, form_url='', extra_context=None):
        if not get_sesion_abierta(request.user):
            self.message_user(request, mark_safe(
                u'Debe realizar una <strong>"Apertura de Caja"</strong> para realizar esta acción'))
            return HttpResponseRedirect(reverse('admin:administracion_retirodinero_changelist'))
        return super(RetiroDineroAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def get_queryset(self, request):
        return super(RetiroDineroAdmin, self).get_queryset(request).filter(tipo=TipoFlujoCaja.EGRESO)

    def save_model(self, request, obj, form, change):
        obj.sesion = get_sesion_abierta(request.user)
        obj.tipo = TipoFlujoCaja.EGRESO
        res = super(RetiroDineroAdmin, self).save_model(request, obj, form, change)
        obj.sesion.caja.disponible -= obj.monto
        obj.sesion.caja.save()
        return res


@admin.register(IngresoDinero)
class IngresoDineroAdmin(FlujoCajaAdmin):
    autocomplete_fields = ['categoria', 'forma_pago']

    def add_view(self, request, form_url='', extra_context=None):
        if not get_sesion_abierta(request.user):
            self.message_user(request, mark_safe(u'Debe realizar una <strong>"Apertura de Caja"</strong> para realizar esta acción'))
            return HttpResponseRedirect(reverse('admin:administracion_ingresodinero_changelist'))
        return super(IngresoDineroAdmin, self).add_view(request,
                                                    form_url=form_url,
                                                    extra_context=extra_context)

    def get_queryset(self, request):
        return super(IngresoDineroAdmin, self).get_queryset(request).filter(tipo=TipoFlujoCaja.INGRESO)

    def save_model(self, request, obj, form, change):
        obj.sesion = get_sesion_abierta(request.user)
        obj.tipo = TipoFlujoCaja.INGRESO
        res = super(IngresoDineroAdmin, self).save_model(request, obj, form, change)
        obj.sesion.caja.disponible += obj.monto
        obj.sesion.caja.save()
        return res


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'monto_disponible', 'estado']
    search_fields = ['nombre']
    readonly_fields = ['estado', 'disponible']
    actions = None
    list_filter = ['estado']
    fields = ['nombre', 'disponible', 'activo', 'estado']

    def monto_disponible(self, obj):
        return separar(obj.disponible)
    monto_disponible.short_description = 'Disponible'


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    form = DetalleVentaForm

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 20


class DetalleVentaPagoInline(admin.TabularInline):
    model = Pago
    form = PagoForm
    autocomplete_fields = ('medio_de_pago', )
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    class Media:
        js = ('venta.js',)
    form = VentaForm
    list_display = ('id', 'fecha', 'cliente', 'factura', 'condicion', 'total', 'get_pagado')
    search_fields = ('cliente__nombre', )
    list_filter = (('fecha', DateRangeFilter), 'condicion',)
    inlines = (DetalleVentaInline, DetalleVentaPagoInline)
    autocomplete_fields = ('cliente', )
    actions = None

    def get_default_venta(self, object_id=False):
        return object_id and Venta.objects.get(pk=object_id) or Venta(id=get_siguiente_numero())

    def add_view(self, request, object_id=None, form_url='', extra_context={}, **kwargs):
        if not get_sesion_abierta(request.user):
            self.message_user(request, "NO PUEDE REALIZAR UNA VENTA SIN REALIZAR UNA APERTURA DE CAJA", level=messages.WARNING)
            info = self.model._meta.app_label, self.model._meta.model_name
            return HttpResponseRedirect('/admin/%s/%s/' % info)

        return super(VentaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        venta = obj
        venta.save()
        venta.sesion = get_sesion_abierta(request.user)
        venta.sesion.caja.disponible += venta.total
        venta.sesion.caja.save()
        return super(VentaAdmin, self).save_model(request, obj, form, change)


class MovimientoAdmin(admin.ModelAdmin):
    search_fields = ['caja__nombre', 'vendedor__username']
    actions = None
    list_display_links = None

    def monto_efectivo(self, obj):
        return mark_safe('<div >'+separar(int(obj.saldo_apertura or 0))+' Gs.</div>')

    def changelist_view(self, request, extra_context=None):
        self.current_user = request.user
        return super(MovimientoAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.current_user = request.user
        return super(MovimientoAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.current_user = request.user
        return super(MovimientoAdmin, self).change_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def modificar(self, obj):
        if self.current_user == obj.vendedor:
            opts = obj._meta
            pk_value = obj._get_pk_val()
            obj_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(quote(pk_value),),
                current_app=self.admin_site.name,
            )

            return format_html('<a href="%s">%s</a>'%(obj_url, obj.caja))

        return obj.caja

    modificar.short_description = 'Caja'
    modificar.allow_tags = False
    modificar.admin_order_field = 'caja__nombre'

    def caja_abierta(self, request):
        movimientos = MovimientoCaja.objects.filter(apertura=True,
                                                    caja__estado=True,
                                                    vendedor=request.user)
        return movimientos.exists()

    def save_model(self, request, obj, form, change):
        obj.vendedor = request.user
        return super(MovimientoAdmin,self).save_model(request, obj, form, change)

    def saldo_apertura_(self, obj):
        return separar(int(obj.saldo_apertura))


@admin.register(AperturaCaja)
class AperturaCajaAdmin(MovimientoAdmin):
    readonly_fields = ['saldo_apertura']
    fields = ['caja', 'fecha_apertura']
    list_display = ['modificar', 'vendedor', 'saldo_apertura_', 'fecha_apertura']

    class Media(object):
        css = {
            'all':('/static/admin/movimiento/movimiento_caja.css',)
        }
        js = (
            '/static/admin/apertura_caja/apertura_caja.js',

        )

    def save_model(self, request, obj, form, change):
        obj.caja.estado = True
        obj.caja.save()
        obj.vendedor = request.user
        obj.save()
        if not change:
            obj.saldo_apertura = obj.get_saldo_apertura()
            obj.disponible = obj.saldo_apertura
            obj.save()

    def get_queryset(self, request):
        queryset = super(AperturaCajaAdmin, self).get_queryset(request)
        return queryset

    def add_view(self, request, form_url='', extra_context=None):
        sesion = get_sesion_abierta(request.user)
        if sesion:
            self.message_user(request, "YA EXISTE UNA CAJA ABIERTA CON ESTE USUARIO.", level=messages.WARNING)
            info = self.model._meta.app_label, self.model._meta.model_name
            return HttpResponseRedirect('/admin/%s/%s/'%info)
        return super(AperturaCajaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)


@admin.register(CierreCaja)
class CierreCajaAdmin(MovimientoAdmin):
    readonly_fields = ['caja']
    form = CierreCajaForm
    fields = ['caja', 'fecha_cierre', 'saldo_apertura', 'ingresos', 'egresos', 'saldo_cierre']
    list_display = ['modificar', 'vendedor', 'fecha_apertura',
                    'saldo_apertura_', 'fecha_cierre', 'saldo_cierre_', 'acciones']
    actions = None

    def acciones(self, obj):
        html = '<a href="/admin/cajas/reporte_consolidado_pdf/%s">Consolidado</a>'%obj.pk
        return  mark_safe(html)

    def saldo_cierre_(self, obj):
        return separar(int(obj.saldo_cierre)).rjust(10)

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        obj.apertura = False
        obj.caja.estado = False
        obj.efectivo = obj.caja.disponible
        obj.saldo_cierre = obj.get_saldo_cierre()
        obj.caja.estado = False
        obj.caja.save()

        return super(CierreCajaAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super(CierreCajaAdmin, self).get_queryset(request)
        return queryset.all()

    def add_view(self, request, form_url='', extra_context=None):
        if not get_sesion_abierta(request):
            self.message_user(request, "NO EXISTE UNA CAJA ABIERTA CON ESTE USUARIO", level=messages.WARNING)
            info = self.model._meta.app_label, self.model._meta.model_name
            return HttpResponseRedirect('/admin/%s/%s/' % info)

        return super(CierreCajaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = CierreCaja.objects.get(pk=object_id)
        if obj.fecha_cierre:
            self.readonly_fields = ['caja', 'fecha_cierre']
        else:
            self.readonly_fields = ['caja']

        return super(CierreCajaAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(Pago)
class ReciboAdmin(admin.ModelAdmin):
    autocomplete_fields = ('venta', )
    list_display = ('id', 'comprobante_numero', 'venta', 'monto')
    search_fields = ('id', 'comprobante_numero', 'venta')
    list_filter = ('medio_de_pago', )
    actions = None
