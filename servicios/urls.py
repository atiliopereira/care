from django.conf.urls import url

from servicios.ajax import get_servicio, get_detallespendientes

urlpatterns = [
    url('getservicio/$', get_servicio),
    url('getdetallespendientes/$', get_detallespendientes),
]
