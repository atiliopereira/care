from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from cajas.constants import TipoFlujoCaja, CondicionVenta, get_categoria_flujo_venta, EstadoPago
from clientes.models import Cliente
from servicios.models import OrdenDeTrabajo, DetalleOrdenDeTrabajo


def get_siguiente_numero():
    from django.db import connection
    with connection.cursor() as cursor:
        try:
            cursor.execute('''SELECT MAX(id) FROM cajas_venta''')
            id = cursor.fetchone()[0]
        except:
            id = 0
        return id and (id + 1) or 1


class Caja(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(choices=((True, 'Abierta'), (False, 'Cerrada')), default=False)
    disponible = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class FormaPago(models.Model):
    codigo = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=30, unique=True)
    nombre_comprobante = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Sesion(models.Model):
    class Movimiento:
        def __init__(self, descripcion, monto, id):
            self.descripcion = descripcion
            self.monto = monto
            self.id = id

    vendedor = models.ForeignKey(User, on_delete=models.PROTECT)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT)
    fecha_apertura = models.DateTimeField(default=datetime.now)
    fecha_cierre = models.DateTimeField(null=True)
    saldo_apertura = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    saldo_cierre = models.DecimalField(decimal_places=2, max_digits=14, default=0)

    # satanas estuvo aqui
    def agrupar(self, lista):
        values = set(map(lambda x: x.id, lista))
        newlist = []
        for x in values:
            aux = []
            for y in lista:
                if y.id == x:
                    aux.append(y)
            newlist.append(aux)
        true_list = []
        for b in newlist:
            total = 0
            for a in b:
                total += a.monto
            true_list.append(self.Movimiento(a.descripcion, total, a.id))
        return true_list

    def __str__(self):
        info = {
            'fecha': self.fecha_apertura.strftime('%d/%m/%Y - %H:%m'),
            'usuario' : self.vendedor.username,
            'caja' : self.caja
        }
        return mark_safe('<strong>Fecha:</strong> {fecha} hs. <strong>Usuario:</strong> {usuario}  <strong>Caja:</strong> {caja}'.format(**info))

    def ingresos(self):
        lista_ingresos = []
        for ingreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.INGRESO):
            if ingreso.forma_pago:
                lista_ingresos.append(self.Movimiento(
                    descripcion=str(ingreso.forma_pago),
                    monto=ingreso.monto,
                    id=ingreso.forma_pago.pk
                ))
        return self.agrupar(lista_ingresos)

    def egresos(self):
        lista_egresos = []
        for egreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.EGRESO):
            lista_egresos.append(self.Movimiento(
                descripcion=str(egreso.categoria),
                monto=egreso.monto,
                id=egreso.categoria.pk
            ))
        return self.agrupar(lista_egresos)

    def ingresos_egresos_apertura(self):
        obj = Sesion.objects.filter(pk__lt=self.pk)
        if obj:
            return obj.order_by('-id').first().ingresos_egresos_cierre()
        return []

    def ingresos_egresos_cierre(self):
        apertura = self.ingresos_egresos_apertura()
        egresos = []
        for egreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.EGRESO):
            if egreso.forma_pago:
                egresos.append(self.Movimiento(
                    descripcion=str(egreso.forma_pago),
                    monto=egreso.monto,
                    id=egreso.forma_pago.pk
                ))
        ingresos = self.ingresos()
        movimientos = self.agrupar(ingresos+egresos+apertura)
        for m in movimientos: m.monto = 0

        for i in apertura:
            for m in movimientos:
                if i.id == m.id:
                    m.monto += i.monto

        for i in ingresos:
            for m in movimientos:
                if i.id == m.id:
                    m.monto += i.monto

        for e in egresos:
            for m in movimientos:
                if e.id == m.id:
                    m.monto -= e.monto
        return movimientos

    def total_ingresos(self):
        total = 0
        for ingreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.INGRESO):
            total += ingreso.monto
        return int(round(total))

    def total_egresos(self):
        total = 0
        for egreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.EGRESO):
            total += egreso.monto
        return int(round(total))

    def get_saldo_apertura(self):
        total = 0
        if not self.saldo_apertura or self.saldo_apertura == 0:
            for m in self.ingresos_egresos_apertura():
                total += m.monto
            return int(round(total))
        return self.saldo_apertura

    def get_saldo_cierre(self):
        total = 0
        for m in self.ingresos_egresos_cierre():
            total += m.monto
        return int(round(total))


