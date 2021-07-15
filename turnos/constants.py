# -*- coding: utf-8 -*-
import math


class BoxTurno:
    BOX_1 = 'box_1'
    BOX_2 = 'box_2'
    BOX_3 = 'box_3'
    BOX_4 = 'box_4'
    BOX_5 = 'box_5'
    BOX_6 = 'box_6'
    BOX_7 = 'box_7'
    BOX_8 = 'box_8'
    BOX_9 = 'box_9'
    BOX_10 = 'box_10'
    BOX_11 = 'box_11'
    BOX_12 = 'box_12'
    BOX_13 = 'box_13'
    BOX_14 = 'box_14'
    BOX_15 = 'box_15'
    BOX_16 = 'box_16'
    BOX_17 = 'box_17'
    BOX_18 = 'box_18'
    BOX_19 = 'box_19'
    BOX_20 = 'box_20'
    BOX_21 = 'box_21'

    BOX_22 = 'box_22'
    BOX_23 = 'box_23'
    BOX_24 = 'box_24'
    BOX_25 = 'box_25'
    BOX_26 = 'box_26'

    BOX_27 = 'box_27'
    BOX_28 = 'box_28'
    BOX_29 = 'box_29'
    BOX_30 = 'box_30'
    BOX_31 = 'box_31'

    BOXES = (
        (BOX_1, 'Dr. Pablo Peña'),
        (BOX_2, 'Dr. Marcelo Arango'),
        (BOX_3, 'Dr. Luis Servin'),
        (BOX_15, 'Dr. Arias'),
        (BOX_16, 'Dr. Giacomo Cruzants'),
        (BOX_4, 'Lic. Laura Joy'),
        (BOX_5, 'Lic. Cynthia Aquino'),
        (BOX_6, 'Lic. Adriana Peralta'),
        (BOX_19, 'Lic. Oriana Pereira'),
        (BOX_18, 'Lic. Sol Jara'),
        (BOX_7, 'Dra. Silvana Alfieri'),
        (BOX_8, 'Dra. Tatiana Roy'),
        (BOX_9, 'Dra. Andrea Ramirez'),
        (BOX_10, 'Dra. Belén Gonzalez'),
        (BOX_11, 'Dra. Belkis Vaccaro'),
        (BOX_12, 'Dr. Juan Sebastian Pereira'),
        (BOX_13, 'Lic. Alicia Yegros'),
        (BOX_14, 'Lic. Bettina Madelaire'),
        (BOX_21, 'Lic. Mariela Ciccone'),
        (BOX_20, 'Dr. Alcaraz'),
        (BOX_17, 'Dra. Fernandez'),
        (BOX_22, 'Suero 1'),
        (BOX_23, 'Suero 2'),
        (BOX_24, 'Suero 3'),
        (BOX_25, 'Suero Domicilio'),
        (BOX_26, 'Vacunación'),
        (BOX_27, 'Extra 1'),
        (BOX_28, 'Extra 2'),
        (BOX_29, 'Extra 3'),
        (BOX_30, 'Extra 4'),
        (BOX_31, 'Extra 5'),
    )


class Especialidad:
    PROGRAMA_3R_MASQUELIER = 'M3R'
    NUTRICION = 'NUT'
    PROGRAMA_3R_SAGA = 'S3R'
    PEDIATRIA = 'PED'
    PSICOLOGIA = 'PSI'
    DR_ALCARAZ = 'ALC'
    DRA_FERNANDEZ = 'FER'
    ENFERMERIA = 'ENF'
    EXTRA = 'EXT'

    ESPECIALIDADES = (
        (PROGRAMA_3R_MASQUELIER, 'Médicos - MASQUELIER'),
        (NUTRICION, 'Nutrición'),
        (PROGRAMA_3R_SAGA, 'Programa 3R - SAGA'),
        (PEDIATRIA, 'Pediatría'),
        (PSICOLOGIA, 'Psicología'),
        (DR_ALCARAZ, 'Dr. Alcaraz'),
        (DRA_FERNANDEZ, 'Dra. Fernandez'),
        (ENFERMERIA, 'Enfermería'),
        (EXTRA, 'Extra')
    )


class TipoDeTurno:
    PRIMERA_VEZ = 'pv'
    CONTROL = 'co'

    TIPOS = (
        (PRIMERA_VEZ, 'Primera'),
        (CONTROL, 'Control'),
    )


class OpcionesCancelados:
    TODOS = ''
    CANCELADOS = 'si'
    NO_CANCELADOS = 'no'

    OPCIONES = (
        (NO_CANCELADOS, 'No cancelados'),
        (TODOS, 'Todos'),
        (CANCELADOS, 'Cancelados'),
    )


BOXES_POR_ESPECIALIDAD = {
        Especialidad.PROGRAMA_3R_MASQUELIER: (BoxTurno.BOX_1, BoxTurno.BOX_2, BoxTurno.BOX_3, BoxTurno.BOX_15, BoxTurno.BOX_16),
        Especialidad.NUTRICION: (BoxTurno.BOX_4, BoxTurno.BOX_5, BoxTurno.BOX_6, BoxTurno.BOX_19, BoxTurno.BOX_18),
        Especialidad.PROGRAMA_3R_SAGA: (BoxTurno.BOX_7, BoxTurno.BOX_8),
        Especialidad.PEDIATRIA: (BoxTurno.BOX_9, BoxTurno.BOX_10, BoxTurno.BOX_11, BoxTurno.BOX_12),
        Especialidad.PSICOLOGIA: (BoxTurno.BOX_13, BoxTurno.BOX_14, BoxTurno.BOX_21),
        Especialidad.ENFERMERIA: (BoxTurno.BOX_22, BoxTurno.BOX_23, BoxTurno.BOX_24, BoxTurno.BOX_25, BoxTurno.BOX_26),
        Especialidad.EXTRA: (BoxTurno.BOX_27, BoxTurno.BOX_28, BoxTurno.BOX_29, BoxTurno.BOX_30, BoxTurno.BOX_31)
}


def crear_horarios(inicio, fin, intervalo):
    """
    Crea rango de horarios en formato: ("08:00", "08:30", ...)
    - inicio: primer horario
    - fin: fin del último horario
    - intervalo: intervalo de tiempo para dividir los horarios.

    """
    time_to_minutes = lambda time: time.hour * 60 + time.minute
    return [f"{math.floor(h / 60):02d}:{(h % 60):02d}" for h in
            range(time_to_minutes(inicio), time_to_minutes(fin), intervalo)]


