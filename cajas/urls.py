from django.conf.urls import url

from cajas.reports import reporte_consolidado_pdf

urlpatterns = [
    url(
        r'^reporte_consolidado_pdf/(?P<id>\w+)/$',
        reporte_consolidado_pdf,
        name='reporte_consolidado_pdf',
    ),
]
