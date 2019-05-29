from dal import autocomplete
from django.db.models import Q

from clientes.models import DatoFacturacion, Cliente


class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cliente.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs


class DatoFacturacionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DatoFacturacion.objects.all()
        if self.q:
            qs = qs.filter(Q(razon_social__icontains=self.q) | Q(ruc__istartswith=self.q))
        return qs


class DatoFacturacionClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DatoFacturacionAutocomplete.get_queryset(self)
        if self.forwarded['cliente']:
            qs = qs.filter(cliente_id=int(self.forwarded['cliente']))
        return qs
