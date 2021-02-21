# -*- coding: utf-8 -*-


class Parto:
    CESAREA = 'CES'
    NORMAL = 'NOR'

    TIPOS = (
        (CESAREA, 'Cesárea'),
        (NORMAL, 'Normal')
    )


class LactanciaMaterna:
    LT6M = 'LT6M'
    LT1Y = 'LT1Y'
    LT2Y = 'LT2Y'
    MT2Y = 'MT2Y'

    DURACIONES = (
        (LT6M, 'Menos de 6 meses'),
        (LT1Y, 'Menos de 1 año'),
        (LT2Y, 'Menos de 2 años'),
        (MT2Y, 'Más de 2 años')
    )


class Antibioticos:
    SI = 'SI'
    NO = 'NO'
    NO_RECUEDA = 'NR'

    OPCIONES = (
        (SI, 'Sí'),
        (NO, 'No'),
        (NO_RECUEDA, 'No recuerda')
    )


class VaDeCuerpo:
    CUATRO_VECES_AL_DIA = '4VAD'
    DOS_VECES_AL_DIA = '2VAD'
    UNA_VEZ_AL_DIA = '1VAD'
    DIA_DE_POR_MEDIO = 'DDPM'
    DOS_VECES_POR_SEMANA = '2VPS'
    UNA_VEZ_POR_SEMANA = '1VPS'
    CADA_QUINCE_DIAS = 'C15D'

    FRECUENCIA = (
        (CUATRO_VECES_AL_DIA, '4 veces al día'),
        (DOS_VECES_AL_DIA, '2 veces al día'),
        (UNA_VEZ_AL_DIA, '1 vez al día'),
        (DIA_DE_POR_MEDIO, 'día de por medio'),
        (DOS_VECES_POR_SEMANA, '2 veces por semana'),
        (UNA_VEZ_POR_SEMANA, '1 vez por semana'),
        (CADA_QUINCE_DIAS, 'cada 15 días')
    )
