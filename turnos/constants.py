# -*- coding: utf-8 -*-


class BoxTurno:
    BOX_1 = 'box_1'
    BOX_2 = 'box_2'
    BOX_3 = 'box_3'
    BOX_4 = 'box_4'
    BOX_5 = 'box_5'
    BOX_6 = 'box_6'
    BOX_19 = 'box_19'
    BOX_18 = 'box_18'
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
    BOX_20 = 'box_20'
    BOX_17 = 'box_17'
    BOX_21 = 'box_21'

    BOXES = (
        (BOX_1, 'Dr. Pablo Peña'),
        (BOX_2, 'Dr. Marcelo Arango'),
        (BOX_3, 'Dr. Luis Servin'),
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
        (BOX_15, 'Dr. Arias'),
        (BOX_16, 'Dr. Giacomo Cruzants'),
        (BOX_20, 'Dr. Alcaraz'),
        (BOX_17, 'Dra. Fernandez'),
        (BOX_21, 'Lic. Mariela Ciccone'),
    )


class Especialidad:
    PROGRAMA_3R_MASQUELIER = 'M3R'
    NUTRICION = 'NUT'
    PROGRAMA_3R_SAGA = 'S3R'
    PEDIATRIA = 'PED'
    PSICOLOGIA = 'PSI'
    DR_ALCARAZ = 'ALC'
    DRA_FERNANDEZ = 'FER'

    ESPECIALIDADES = (
        (PROGRAMA_3R_MASQUELIER, 'Médicos - MASQUELIER'),
        (NUTRICION, 'Nutrición'),
        (PROGRAMA_3R_SAGA, 'Programa 3R - SAGA'),
        (PEDIATRIA, 'Pediatría'),
        (PSICOLOGIA, 'Psicología'),
        (DR_ALCARAZ, 'Dr. Alcaraz'),
        (DRA_FERNANDEZ, 'Dra. Fernandez')
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


