# Generated by Django 2.1.3 on 2021-01-18 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_auto_20210118_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='ruc',
        ),
        migrations.AddField(
            model_name='cliente',
            name='documento',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]