# Generated by Django 2.1.3 on 2021-05-17 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruc', models.CharField(blank=True, max_length=20, null=True, verbose_name='RUC/CI Nro.')),
                ('box', models.CharField(blank=True, choices=[('box_1', 'Dr. Pablo Peña'), ('box_2', 'Dr. Marcelo Arango'), ('box_3', 'Dr. Luis Servin'), ('box_4', 'Lic. Laura Joy'), ('box_5', 'Lic. Cynthia Aquino'), ('box_6', 'Lic. Adriana Peralta'), ('box_19', 'Lic. Oriana Pereira'), ('box_18', 'Lic. Sol Jara'), ('box_7', 'Dra. Silvana Alfieri'), ('box_8', 'Dra. Tatiana Roy'), ('box_9', 'Dra. Andrea Ramirez'), ('box_10', 'Dra. Belen Gonzalez'), ('box_11', 'Dra. Belkis Vaccaro'), ('box_12', 'Dr. Juan Sebastian Pereira'), ('box_13', 'Lic. Alicia Yegros'), ('box_14', 'Lic. Bettina Madelaire'), ('box_15', 'Dr. Arias'), ('box_16', 'Dr. Giacomo Cruzants'), ('box_20', 'Dr. Alcaraz'), ('box_17', 'Dra. Fernandez')], max_length=6, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
