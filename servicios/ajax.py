from django.http.response import JsonResponse

from servicios.models import Servicio


def get_servicio(request):
    servicio_id = (request.GET['servicio_id']).replace(" ", "")
    datos = {}

    if servicio_id == "":
        return JsonResponse(datos)

    servicio = Servicio.objects.get(pk=servicio_id)
    datos.update({'precio': int(servicio.precio)})

    return JsonResponse(datos)
