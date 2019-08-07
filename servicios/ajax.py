import json

from django.http.response import JsonResponse, HttpResponse

from clientes.models import Cliente
from extra.globals import separador_de_miles
from servicios.models import Servicio, DetalleOrdenDeTrabajo


def get_servicio(request):
    servicio_id = (request.GET['servicio_id']).replace(" ", "")
    datos = {}

    if servicio_id == "":
        return JsonResponse(datos)

    servicio = Servicio.objects.get(pk=servicio_id)
    datos.update({'precio': int(servicio.precio)})

    return JsonResponse(datos)


def get_detallespendientes(request):
    cliente_id = (request.GET['cliente_id']).replace(" ", "")
    datos = []

    if cliente_id == "":
        return JsonResponse(datos)

    detalles = DetalleOrdenDeTrabajo.objects.filter(orden_de_trabajo__cliente_id=cliente_id).exclude(facturado=True)
    cliente = Cliente.objects.get(pk=cliente_id)
    puntos_acumulados = cliente.puntos_acumulados

    for detalle in detalles:
        datos.append({'puntos_acumulados': separador_de_miles(puntos_acumulados), 'id': detalle.id,
                      'precio': separador_de_miles(detalle.servicio.precio)})
    return HttpResponse(json.dumps(datos),
                        content_type='application/json')
