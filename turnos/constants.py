# -*- coding: utf-8 -*-
import math


class BoxTurno:

    BOX_27 = 'box_27'
    BOX_28 = 'box_28'
    BOX_29 = 'box_29'
    BOX_30 = 'box_30'
    BOX_31 = 'box_31'

    BOXES = (

        (BOX_27, 'Extra 1'),
        (BOX_28, 'Extra 2'),
        (BOX_29, 'Extra 3'),
        (BOX_30, 'Extra 4'),
        (BOX_31, 'Extra 5'),
    )


class Especialidad:

    EXTRA = 'EXT'

    ESPECIALIDADES = (

        (EXTRA, 'Extra'),
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
        Especialidad.EXTRA: (BoxTurno.BOX_27, BoxTurno.BOX_28, BoxTurno.BOX_29, BoxTurno.BOX_30, BoxTurno.BOX_31),
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


