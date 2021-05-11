from django.conf.urls import url

from turnos.views import TurnosAgendaListView, cancelar_turno

urlpatterns = [
        url(
           r'^agenda/$',
           TurnosAgendaListView.as_view(),
           name='turnosagenda_lis'
        ),
        url(r'^cancelar_turno/(?P<pk>\d+)/$', cancelar_turno, name='cancelar_turno'),
]
