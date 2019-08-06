from datetime import datetime
from dal import autocomplete

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from cajas.models import CierreCaja, Venta, DetalleVenta, Caja, Pago
from clientes.models import Cliente


class CierreCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = '__all__'

    class Media:
        js = (
            '/static/admin/js/autoNumeric.js',
            '/static/admin/cierre_caja/cierre_caja.js',

        )
        css = {
            'all': ('/static/admin/movimiento/movimiento_caja.css',)
        }
    ingresos = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    egresos = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    saldo_cierre = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    saldo_apertura = forms.CharField(required=False,
                                     widget=forms.TextInput(
                                         attrs={'readonly': 'readonly', 'class':'auto', 'style': 'text-align: right'}))

    def __init__(self,*args,**kwargs):
        super(CierreCajaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ingresos'].initial = self.instance.total_ingresos()
            self.fields['egresos'].initial = self.instance.total_egresos()
            self.fields['saldo_cierre'].initial = self.instance.get_saldo_cierre()


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

        widgets = {
            "cliente": autocomplete.ModelSelect2(url='cliente-autocomplete'),
            "dato_facturacion": autocomplete.ModelSelect2(url='dato_facturacion__cliente-autocomplete',
                                                              forward=['cliente']),
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    puntos_acumulados = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False)
    total_medios_de_pago = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['total_medios_de_pago'] = instance.get_total_medios_de_pago()

        self.fields['puntos_acumulados'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(VentaForm, self).clean()
        total = cleaned_data.get("total")
        total_medios_de_pago = cleaned_data.get("total_medios_de_pago")
        condicion = cleaned_data.get('condicion')

        if condicion == 'CO':
            if int(total) != int(total_medios_de_pago):
                msg = "Suma de servicios a pagar no coinciden con suma de montos en medios de pago"
                self.add_error('total', msg)


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

        widgets = {
            "precio": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    subtotal = forms.CharField(
        widget=forms.TextInput(
            attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.'}), label="Subtotal")

    def __init__(self, *args, **kwargs):
        super(DetalleVentaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['subtotal'] = instance.servicio.servicio.precio
        self.fields['subtotal'].widget.attrs['readonly'] = True


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

        widgets = {
            "monto": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    def clean(self):
        cleaned_data = super(PagoForm, self).clean()
        monto = cleaned_data.get("monto")
        venta = cleaned_data.get("venta")
        medio_de_pago = cleaned_data.get("medio_de_pago")

        if int(monto) > int(venta.get_saldo()):
            msg = "Suma de servicios a pagar no coinciden con suma de montos en medios de pago"
            self.add_error('monto', msg)

        if medio_de_pago.nombre == 'PUNTOS':
            if int(monto) > int(venta.cliente.puntos_acumulados):
                msg = "Cantidad de puntos insuficiente"
                self.add_error('monto', msg)


class VentaSearchForm(forms.Form):
    numero = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Numero', 'style': 'width:120px;'}))
    cliente = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)


class MovimientoFlujoCajaForm(forms.Form):
    caja = forms.ModelChoiceField(
        queryset=Caja.objects.all(),
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
    )
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False, initial=datetime.now())


class CierreCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = '__all__'

    class Media:
        js = (
            '/static/admin/js/autoNumeric.js',
            '/static/admin/cierre_caja/cierre_caja.js',

        )
        css = {
            'all': ('/static/admin/movimiento/movimiento_caja.css',)
        }
    ingresos = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    egresos = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    saldo_cierre = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'auto', 'style': 'text-align: right'}))
    saldo_apertura = forms.CharField(required=False,
                                     widget=forms.TextInput(
                                         attrs={'readonly': 'readonly', 'class':'auto', 'style': 'text-align: right'}))

    def __init__(self, *args,**kwargs):
        super(CierreCajaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ingresos'].initial = self.instance.total_ingresos()
            self.fields['egresos'].initial = self.instance.total_egresos()
            self.fields['saldo_cierre'].initial = self.instance.get_saldo_cierre()
