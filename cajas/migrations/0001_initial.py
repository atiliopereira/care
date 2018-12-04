# Generated by Django 2.1.3 on 2018-12-03 16:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientes', '0001_initial'),
        ('servicios', '0003_auto_20181130_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('estado', models.BooleanField(choices=[(True, 'Abierta'), (False, 'Cerrada')], default=False)),
                ('disponible', models.IntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaFlujoCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('tipo', models.CharField(choices=[('IN', 'Ingreso'), ('EG', 'Egreso')], max_length=2)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=15)),
                ('orden_de_trabajo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='servicios.OrdenDeTrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='FlujoCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('IN', 'Ingreso'), ('EG', 'Egreso')], max_length=5)),
                ('motivo', models.CharField(blank=True, max_length=200, null=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=14)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cajas.CategoriaFlujoCaja')),
            ],
        ),
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15, unique=True)),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('nombre_comprobante', models.CharField(max_length=30)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('apertura', models.BooleanField(choices=[(True, 'Apertura'), (False, 'Cierre')], verbose_name='tipo')),
                ('efectivo', models.IntegerField(default=0)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cajas.Caja')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura', models.DateTimeField(default=datetime.datetime.now)),
                ('fecha_cierre', models.DateTimeField(null=True)),
                ('saldo_apertura', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('saldo_cierre', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cajas.Caja')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.CharField(max_length=50)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('condicion', models.CharField(choices=[('CO', 'Contado'), ('CR', 'Crédito')], default='CO', max_length=2, verbose_name='Condicion de Venta')),
                ('anulado', models.BooleanField(default=False, editable=False)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente')),
                ('forma_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cajas.FormaPago')),
                ('sesion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='cajas.Sesion')),
            ],
        ),
        migrations.AddField(
            model_name='flujocaja',
            name='forma_pago',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cajas.FormaPago', verbose_name='Forma de Pago'),
        ),
        migrations.AddField(
            model_name='flujocaja',
            name='sesion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cajas.Sesion'),
        ),
        migrations.AddField(
            model_name='flujocaja',
            name='venta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cajas.Venta'),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cajas.Venta'),
        ),
        migrations.CreateModel(
            name='AperturaCaja',
            fields=[
            ],
            options={
                'verbose_name': 'Apertura de Caja',
                'verbose_name_plural': 'Aperturas de Caja',
                'proxy': True,
                'indexes': [],
            },
            bases=('cajas.sesion',),
        ),
        migrations.CreateModel(
            name='CierreCaja',
            fields=[
            ],
            options={
                'verbose_name': 'Cierre de Caja',
                'verbose_name_plural': 'Cierres de Caja',
                'proxy': True,
                'indexes': [],
            },
            bases=('cajas.sesion',),
        ),
        migrations.CreateModel(
            name='IngresoDinero',
            fields=[
            ],
            options={
                'verbose_name': 'Ingreso de Dinero',
                'verbose_name_plural': 'Ingresos de Dinero',
                'proxy': True,
                'indexes': [],
            },
            bases=('cajas.flujocaja',),
        ),
        migrations.CreateModel(
            name='MovimientoFlujoCaja',
            fields=[
            ],
            options={
                'verbose_name': 'Movimiento de Caja',
                'verbose_name_plural': 'Movimientos de Cajas',
                'proxy': True,
                'indexes': [],
            },
            bases=('cajas.flujocaja',),
        ),
        migrations.CreateModel(
            name='RetiroDinero',
            fields=[
            ],
            options={
                'verbose_name': 'Retiro de Dinero',
                'verbose_name_plural': 'Retiros de Dinero',
                'proxy': True,
                'indexes': [],
            },
            bases=('cajas.flujocaja',),
        ),
    ]
