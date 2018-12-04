from cajas.models import MovimientoCaja, Sesion


def get_sesion_abierta(user):
    sesion = Sesion.objects.filter(vendedor=user,
                                   fecha_cierre__isnull=True)
    return sesion.first() if sesion.exists() else None


def get_caja_abierta(request):
        movimientos = MovimientoCaja.objects.filter(apertura=True,
                                                    caja__estado=True,
                                                    vendedor=request.user)
        return movimientos.first().caja if movimientos.exists() else None


def get_apertura_caja(request):
    movimientos = MovimientoCaja.objects.filter(apertura=True,
                                                caja__estado=True,
                                                vendedor=request.user)
    return movimientos.first()
