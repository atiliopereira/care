from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from servicios.models import DetalleOrdenDeTrabajo, OrdenDeTrabajo
from turnos.constants import BoxTurno


class OrdenDeTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenDeTrabajo
        fields = "__all__"
        widgets = {
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    def __init__(self, *args, **kwargs):
        super(OrdenDeTrabajoForm, self).__init__(*args, **kwargs)
        self.fields['total'].widget.attrs['readonly'] = True



class OrdendetrabajoSearchForm(forms.Form):
    BOXES_EMPTY = (('', '---------'),)
    cliente = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    motivo = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Motivo', 'style': 'width:120px;'}))
    profesional = forms.ChoiceField(choices=BOXES_EMPTY + BoxTurno.BOXES, label='Profesional', required=False)
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)


class DetalleOrdenDeTrabajoForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenDeTrabajo
        fields = "__all__"

    precio = forms.CharField(
        widget=forms.TextInput(
            attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        label="Precio", initial="0"
    )

    def __init__(self, *args, **kwargs):
        super(DetalleOrdenDeTrabajoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['precio'] = instance.servicio.precio

        self.fields['precio'].widget.attrs['readonly'] = True
