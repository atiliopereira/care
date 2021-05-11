# Generated by Django 2.1.3 on 2021-02-23 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0011_auto_20210223_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='box',
            field=models.CharField(blank=True, choices=[('box_1', 'Dr. Pablo Peña'), ('box_2', 'Dr. Marcelo Arango'), ('box_3', 'Dr. Luis Servin'), ('box_4', 'Lic. Laura Joy'), ('box_5', 'Lic. Cynthia Aquino'), ('box_6', 'Lic. Adriana Peralta'), ('box_19', 'Lic. Oriana Pereira'), ('box_7', 'Dra. Silvana Alfieri'), ('box_8', 'Dra. Tatiana Roy'), ('box_9', 'Dra. Andrea Ramirez'), ('box_10', 'Dra. Belen Gonzalez'), ('box_11', 'Dra. Belkis Vaccaro'), ('box_12', 'Dr. Juan Sebastian Pereira'), ('box_13', 'Lic. Alicia Yegros'), ('box_14', 'Lic. Bettina Madelaire'), ('box_15', 'Dr. Arias'), ('box_16', 'Dr. Giacomo Cruzants'), ('box_17', 'Dra. Fernandez'), ('box_18', 'Lic. Sol Jara'), ('box_20', 'Dr. Alcaraz')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='especialidad',
            field=models.CharField(choices=[('M3R', 'Médicos - MASQUELIER'), ('NUT', 'Nutrición'), ('S3R', 'Programa 3R - SAGA'), ('PED', 'Pediatría'), ('PSI', 'Psicología'), ('ALC', 'Dr. Alcaraz'), ('FER', 'Dra. Fernandez')], max_length=3),
        ),
    ]