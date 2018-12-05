# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models

from servicios.constants import CategoriaServicio, EstadoFacturacion


class Servicio(models.Model):
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    categoria = models.CharField(max_length=3, choices=CategoriaServicio.CATEGORIAS, default=CategoriaServicio.PELUQUERIA)
    precio = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    activo = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.descripcion


class OrdenDeTrabajo(models.Model):
    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Ordenes de trabajo"

    fecha = models.DateField(default=datetime.date.today, editable=False)
    hora = models.TimeField(default=datetime.datetime.now, editable=False)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    estado_facturacion = models.CharField(max_length=2, choices=EstadoFacturacion.ESTADOS,
                                          default=EstadoFacturacion.NO_FACTURADO, editable=False)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.fecha.strftime('%d/%m/%Y') + ' | ' + str(self.cliente.nombre))

    def actualizar_facturacion(self):
        detalles_ot = DetalleOrdenDeTrabajo.objects.filter(orden_de_trabajo=self)
        total_detalles = len(detalles_ot)
        detalles_facturados = 0

        for detalle in detalles_ot:
            if detalle.facturado:
                detalles_facturados += 1
        if detalles_facturados is 0:
            self.estado_facturacion = EstadoFacturacion.NO_FACTURADO
        elif 0 < detalles_facturados < total_detalles:
            self.estado_facturacion = EstadoFacturacion.PARCIALMENTE
        elif detalles_facturados is total_detalles:
            self.estado_facturacion = EstadoFacturacion.FACTURADO
        self.save()


class DetalleOrdenDeTrabajo(models.Model):
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    facturado = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return str(self.servicio.descripcion) + ' - ' + str(self.orden_de_trabajo.id) + ' | ' + str(self.orden_de_trabajo.creado_por.username)

    def save(self, *args, **kwargs):
        super(DetalleOrdenDeTrabajo, self).save(*args, **kwargs)
        ot = OrdenDeTrabajo.objects.get(id=self.orden_de_trabajo.id)
        ot.actualizar_facturacion()
