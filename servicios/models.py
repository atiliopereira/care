# -*- coding: utf-8 -*-
from django.db import models

from servicios.constants import CategoriaServicio


class Servicio(models.Model):
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    categoria = models.CharField(max_length=3, choices=CategoriaServicio.CATEGORIAS, default=CategoriaServicio.PELUQUERIA)
    precio = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    activo = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.descripcion


