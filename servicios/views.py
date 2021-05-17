from servicios.models import OrdenDeTrabajo
from sistema.models import Usuario
from turnos.models import Turno


def get_ots_queryset(request, form):
    usuario = Usuario.objects.get(pk=request.user.id)
    qs = OrdenDeTrabajo.objects.filter(creado_por=usuario.id)
    if form.cleaned_data.get('cliente', ''):
        qs = qs.filter(cliente__nombre__icontains=form.cleaned_data.get('cliente', ''))
    if form.cleaned_data.get('motivo', ''):
        qs = qs.filter(motivo_de_consulta__icontains=form.cleaned_data.get('motivo', ''))
    if form.cleaned_data.get('profesional', ''):
        qs = qs.filter(cliente_id__in=[i.cliente.id for i in Turno.objects.filter(box=form.cleaned_data['profesional'])])
    if form.cleaned_data.get('desde', ''):
        qs = qs.filter(fecha__gte=form.cleaned_data.get('desde', ''))
    if form.cleaned_data.get('hasta', ''):
        qs = qs.filter(fecha__lte=form.cleaned_data.get('hasta', ''))
    return qs