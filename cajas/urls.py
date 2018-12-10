from django.conf.urls import url

from cajas.ajax import get_venta
from cajas.reports import reporte_consolidado_pdf

urlpatterns = [
    url(
        r'^reporte_consolidado_pdf/(?P<id>\w+)/$',
        reporte_consolidado_pdf,
        name='reporte_consolidado_pdf',
    ),
    url('getventa/$', get_venta),
]
