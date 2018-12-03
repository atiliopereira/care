from django.conf.urls import url

from servicios.ajax import get_servicio

urlpatterns = [
    url('getservicio/$', get_servicio),
]
