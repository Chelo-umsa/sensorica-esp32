# -*- coding: utf-8 -*-
"""Los diagramas de conexión del capítulo 3.

Todas las entradas analógicas de este capítulo van al ADC1, y el ADC1
vive en la columna izquierda de la placa. Por eso en los cuatro
diagramas el cable de señal rodea la placa por abajo: no es una
elección del dibujo, es dónde están los pines.
"""
import circuitos as C

LIENZO = 440
X_PLACA, Y_PLACA = 96, 26
LANE_GND = 244
LANE_IZQ = 24        # por fuera de los rotulos, que
                     # llegan hasta x = 94


def _riel(alto):
    return Y_PLACA + alto + 38


Y_SENAL = 14          # el carril por donde la señal cruza por arriba


def _al_adc(d, desde, pin_destino, lane_x):
    """Lleva la señal hasta un pin del ADC1, que está en la otra columna.

    Pasa por ENCIMA de la placa y no por debajo. Por debajo hay que
    cruzar el riel de masa y el cable de alimentación, y el dibujo se
    llena de saltos; por arriba no hay nada.
    """
    # El carril sube por la IZQUIERDA del componente. A la derecha
    # bajan las masas, y cualquier carril de ese lado las cruza.
    d.cable([desde, (desde[0], desde[1] + 10), (lane_x, desde[1] + 10),
             (lane_x, Y_SENAL), (LANE_IZQ, Y_SENAL),
             (LANE_IZQ, pin_destino[1]), pin_destino], C.VIOLETA)


# =============================================================== 3.1
def lab_3_1():
    """Potenciómetro leído por el ADC1."""
    d = C.Dibujo("3.1")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO34", "3V3", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    px, py = 320, 150
    pot, ext1, cursor, ext3 = C.potenciometro(px, py)
    d.add(pot)

    d.cable([ext3, (ext3[0] + 34, ext3[1]), (ext3[0] + 34, riel)], C.NEGRO)
    d.nodo(ext3[0] + 34, riel, C.NEGRO)
    d.cable([(ext3[0] + 34, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    d.cable([pin["3V3"], (268, pin["3V3"][1]), (268, ext1[1] + 16),
             (ext1[0], ext1[1] + 16), ext1], C.ROJO)
    _al_adc(d, cursor, pin["GPIO34"], 252)
    return d, riel + 24


# =============================================================== 3.2
def lab_3_2():
    """Señal de 5 V acondicionada con un divisor de tensión."""
    d = C.Dibujo("3.2")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO35", "VIN", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    px, py = 292, 108
    pot, ext1, cursor, ext3 = C.potenciometro(px, py, "10 kΩ")
    d.add(pot)

    # el divisor: R1 en serie desde el cursor, R2 a masa
    r1, r1a, r1b = C.resistencia(346, cursor[1] + 20, "10k", rotulo="R1 10 kΩ")
    d.add(r1)
    # mas a la izquierda de lo que pediria el dibujo: su rotulo va a
    # la derecha y con R2 pegada al borde quedaba cortado
    r2, r2a, r2b = C.resistencia(386, 228, "15k", horizontal=False,
                                 rotulo="R2 15 kΩ")
    d.add(r2)

    # VIN esta en la columna izquierda: el cable rodea la placa por
    # abajo y sube por fuera de los rotulos.
    d.cable([ext1, (ext1[0], riel + 22), (LANE_IZQ, riel + 22),
             (LANE_IZQ, pin["VIN"][1]), pin["VIN"]], C.ROJO)
    d.cable([ext3, (ext3[0] + 22, ext3[1]), (ext3[0] + 22, riel)], C.NEGRO)
    d.nodo(ext3[0] + 22, riel, C.NEGRO)

    d.cable([cursor, (cursor[0], cursor[1] + 20), r1a], C.SENAL)
    d.cable([r1b, (r2a[0], r1b[1]), r2a], C.SENAL)
    d.cable([r2b, (r2b[0], riel)], C.NEGRO)
    d.nodo(r2b[0], riel, C.NEGRO)

    # el punto medio del divisor es lo que entra al conversor
    d.nodo(r2a[0], r2a[1], C.SENAL)
    _al_adc(d, (r2a[0], r2a[1]), pin["GPIO35"], 256)

    d.cable([(ext3[0] + 22, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)
    return d, riel + 24


# =============================================================== 3.3
def lab_3_3():
    """LM35, sensor lineal alimentado con 5 V."""
    d = C.Dibujo("3.3")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO32", "VIN", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    sx, sy = 330, 120
    s, patas = C.to92(sx, sy, "LM35")
    d.add(s)
    izq, centro, der = patas

    d.cable([pin["VIN"], (LANE_IZQ, pin["VIN"][1]), (LANE_IZQ, riel + 22),
             (izq[0], riel + 22), izq], C.ROJO)
    d.cable([der, (der[0] + 26, der[1]), (der[0] + 26, riel)], C.NEGRO)
    d.nodo(der[0] + 26, riel, C.NEGRO)
    d.cable([(der[0] + 26, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _al_adc(d, centro, pin["GPIO32"], 252)
    return d, riel + 24


# =============================================================== 3.4
def lab_3_4():
    """Termistor NTC de 100 kΩ, con su resistencia fija y el condensador."""
    d = C.Dibujo("3.4")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO33", "3V3", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    # R fija arriba, NTC abajo: el punto medio es la señal
    r, ra, rb = C.resistencia(286, 92, "100k", horizontal=False,
                              rotulo="R fija 100 kΩ")
    d.add(r)
    t, ta, tb = C.termistor(292, 190)
    d.add(t)

    NODO = (292, 148)
    d.cable([pin["3V3"], (238, pin["3V3"][1]), (238, 74), (ra[0], 74), ra],
            C.ROJO)
    d.cable([rb, (rb[0], NODO[1]), NODO], C.VIOLETA)
    # baja por fuera del termistor: recto desde el nodo, el cable le
    # pasaba por encima de la perla
    d.cable([NODO, (270, NODO[1]), (270, ta[1]), ta], C.VIOLETA)
    d.nodo(NODO[0], NODO[1], C.VIOLETA)
    d.cable([tb, (tb[0] + 30, tb[1]), (tb[0] + 30, riel)], C.NEGRO)
    d.nodo(tb[0] + 30, riel, C.NEGRO)

    # el condensador, en paralelo con el termistor
    c, ca, cb = C.condensador(378, 150)
    d.add(c)
    d.cable([(NODO[0], NODO[1]), (ca[0], NODO[1]), (ca[0], ca[1] - 26), ca],
            C.VIOLETA)
    d.cable([cb, (cb[0], riel)], C.NEGRO)
    d.nodo(cb[0], riel, C.NEGRO)

    _al_adc(d, NODO, pin["GPIO33"], 252)
    d.cable([(tb[0] + 30, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)
    return d, riel + 24


TODOS = {"lab_3_1": lab_3_1, "lab_3_2": lab_3_2,
         "lab_3_3": lab_3_3, "lab_3_4": lab_3_4}


def svg(nombre):
    d, alto = TODOS[nombre]()
    return d.svg(LIENZO, alto), len(d.cruces())
