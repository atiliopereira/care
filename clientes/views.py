from django.shortcuts import render
from django.views.generic import DetailView

from clientes.models import Cliente, DatoFacturacion
from servicios.models import OrdenDeTrabajo, DetalleOrdenDeTrabajo


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "cliente_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['datos_de_facturacion'] = DatoFacturacion.objects.filter(cliente=self.object)
        context['sesiones'] = OrdenDeTrabajo.objects.filter(cliente=self.object).order_by("-fecha")
        context['detalles_sesiones'] = DetalleOrdenDeTrabajo.objects.filter(orden_de_trabajo__cliente=self.object)
        return context
