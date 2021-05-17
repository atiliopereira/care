import datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from turnos.constants import BoxTurno, OpcionesCancelados
from turnos.models import Turno


class AgendaForm(forms.Form):
    fecha = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'fecha'}), required=False,
                            initial=datetime.datetime.today())


class TurnoSearchForm(forms.Form):
    BOXES_EMPTY = (('', '---------'),)
    box = forms.ChoiceField(choices=BOXES_EMPTY + BoxTurno.BOXES, label='Profesional', required=False)
    cliente = forms.CharField(required=False, label='Paciente',
                              widget=forms.TextInput(attrs={'placeholder': 'Nombre y/o Apellido', 'style': 'width:220px;'}))
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False,
                            initial=datetime.date.today())

    cancelado = forms.ChoiceField(choices=OpcionesCancelados.OPCIONES, required=False,
                                  initial=OpcionesCancelados.NO_CANCELADOS)


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'

    def clean(self):
        cleaned_data = super(TurnoForm, self).clean()
        fecha = cleaned_data.get("fecha")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_finalizacion = cleaned_data.get("hora_finalizacion")
        cliente = cleaned_data.get("cliente")
        repeticiones = cleaned_data.get("repeticiones")
        box = cleaned_data.get("box")

        if repeticiones > 0:
            for i in range(repeticiones):
                multiplo_fecha = (i + 1) * 7
                fecha_i = fecha + datetime.timedelta(days=multiplo_fecha)
                Turno.objects.create(fecha=fecha_i, hora_inicio=hora_inicio, hora_finalizacion=hora_finalizacion,
                                     cliente=cliente, box=box)
