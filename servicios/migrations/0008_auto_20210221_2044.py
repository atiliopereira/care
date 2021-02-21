# Generated by Django 2.1.3 on 2021-02-21 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0007_auto_20210118_0954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detalleordendetrabajo',
            options={'verbose_name': 'Servicio realizado', 'verbose_name_plural': 'Servicios realizados'},
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='altura',
            field=models.PositiveIntegerField(blank=True, help_text='Altura en cm', null=True),
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='antecedentes_de_la_enfermedad_actual',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='estudios',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='peso',
            field=models.FloatField(blank=True, help_text='Peso en kg', null=True),
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='presion_arterial',
            field=models.FloatField(blank=True, help_text='Peso en kg', null=True),
        ),
    ]
