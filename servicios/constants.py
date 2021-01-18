# -*- coding: utf-8 -*-


class CategoriaServicio:
    CATEGORIA_1 = 'CA1'
    CATEGORIA_2 = 'CA2'

    CATEGORIAS = (
        (CATEGORIA_1, 'Categoría 1'),
        (CATEGORIA_2, 'Categoría 2')
    )


class EstadoFacturacion:
    NO_FACTURADO = 'no'
    PARCIALMENTE = 'pa'
    FACTURADO = 'si'

    ESTADOS = (
        (NO_FACTURADO, 'No facturado'),
        (PARCIALMENTE, 'Facturado Parcialmente'),
        (FACTURADO, 'Facturado Totalmente')
    )
