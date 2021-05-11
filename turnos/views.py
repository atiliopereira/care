import datetime

from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.views.generic import ListView

from clientes.models import Cliente
from turnos.forms import AgendaForm
from turnos.models import Turno, DetalleTurno


class TurnosAgendaListView(ListView):
    model = Turno
    form = AgendaForm()
    template_name = "turnos_por_dia.html"
    queryset = Turno.objects.exclude(cancelado=True)

    def get_queryset(self):
        turnos = self.queryset
        fecha = self.request.GET.get('fecha', datetime.date.today().strftime("%Y-%m-%d"))
        if fecha != '':
            turnos = turnos.filter(fecha=fecha)

        especialidad = self.request.GET.get('especialidad', 'NON')
        if especialidad != 'NON':
            turnos = turnos.filter(especialidad=especialidad)

        return turnos.order_by('hora_inicio').reverse()

    def get_context_data(self, **kwargs):
        context = super(TurnosAgendaListView, self).get_context_data(**kwargs)
        context['fecha'] = fecha = self.request.GET.get('fecha', datetime.date.today().strftime("%Y-%m-%d"))
        dia_date = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        context['nro_de_dia'] = dia_date.weekday()
        context['dia_en_letras'] = dia_en_letras(dia_date.weekday())
        context['ahora'] = datetime.datetime.now().time()
        context['hoy'] = datetime.date.today().strftime("%d/%m/%Y")
        context['detalles'] = DetalleTurno.objects.filter(turno__fecha__gte=datetime.date.today())
        context['clientes'] = Cliente.objects.all()
        context['especialidad'] = self.request.GET.get('especialidad', '')
        return context


def dia_en_letras(num):
    if num == 0:
        return f'Lunes'
    elif num == 1:
        return f'Martes'
    elif num == 2:
        return f'Miércoles'
    elif num == 3:
        return f'Jueves'
    elif num == 4:
        return f'Viernes'
    elif num == 5:
        return f'Sábado'
    elif num == 6:
        return f'Domingo'
    else:
        return None


def cancelar_turno(request, pk):
    turno = Turno.objects.get(pk=pk)
    if request.method == 'POST':
        turno.cancelado = True
        turno.save()
        fecha = turno.fecha.strftime("%d/%m/%Y")
        especialidad = turno.especialidad
        return redirect(
            f'/admin/turnos/agenda/?fecha={fecha[6:10]}-{fecha[3:5]}-{fecha[0:2]}&especialidad={especialidad}')

    mensaje = f'¿Confirmar cancelación de turno: {turno}?'
    advertencia = f''
    return render(request, 'turno_confirm.html', {'mensaje': mensaje, 'advertencia': advertencia})




