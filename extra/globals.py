import datetime
from django.http import HttpResponse
from django.utils.text import get_valid_filename
import xlwt


# escritor xls
def listview_to_excel(values_list, name, titulos):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('Libro1')
    default_style = xlwt.Style.default_style
    estilo_cabecera = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                                  'font: colour white, bold True;')

    for col, datos in enumerate(titulos):
        sheet.write(0, col, datos, style=estilo_cabecera)

    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata):
            style = default_style
            sheet.write(row + 1, col, val, style=style)
    response = HttpResponse(content_type='application/ms-excel')

    filename = "%s_%s.xls" % (name, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    filename = get_valid_filename(filename)
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    book.save(response)
    return response


def separador_de_miles(numero, gs=False):
    numero = str(numero)
    vector = numero.split(".")
    s = vector[0]
    for i in range(len(vector[0]), 0, -3):
        if i == 1 and s[0] == "-":
            s = s[:i] + s[i:]
        else:
            s = s[:i] + "." + s[i:]
    a = s[:len(s) - 1]
    if gs:
        return a
    if len(vector) == 2 and vector[1] != "00":

        if len(vector[1]) > 2:
            dato = vector[1][0:2]
        else:
            dato = vector[1]
        a += "," + dato

    return a
