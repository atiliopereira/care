# -*- coding: utf-8 -*-
from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre y Apellido")
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")
    puntos_acumulados = models.IntegerField(default=0, verbose_name="Puntos acumulados")

    def __str__(self):
        return self.nombre


class DatoFacturacion(models.Model):
    class Meta:
        verbose_name = "Dato de facturación"
        verbose_name_plural = 'Datos de facturación'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    razon_social = models.CharField(max_length=100, verbose_name="Razón Social")
    ruc = models.CharField(max_length=30, verbose_name="RUC")

    def __str__(self):
        return self.razon_social + " - " + self.ruc
