# Generated by Django 2.1.3 on 2018-12-19 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0004_auto_20181212_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='repeticiones',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
