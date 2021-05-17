from django.contrib.auth.models import User
from django.db import models

from turnos.constants import BoxTurno


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    box = models.CharField(max_length=6, choices=BoxTurno.BOXES, blank=True, null=True)



