# -*- coding: utf-8 -*-
import math
import time
from io import BytesIO

from django.http import HttpResponse
from django.utils.encoding import force_text
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from cajas.constants import CondicionVenta
from cajas.forms import VentaSearchForm
from cajas.models import Sesion, DetalleVenta, Venta
from cajas.views import get_ventas_queryset
from extra.globals import listview_to_excel
from care.globales import separar, numero_to_letras
from care.settings import BASE_DIR

width, height = A4


def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y


def reporte_consolidado_pdf(request, id):
    def contenido(canvas, obj):
        from reportlab.lib.colors import darkblue, black
        canvas.setFillColor(darkblue)
        canvas.setFillColor(black)
        canvas.setStrokeColor(black)
        canvas.setFont("Helvetica-Bold", 13)

        canvas.drawString(250, 805, "Apertura Caja:")
        canvas.setFont("Helvetica", 13)
        canvas.drawString(370, 805, obj.fecha_apertura.strftime('%d/%m/%Y %H:%M'))

        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(250, 785, "Cierre Caja:")
        canvas.setFont("Helvetica", 13)

        fecha_cierre = obj.fecha_cierre.strftime('%d/%m/%Y %H:%M') if obj.fecha_cierre else 'CAJA ABIERTA'
        canvas.drawString(370, 785, fecha_cierre)

        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(250, 765, "Usuario Caja:")
        canvas.setFont("Helvetica", 13)
        canvas.drawString(370, 765, str(obj.vendedor))

        # LINEA HORIZONTAL QUE SEPARA LA CABECERA DEL RESTO
        canvas.line(30, 755, 550, 755)
        # LINEA VERTICAL QUE SEPARA LOGO DE LOS DATOS DE LA EMPRESA

        row = 720
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(30, row, "Saldo Inicial: ")
        canvas.drawString(450, row, separar(int(round(obj.get_saldo_apertura()))).rjust(12))
        # for x in obj.ingresos_egresos_apertura():
        #     print x.descripcion,x.monto,x.id
        #
        # for x in obj.ingresos_egresos_cierre():
        #     print x.descripcion, x.monto, x.id

        canvas.setFont("Helvetica", 11)
        for movimiento in obj.ingresos_egresos_apertura():
            row -= 20
            canvas.drawString(100, row, force_text(movimiento.descripcion))
            canvas.drawString(450, row, separar(int(round(movimiento.monto))).rjust(15))

        row -= 20
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(30, row, "Ingresos:")
        canvas.drawString(450, row, separar(int(round(obj.total_ingresos()))).rjust(15))

        canvas.setFont("Helvetica", 11)
        for ingreso in obj.ingresos():
            row -= 20
            canvas.drawString(100, row, force_text(ingreso.descripcion))
            canvas.drawString(450, row, separar(int(round(ingreso.monto))).rjust(15))

        row -= 20
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(30, row, "Egresos:")
        canvas.drawString(450, row, separar(int(round(obj.total_egresos()))).rjust(15))

        canvas.setFont("Helvetica", 11)
        for egreso in obj.egresos():
            row -= 20
            canvas.drawString(100, row, egreso.descripcion)
            canvas.drawString(450, row, separar(int(round(egreso.monto))).rjust(15))

        row -= 30
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawString(30, row, "Saldo Final: ")
        canvas.drawString(450, row, separar(int(round(obj.get_saldo_cierre()))).rjust(15))

        canvas.setFont("Helvetica", 11)
        for movimiento in obj.ingresos_egresos_cierre():
            row -= 20
            canvas.drawString(100, row, force_text(movimiento.descripcion))
            canvas.drawString(450, row, separar(int(round(movimiento.monto))).rjust(15))

        row -= 30
        canvas.line(30, row, 550, row)

        row -= 30
        canvas.setFont("Helvetica", 10)
        canvas.drawString(30, row, "Fecha: %s" % time.strftime("%Y/%m/%d"))
        canvas.drawString(200, row, "Hora: %s" % time.strftime("%X"))
        canvas.drawString(350, row, "Impreso por: %s" % request.user)

    obj = Sesion.objects.get(pk=id)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Consolidado.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    contenido(p, obj)
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def lista_ventas(request):
    form = VentaSearchForm(request.GET)
    form.is_valid()

    desde = form.cleaned_data.get('desde', '')
    if desde:
        desde = desde.strftime("%d/%m/%Y")
    hasta = form.cleaned_data.get('hasta', '')
    if hasta:
        hasta = hasta.strftime("%d/%m/%Y")

    queryset = get_ventas_queryset(request, form)
    total = 0
    pagado = 0

    nombre_archivo = 'lista_ventas'

    lista_datos = []
    for venta in queryset.order_by('fecha'):
        total += venta.total
        pagado += venta.pagado
        if venta.condicion == 'CO':
            condicion = 'Contado'
        elif venta.condicion == 'CR':
            condicion = 'Crédito'

        if venta.estado == 'PE':
            estado = 'Pendiente'
        elif venta.estado == 'PG':
            estado = 'Pagado'

        lista_datos.append([
            venta.fecha.strftime("%d/%m/%Y"),
            venta.cliente.nombre,
            condicion,
            estado,
            separar(int(venta.total)),
            separar(int(venta.pagado))
        ])
    lista_datos.append([])
    lista_datos.append(['', '', '', 'Total', separar(int(total)), separar(int(pagado))])
    lista_datos.append([])
    lista_datos.append(['Desde: ', desde, 'Hasta: ', hasta])
    titulos = ['Fecha', 'Cliente', 'Condicion', 'Estado', 'Monto', 'Pagado']
    response = listview_to_excel(lista_datos, nombre_archivo, titulos)
    return response


