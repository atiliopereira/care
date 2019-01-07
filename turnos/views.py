import datetime

from django.db.models import Count, Sum
from django.views.generic import ListView

from turnos.forms import AgendaForm, TurnoSearchForm
from turnos.models import Turno


class TurnosAgendaListView(ListView):
    model = Turno
    form = AgendaForm()
    template_name = "turnos_por_dia.html"
    queryset = Turno.objects.distinct().annotate(cantidad=Count('hora_inicio'))

    def get_queryset(self):
        turnos = self.queryset

        fecha = self.request.GET.get('fecha', datetime.date.today().strftime("%d/%m/%Y"))
        if fecha != '':
            vector = fecha.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            turnos = turnos.filter(fecha=fecha)

        return turnos.order_by('hora_inicio').reverse()

    def get_context_data(self, **kwargs):
        context = super(TurnosAgendaListView, self).get_context_data(**kwargs)
        context['fecha'] = self.request.GET.get('fecha', datetime.date.today().strftime("%d/%m/%Y"))
        context['fecha_de_entrega_hasta'] = self.request.GET.get('fecha_de_entrega_hasta', '')
        context['ahora'] = datetime.datetime.now().time()
        context['hoy'] = datetime.date.today().strftime("%d/%m/%Y")
        context['total_turnos'] = self.get_queryset().aggregate(total_cantidad=Sum('cantidad')).get('total_cantidad')
        return context





