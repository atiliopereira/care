# -*- coding: utf-8 -*-
class TipoFlujoCaja:
    INGRESO = 'IN'
    EGRESO = 'EG'

    TIPOS = (
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
    )


class CondicionVenta:
    CONTADO = 'CO'
    CREDITO = 'CR'

    CONDICIONES = (
        (CONTADO, 'Contado'),
        (CREDITO, 'Crédito'),
    )


def get_categoria_flujo_venta():
    from cajas.models import CategoriaFlujoCaja
    queryset = CategoriaFlujoCaja.objects.filter(nombre='VENTAS')
    if queryset.exists():
        return queryset.first()
    return CategoriaFlujoCaja.objects.create(
        nombre='VENTAS',
        tipo=TipoFlujoCaja.INGRESO,
        activo=True
    )