class MovimientoCaja(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=datetime.now)
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT)
    apertura = models.BooleanField(choices=((True, 'Apertura'), (False, 'Cierre')), verbose_name='tipo')
    efectivo = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s'%(self.fecha, self.vendedor.username)


class AperturaCaja(Sesion):
    class Meta:
        proxy = True
        verbose_name = "Apertura de Caja"
        verbose_name_plural = 'Aperturas de Caja'

    def __str__(self):
        return '%s; %s' % (self.fecha_apertura.strftime('%d/%m/%Y - %H:%m'), self.vendedor.username)


class CierreCaja(Sesion):
    class Meta:
        proxy = True
        verbose_name = "Cierre de Caja"
        verbose_name_plural = 'Cierres de Caja'

    def __str__(self):
        return '%s - %s' % (self.fecha_cierre.strftime('%d/%m/%Y - %HH:%mm') if self.fecha_cierre else '', self.vendedor.username)


class Venta(models.Model):
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    dato_facturacion = models.ForeignKey('clientes.DatoFacturacion', on_delete=models.PROTECT, null=True, blank=True)
    factura = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(default=date.today)
    condicion = models.CharField(choices=CondicionVenta.CONDICIONES, default=CondicionVenta.CONTADO, max_length=2,
                                 verbose_name='Condicion de Venta')
    anulado = models.BooleanField(default=False, editable=False)
    total = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    pagado = models.DecimalField(max_digits=15, decimal_places=0, default=0, editable=False)
    sesion = models.ForeignKey(Sesion, null=True, blank=True, editable=False, on_delete=models.PROTECT)
    estado = models.CharField(choices=EstadoPago.ESTADOS, default=EstadoPago.PENDIENTE, max_length=2,
                              verbose_name='Estado de Pago', editable=False)

    def __str__(self):
        if self.factura:
            cadena = "FACTURA " + self.get_condicion_display() + " Nro.: " + self.factura
        else:
            cadena = "VENTA " + self.get_condicion_display() + " Nro.: " + str(self.id)
        return str(cadena) + ' | ' + str(self.cliente.nombre)

    def get_total_medios_de_pago(self):
        detalles = Pago.objects.filter(venta_id=self.id)
        total = 0
        for detalle in detalles:
            total = total + detalle.monto
        return total

    def get_pagado(self):
        pagos = Pago.objects.filter(venta=self)
        suma = 0
        for pago in pagos:
            suma += pago.monto
        return suma

    get_pagado.short_description = 'Pagado'

    def get_saldo(self):
        return self.total - self.pagado

    def save(self, *args, **kwargs):
        if self.pk:
            self.pagado = self.get_pagado()
            if self.pagado >= self.total:
                self.estado = EstadoPago.PAGADO
            elif self.pagado < self.total:
                self.estado = EstadoPago.PENDIENTE
        else:
            credito_por_venta = self.total / 20
            puntos_actuales = self.cliente.puntos_acumulados
            puntos_acumulados = int(credito_por_venta) + int(puntos_actuales)
            Cliente.objects.filter(pk=self.cliente.pk).update(puntos_acumulados=puntos_acumulados)

        super(Venta, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        DetalleVenta.objects.filter(venta=self).delete()
        IngresoDinero.objects.filter(venta=self).delete()

        credito_por_venta = self.total / 20
        print(credito_por_venta)
        puntos_actuales = self.cliente.puntos_acumulados
        print(puntos_actuales)
        puntos_acumulados = int(puntos_actuales) - int(credito_por_venta)
        print(puntos_acumulados)
        Cliente.objects.filter(pk=self.cliente.pk).update(puntos_acumulados=puntos_acumulados)
        super(Venta, self).delete(*args, **kwargs)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicios.DetalleOrdenDeTrabajo', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(DetalleVenta, self).save(*args, **kwargs)
        detalle_ot = DetalleOrdenDeTrabajo.objects.get(id=self.servicio.id)
        detalle_ot.facturado = True
        detalle_ot.save(force_update=True)

    def delete(self, *args, **kwargs):
        detalle_ot = DetalleOrdenDeTrabajo.objects.get(id=self.servicio.id)
        detalle_ot.facturado = False
        detalle_ot.save(force_update=True)
        super(DetalleVenta, self).delete(*args, **kwargs)


class Pago(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    medio_de_pago = models.ForeignKey(FormaPago, on_delete=models.PROTECT)
    comprobante_numero = models.CharField(max_length=20, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    def save(self, *args, **kwargs):
        super(Pago, self).save(*args, **kwargs)
        if self.venta.factura:
            motivo = 'Venta: ' + str(self.venta.factura)
        else:
            motivo = 'Venta: ' + str(self.venta.id)

        self.venta.save()

        # FLUJO DE CAJA
        IngresoDinero.objects.create(
            categoria=get_categoria_flujo_venta(),
            sesion=self.venta.sesion,
            tipo=TipoFlujoCaja.INGRESO,
            motivo=motivo,
            monto=self.monto,
            fecha=self.venta.fecha,
            forma_pago=self.medio_de_pago,
            venta=self.venta
        )

    def delete(self, *args, **kwargs):
        venta = self.venta
        super(Pago, self).delete(*args, **kwargs)
        venta.save()

        # FLUJO DE CAJA
        RetiroDinero.objects.create(
            categoria=get_categoria_flujo_venta(),
            sesion=self.venta.sesion,
            tipo=TipoFlujoCaja.EGRESO,
            motivo='Por pago eliminado',
            monto=self.monto*(-1),
            fecha=date.today(),
            forma_pago=self.medio_de_pago,
            venta=self.venta
        )

    def __str__(self):
        if self.comprobante_numero:
            numero = str(self.comprobante_numero)
        else:
            numero = str(self.id)
        return 'Recibo nro. ' + numero


class CategoriaFlujoCaja(models.Model):
    nombre = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(choices=TipoFlujoCaja.TIPOS, max_length=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class FlujoCaja(models.Model):
    categoria = models.ForeignKey(CategoriaFlujoCaja, null=True, on_delete=models.PROTECT)
    sesion = models.ForeignKey(Sesion, null=True, on_delete=models.PROTECT)
    tipo = models.CharField(choices=TipoFlujoCaja.TIPOS, max_length=5)
    motivo = models.CharField(max_length=200, null=True, blank=True)
    monto = models.DecimalField(decimal_places=2, max_digits=14)
    fecha = models.DateTimeField(default=datetime.now)
    forma_pago = models.ForeignKey(FormaPago, null=True, verbose_name='Forma de Pago', on_delete=models.PROTECT)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.fecha.strftime('%d/%m/%Y - %H:%m'))


class RetiroDinero(FlujoCaja):
    class Meta:
        proxy = True
        verbose_name = "Retiro de Dinero"
        verbose_name_plural = "Retiros de Dinero"


class IngresoDinero(FlujoCaja):
    class Meta:
        proxy = True
        verbose_name = "Ingreso de Dinero"
        verbose_name_plural = "Ingresos de Dinero"


class MovimientoFlujoCaja(FlujoCaja):
    class Meta:
        proxy = True
        verbose_name_plural = 'Movimientos de Cajas'
        verbose_name = 'Movimiento de Caja'
