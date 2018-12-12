# -*- coding: utf-8 -*-

import time
from io import BytesIO

from django.http import HttpResponse
from django.utils.encoding import force_text
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from cajas.models import Sesion
from nutrifit.globales import separar


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
