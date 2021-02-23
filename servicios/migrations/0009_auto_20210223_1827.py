# Generated by Django 2.1.3 on 2021-02-23 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0008_auto_20210221_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordendetrabajo',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente', verbose_name='Paciente'),
        ),
        migrations.AlterField(
            model_name='ordendetrabajo',
            name='total',
            field=models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=15),
        ),
    ]
