from django.conf.urls import url

from cajas.ajax import get_venta
from cajas.reports import reporte_consolidado_pdf, lista_ventas, factura_pdf

urlpatterns = [
    url(
        r'^reporte_consolidado_pdf/(?P<id>\w+)/$',
        reporte_consolidado_pdf,
        name='reporte_consolidado_pdf',
    ),
    url('getventa/$', get_venta),
    url(
        r'^lista_ventas/$',
        lista_ventas,
        name='lista_ventas',
    ),
    url(
        r'^generar_factura/(?P<id>\w+)/$',
        factura_pdf,
        name='generar_factura',
    ),

]
