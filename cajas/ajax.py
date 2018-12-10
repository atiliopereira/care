from django.http.response import JsonResponse
from cajas.models import Venta


def get_venta(request):
    venta_id = (request.GET['venta_id']).replace(" ", "")
    datos = {}

    if venta_id == "":
        return JsonResponse(datos)

    venta = Venta.objects.get(id=venta_id)
    saldo = venta.get_saldo()
    datos.update({'saldo': int(saldo)})

    return JsonResponse(datos)
