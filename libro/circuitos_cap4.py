# -*- coding: utf-8 -*-
"""Los diagramas de conexión del capítulo 4."""
import circuitos as C

LIENZO = 440
X_PLACA, Y_PLACA = 96, 26
LANE_GND = 244
LANE_IZQ = 24        # por fuera de los rotulos, que
                     # llegan hasta x = 94


def _riel(alto):
    return Y_PLACA + alto + 38


# =============================================================== 4.1
def lab_4_1():
    """Un solo puente entre dos pines: el circuito más corto del libro."""
    d = C.Dibujo("4.1")
    # La placa va corrida a la derecha y hacia abajo, que es lo que
    # esta figura necesita y ninguna otra: el rotulo "un puente" va a
    # la izquierda de los pines y se salia del lienzo, y las dos
    # lineas de la nota le caian encima al modulo.
    X, Y = X_PLACA + 56, Y_PLACA + 20
    cuerpo, pin, alto, cajas = C.placa_real(X, Y, {"GPIO25", "GPIO26"},
                                            gnd_lado="der")
    d.add(cuerpo, cajas)

    # GPIO25 y GPIO26 son vecinos en la columna izquierda: el puente
    # es un cable corto que no sale de ese lado de la placa.
    a, b = pin["GPIO25"], pin["GPIO26"]
    d.cable([a, (a[0] - 30, a[1]), (b[0] - 30, b[1]), b], C.SENAL)

    d.texto(a[0] - 38, (a[1] + b[1]) / 2 + 3, "un puente", 7.6, C.TEXTO,
            "end", "bold")
    d.texto(LIENZO / 2, 14,
            "no hace falta ningún sensor: la placa genera los pulsos "
            "y los cuenta",
            7, C.GRIS, "middle", inclinada=True)
    d.texto(LIENZO / 2, 28,
            "GPIO25 los produce, GPIO26 los recibe",
            7, C.GRIS, "middle", inclinada=True)

    return d, Y + alto + 24


# =============================================================== 4.4
def lab_4_4():
    """Sensor óptico de ranura, puente H y motor."""
    d = C.Dibujo("4.4")
    cuerpo, pin, alto, cajas = C.placa_real(
        X_PLACA, Y_PLACA,
        {"GPIO19", "GPIO18", "GPIO5", "GPIO17", "VIN", "GND"})
    d.add(cuerpo, cajas)
    RIEL = 370                 # mas abajo de lo habitual: el sensor es alto

    # ---- el puente H y el motor, arriba
    m, mp = C.modulo(300, 60, 74, 76, "L298N", ["ENA", "IN1", "IN2"],
                     color="#7A5230")
    d.add(m)
    motor, bornes = C.motor_cc(330, 165)
    d.add(motor)
    # Los dos bornes del motor estan a su izquierda: las salidas del
    # puente bajan por fuera del cuerpo del motor y entran de costado.
    # Bajar en linea recta hacia el borne de abajo obligaba al cable a
    # cruzar el motor entero por encima del simbolo.
    d.cable([(322, 136), (322, 142), (300, 142),
             (300, bornes["a"][1]), bornes["a"]], C.NARANJA)
    # La segunda salida rodea el motor por la derecha y por debajo:
    # bajando junto a la primera se cruzaban entre si.
    d.cable([(352, 136), (352, 144), (398, 144), (398, 212), (306, 212),
             (306, bornes["b"][1]), bornes["b"]], C.NARANJA)

    # cada mando con su propio carril, para que no se crucen entre si
    for nombre, pin_placa, lane in (("ENA", "GPIO19", 270),
                                    ("IN1", "GPIO18", 278),
                                    ("IN2", "GPIO5", 286)):
        d.cable([pin[pin_placa], (lane, pin[pin_placa][1]),
                 (lane, mp[nombre][1]), mp[nombre]], C.SENAL)

    # ---- el sensor óptico, abajo
    s, sp, cajas_s = C.disco_ranurado(310, 250)
    d.add(s, cajas_s)

    # la señal entra por encima del canal de masa, que empieza mas abajo
    d.cable([pin["GPIO17"], (266, pin["GPIO17"][1]), (266, 318),
             (sp["OUT"][0], 318), sp["OUT"]], C.VIOLETA)

    # la alimentacion rodea todo por debajo y sube por fuera
    d.cable([pin["VIN"], (LANE_IZQ, pin["VIN"][1]), (LANE_IZQ, 390), (392, 390),
             (392, 320), (sp["VCC"][0], 320), sp["VCC"]], C.ROJO)

    d.cable([sp["GND"], (sp["GND"][0], RIEL)], C.NEGRO)
    d.nodo(sp["GND"][0], RIEL, C.NEGRO)
    d.cable([(sp["GND"][0], RIEL), (LANE_GND, RIEL),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    d.texto(LIENZO / 2 + 40, 13,
            "la masa del puente H y la del ESP32 deben estar unidas",
            6.6, C.GRIS, "middle", inclinada=True)

    return d, 412


TODOS = {"lab_4_1": lab_4_1, "lab_4_4": lab_4_4}


def svg(nombre):
    d, alto = TODOS[nombre]()
    return d.svg(LIENZO, alto), len(d.cruces())
