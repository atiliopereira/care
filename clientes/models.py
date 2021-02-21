# -*- coding: utf-8 -*-
from datetime import date

from django.db import models

from clientes.constants import Parto, LactanciaMaterna, Antibioticos, VaDeCuerpo


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    documento = models.CharField(max_length=20, null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")
    nacimiento = models.DateField(blank=True, null=True)
    parto = models.CharField(max_length=3, choices=Parto.TIPOS, default=Parto.NORMAL)
    lactancia_materna = models.CharField(max_length=4, choices=LactanciaMaterna.DURACIONES, default=LactanciaMaterna.LT6M)
    antibioticos_en_infancia = models.CharField(max_length=2, choices=Antibioticos.OPCIONES, default=Antibioticos.NO_RECUEDA)

    #COMORBILIDADES
    hipertension_arterial = models.BooleanField(default=False, verbose_name='Hipertensión arterial')
    diabetes_mellitus_tipo_2 = models.BooleanField(default=False)
    dislipidemia = models.BooleanField(default=False)
    hipotiroidismo = models.BooleanField(default=False)
    hipertiroidismo = models.BooleanField(default=False)
    tiroiditis = models.BooleanField(default=False)
    rinitis_alergica = models.BooleanField(default=False)
    asma = models.BooleanField(default=False)
    gastritis = models.BooleanField(default=False)
    sindrome_del_intestino_irritable = models.BooleanField(default=False)
    celiaquia = models.BooleanField(default=False)
    transtorno_de_ansiedad = models.BooleanField(default=False)
    sindrome_de_panico = models.BooleanField(default=False, verbose_name='Síndrome de pánico')
    depresion = models.BooleanField(default=False, verbose_name='Depresión')
    anemia = models.BooleanField(default=False)
    sindrome_de_ovario_poliquistico = models.BooleanField(default=False, verbose_name='Síndrome de ovario poliquístico')
    otras_comorbolidades = models.CharField(max_length=250, blank=True, null=True, help_text="Especificar o comentarios")

    #CIRUGIAS
    adenoides = models.BooleanField(default=False)
    amigdalectomia = models.BooleanField(default=False)
    apendicectomia = models.BooleanField(default=False)
    histerectomia = models.BooleanField(default=False)
    hemorroides = models.BooleanField(default=False)
    colecistectomia = models.BooleanField(default=False)
    otras_cirugias = models.CharField(max_length=250, blank=True, null=True, help_text="Especificar o comentarios")

    #MEDICAMENTOS
    antibioticos = models.BooleanField(default=False)
    corticoides = models.BooleanField(default=False)
    antidepresivos = models.BooleanField(default=False)
    anticonceptivos = models.BooleanField(default=False)
    inhibidor_de_bomba_de_protones = models.BooleanField(default=False)
    metformina = models.BooleanField(default=False)
    quimioterapia = models.BooleanField(default=False)
    analgesicos = models.BooleanField(default=False)
    otros_medicamentos = models.CharField(max_length=250, blank=True, null=True, help_text="Especificar o comentarios")

    #ACTUALMENTE PRESENTA
    ## SISTEMA NERVIOSO
    cefalea = models.BooleanField(default=False)
    cansancio_o_fatiga = models.BooleanField(default=False)
    insomnio = models.BooleanField(default=False)
    se_despierta_por_las_noches = models.BooleanField(default=False)
    bruxismo = models.BooleanField(default=False)
    perdida_de_memoria = models.BooleanField(default=False)
    falta_de_concentracion = models.BooleanField(default=False)
    mareos = models.BooleanField(default=False)
    irritabilidad = models.BooleanField(default=False)
    ansiedad = models.BooleanField(default=False)
    abombamiento = models.BooleanField(default=False)
    ##APARATO RESPIRATORIO
    congestion_nasal = models.BooleanField(default=False)
    estornudos = models.BooleanField(default=False)
    tos_cronica = models.BooleanField(default=False)
    sibilancias = models.BooleanField(default=False)
    frecuente_sensacion_de_limpiar_la_garganta = models.BooleanField(default=False)
    ##APARATO CIRCULATORIO
    retencion_de_liquidos = models.BooleanField(default=False)
    palpitaciones = models.BooleanField(default=False)
    varices = models.BooleanField(default=False)
    manos_y_pies_frias = models.BooleanField(default=False)
    ##APARATO DIGESTIVO
    aftas_en_la_boca = models.BooleanField(default=False)
    halitosis = models.BooleanField(default=False)
    acides_estomacal = models.BooleanField(default=False)
    nauseas = models.BooleanField(default=False)
    vomitos = models.BooleanField(default=False)
    dolor_abdominal = models.BooleanField(default=False)
    distencion_abdominal = models.BooleanField(default=False)
    reflujo = models.BooleanField(default=False)
    diarreas = models.BooleanField(default=False)
    estrenimiento = models.BooleanField(default=False)

    #Materia fecal
    va_de_cuerpo_cada = models.CharField(max_length=4, choices=VaDeCuerpo.FRECUENCIA, default=VaDeCuerpo.UNA_VEZ_AL_DIA)
    forma_de_materia_fecal = models.SmallIntegerField(default=1, help_text="Escala de Bristol")

    #APARATO TEGUMENTARIO
    alergias_en_el_rostro = models.BooleanField(default=False)
    alergias_en_la_piel = models.BooleanField(default=False)
    acne = models.BooleanField(default=False)

    #APARATO OSTEOMUSCULAR
    dolor_articular = models.BooleanField(default=False)

    bio_resonancia_cuantica = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
            return f'{self.nombre}'

    @property
    def edad(self):
        today = date.today()
        return today.year - self.nacimiento.year - (
                (today.month, today.day) < (self.nacimiento.month, self.nacimiento.day))


class DatoFacturacion(models.Model):
    class Meta:
        verbose_name = "Dato de facturación"
        verbose_name_plural = 'Datos de facturación'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    razon_social = models.CharField(max_length=100, verbose_name="Razón Social")
    ruc = models.CharField(max_length=30, verbose_name="RUC")

    def __str__(self):
        return self.razon_social + " - " + self.ruc
