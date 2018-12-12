from django.conf.urls import url

from turnos.views import TurnosAgendaListView

urlpatterns = [
        url(
           r'^agenda/$',
           TurnosAgendaListView.as_view(),
           name='turnosagenda_lis'
        ),
]
