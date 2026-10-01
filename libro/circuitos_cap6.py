# -*- coding: utf-8 -*-
"""Los diagramas de conexión del capítulo 6."""
import circuitos as C

LIENZO = 440
X_PLACA, Y_PLACA = 96, 26
LANE_GND = 244


def _riel(alto):
    return Y_PLACA + alto + 38


def _nota(d, texto):
    d.texto(LIENZO / 2 + 40, 13, texto, 6.6, C.GRIS, "middle", inclinada=True)


# =============================================================== 6.1
def lab_6_1():
    """La pantalla OLED colgada del bus I2C."""
    d = C.Dibujo("6.1")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO22", "GPIO21", "3V3", "GND"})
    d.add(cuerpo, cajas)

    p, op, cajas_oled = C.oled(300, 150)
    d.add(p, cajas_oled)

    # Las dos señales del bus salen de pines altos y la pantalla los
    # espera abajo: se llevan por encima de la pantalla y bajan por
    # fuera. Las dos alimentaciones, que salen de pines bajos, van
    # por debajo. Asi ninguno de los cuatro cables cruza a otro.
    d.cable([pin["GPIO22"], (432, pin["GPIO22"][1]),
             (432, 264), (op["SCL"][0], 264), op["SCL"]], C.SENAL)
    d.cable([pin["GPIO21"], (420, pin["GPIO21"][1]),
             (420, 250), (op["SDA"][0], 250), op["SDA"]], C.NARANJA)
    d.cable([pin["GND"], (250, pin["GND"][1]), (250, 238),
             (op["GND"][0], 238), op["GND"]], C.NEGRO)
    d.cable([pin["3V3"], (262, pin["3V3"][1]), (262, 278),
             (op["VCC"][0], 278), op["VCC"]], C.ROJO)

    _nota(d, "GPIO22 es SCL y GPIO21 es SDA: los dos llegan a todos los "
             "dispositivos del bus")
    return d, 306


# =============================================================== 6.4
def lab_6_4():
    """Transmisor de presión con HX710B."""
    d = C.Dibujo("6.4")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO16", "GPIO4", "3V3", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    m, mp = C.modulo(312, 96, 84, 84, "HX710B", ["VCC", "OUT", "SCK", "GND"],
                     color="#3A5F7D")
    d.add(m)
    d.texto(354, 194, "transmisor de presión", 6.6, C.GRIS, "middle",
            inclinada=True)

    # La masa se traza primero: los saltos se dibujan sobre el cable
    # posterior, y el riel tiene que quedar entero.
    d.cable([mp["GND"], (308, mp["GND"][1]), (308, riel)], C.NEGRO)
    d.nodo(308, riel, C.NEGRO)
    d.cable([(308, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    # Los dos carriles de señal van ordenados: el que sale del pin
    # mas alto usa el carril mas cerca de la placa. Asi no se cruzan
    # entre si. La alimentacion queda por fuera de los dos.
    d.cable([pin["GPIO16"], (272, pin["GPIO16"][1]), (272, mp["OUT"][1]),
             mp["OUT"]], C.VIOLETA)
    d.cable([pin["GPIO4"], (286, pin["GPIO4"][1]), (286, mp["SCK"][1]),
             mp["SCK"]], C.NARANJA)
    d.cable([pin["3V3"], (296, pin["3V3"][1]), (296, mp["VCC"][1]),
             mp["VCC"]], C.ROJO)

    _nota(d, "OUT lleva el dato y SCK el reloj: la placa marca el ritmo")
    return d, riel + 30


# =============================================================== 6.5
def lab_6_5():
    """Medidor PZEM-004T por puerto serie."""
    d = C.Dibujo("6.5")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO16", "GPIO17", "3V3", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    m, mp = C.modulo(312, 92, 92, 88, "PZEM-004T",
                     ["5V", "RX", "TX", "GND"], color="#7A3040")
    d.add(m)
    d.texto(358, 196, "medidor de energía", 6.6, C.GRIS, "middle",
            inclinada=True)
    d.texto(358, 206, "220 V por el otro lado", 6.4, C.ROJO, "middle",
            inclinada=True)

    # La masa se traza primero: los saltos se dibujan sobre el cable
    # posterior, y el riel tiene que quedar entero.
    d.cable([mp["GND"], (308, mp["GND"][1]), (308, riel)], C.NEGRO)
    d.nodo(308, riel, C.NEGRO)
    d.cable([(308, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    # Cruzado: lo que la placa transmite entra por RX del modulo.
    # Los carriles van ordenados por altura del pin de origen.
    d.cable([pin["GPIO17"], (272, pin["GPIO17"][1]), (272, mp["RX"][1]),
             mp["RX"]], C.NARANJA)
    d.cable([pin["GPIO16"], (286, pin["GPIO16"][1]), (286, mp["TX"][1]),
             mp["TX"]], C.VIOLETA)
    d.cable([pin["3V3"], (296, pin["3V3"][1]), (296, mp["5V"][1]),
             mp["5V"]], C.ROJO)

    _nota(d, "TX de la placa va a RX del módulo, y al revés: siempre cruzado")
    return d, riel + 40


TODOS = {"lab_6_1": lab_6_1, "lab_6_4": lab_6_4, "lab_6_5": lab_6_5}


def svg(nombre):
    d, alto = TODOS[nombre]()
    return d.svg(LIENZO, alto), len(d.cruces())
