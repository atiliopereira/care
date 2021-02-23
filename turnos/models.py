import datetime

from django.contrib.auth.models import User
from django.db import models

from servicios.constants import CategoriaServicio
from turnos.constants import BoxTurno, Especialidad


class Turno(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    hora_inicio = models.TimeField(default=datetime.datetime.now)
    hora_finalizacion = models.TimeField(blank=True, null=True)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    box = models.CharField(max_length=6, choices=BoxTurno.BOXES, blank=True, null=True)
    especialidad = models.CharField(max_length=3, choices=Especialidad.ESPECIALIDADES)
    repeticiones = models.IntegerField(default=0, null=True, blank=True, verbose_name="Repeticiones semanales")

    def __str__(self):
        return str(self.fecha.strftime('%d/%m/%Y')) + ' - ' + str(self.hora_inicio.strftime('%H:%M')) + ' | ' + self.cliente.nombre


class DetalleTurno(models.Model):
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        super(DetalleTurno, self).save(*args, **kwargs)
        if self.turno.repeticiones > 0:
            inicio = self.turno_id - self.turno.repeticiones
            final = self.turno_id
            for i in range(inicio, final):
                DetalleTurno.objects.create(turno_id=i, servicio=self.servicio)
