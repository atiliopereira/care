from django.conf.urls import url

from clientes.autocomplete import DatoFacturacionClienteAutocomplete, ClienteAutocomplete

urlpatterns = [
    url(
        r'^cliente-autocomplete/$',
        ClienteAutocomplete.as_view(),
        name='cliente-autocomplete',
    ),
    url(
        r'^datofacturacionventaautocomplete/$',
        DatoFacturacionClienteAutocomplete.as_view(),
        name='dato_facturacion__cliente-autocomplete',
    ),
]
