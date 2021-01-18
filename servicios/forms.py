from django import forms

from servicios.models import DetalleOrdenDeTrabajo, OrdenDeTrabajo


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