def factura_pdf(request, id):
    def contenido(canvas, venta):
        from reportlab.lib.colors import darkblue, black
        canvas.setFillColor(darkblue)
        canvas.setFillColor(black)
        canvas.setStrokeColor(black)
        canvas.setFont("Helvetica", 10)

        # COPIA SUPERIOR
        canvas.drawString(100, 703, force_text(venta.fecha.strftime('%d/%m/%Y') or ''))
        if venta.condicion == 'CO':
            canvas.drawString(430, 702, 'X')
        elif venta.condicion == 'CR':
            canvas.drawString(495, 702, 'X')
        canvas.drawString(120, 688, force_text(venta.dato_facturacion.razon_social or '').upper())
        canvas.drawString(422, 688, force_text(venta.dato_facturacion.ruc or ''))

        row = 650
        canvas.setFont("Helvetica", 10)
        detalles = DetalleVenta.objects.filter(venta=venta)
        total_venta = 0
        for detalle in detalles:
            row -= 15
            canvas.drawString(43, row, force_text('1'))
            canvas.drawString(73, row, force_text(detalle.servicio.servicio))
            canvas.drawString(470, row, force_text(separar(int(detalle.servicio.servicio.precio))).rjust(15, ' '))
            total_venta += int(detalle.servicio.servicio.precio)

        canvas.setFont("Helvetica", 11)

        row = 510
        canvas.drawString(460, row, force_text(separar(total_venta)).rjust(15, ' '))
        row = 492
        canvas.drawString(152, row, numero_to_letras(total_venta))
        row = 459
        canvas.drawString(233, row, force_text(separar(math.ceil(total_venta/11))).rjust(12, ' '))
        canvas.drawString(390, row, force_text(separar(math.ceil(total_venta / 11))).rjust(12, ' '))

        #COPIA INFERIOR
        canvas.drawString(100, 285, force_text(venta.fecha.strftime('%d/%m/%Y') or ''))
        if venta.condicion == 'CO':
            canvas.drawString(430, 285, 'X')
        elif venta.condicion == 'CR':
            canvas.drawString(495, 285, 'X')
        canvas.drawString(120, 270, force_text(venta.dato_facturacion.razon_social or '').upper())
        canvas.drawString(422, 270, force_text(venta.dato_facturacion.ruc or ''))
        row = 232
        canvas.setFont("Helvetica", 10)
        detalles = DetalleVenta.objects.filter(venta=venta)
        total_venta = 0
        for detalle in detalles:
            row -= 15
            canvas.drawString(43, row, force_text('1'))
            canvas.drawString(73, row, force_text(detalle.servicio.servicio))
            canvas.drawString(470, row, force_text(separar(int(detalle.servicio.servicio.precio))).rjust(15, ' '))
            total_venta += int(detalle.servicio.servicio.precio)

        canvas.setFont("Helvetica", 11)

        row = 92
        canvas.drawString(460, row, force_text(separar(total_venta)).rjust(15, ' '))
        row = 74
        canvas.drawString(152, row, numero_to_letras(total_venta))
        row = 41
        canvas.drawString(233, row, force_text(separar(math.ceil(total_venta / 11))).rjust(12, ' '))
        canvas.drawString(390, row, force_text(separar(math.ceil(total_venta / 11))).rjust(12, ' '))

    venta = Venta.objects.get(pk=id)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % str(venta)

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    contenido(p, venta)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
