from django.conf.urls import url

from clientes.autocomplete import DatoFacturacionClienteAutocomplete, ClienteAutocomplete
from clientes.views import ClienteDetailView

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
    url(r'^cliente_detail/(?P<pk>\d+)/$', ClienteDetailView.as_view(), name='cliente_det'),

]
