# -*- coding: utf-8 -*-


class CategoriaServicio:
    PELUQUERIA = 'pel'
    SPA = 'spa'

    CATEGORIAS = (
        (PELUQUERIA, 'Peluquería'),
        (SPA, 'Spa')
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
