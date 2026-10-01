# -*- coding: utf-8 -*-
"""Los diagramas de conexión del capítulo 5."""
import circuitos as C

LIENZO = 440
X_PLACA, Y_PLACA = 96, 26
COL_A = 290
COL_B = 366
Y_NOTA = 13
LANE_GND = 244
LANE_IZQ = 24        # por fuera de los rotulos, que
                     # llegan hasta x = 94


def _riel(alto):
    return Y_PLACA + alto + 38


def _nota(d, texto):
    d.texto(LIENZO / 2 + 40, Y_NOTA, texto, 6.6, C.GRIS, "middle",
            inclinada=True)


def _alto_placa():
    _c, _p, alto, _cj = C.placa_real(X_PLACA, Y_PLACA, set())
    return alto


# =============================================================== 5.2
def lab_5_2():
    """Potenciómetro que gobierna el brillo de un LED."""
    d = C.Dibujo("5.2")
    cuerpo, pin, alto, cajas = C.placa_real(
        X_PLACA, Y_PLACA, {"GPIO34", "GPIO18", "3V3", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    # ---- el LED, arriba, gobernado por GPIO18
    y18 = pin["GPIO18"][1]
    r, r_izq, r_der = C.resistencia(288, y18, "330", rotulo="330 Ω")
    d.add(r)
    l, anodo, catodo = C.led(400, y18 + 26, rotular=False)
    d.add(l)
    d.cable([pin["GPIO18"], r_izq], C.SENAL)
    d.cable(C.hasta_el_anodo(r_der, anodo), C.SENAL)
    d.cable([catodo, (catodo[0], riel)], C.NEGRO)
    d.nodo(catodo[0], riel, C.NEGRO)

    # ---- el potenciómetro, abajo y despejado del LED
    px, py = 300, 196
    pot, ext1, cursor, ext3 = C.potenciometro(px, py)
    d.add(pot)

    # los dos extremos: uno a 3V3 y el otro a masa
    d.cable([pin["3V3"], (262, pin["3V3"][1]), (262, ext1[1] + 18),
             (ext1[0], ext1[1] + 18), ext1], C.ROJO)
    d.cable([ext3, (ext3[0] + 30, ext3[1]), (ext3[0] + 30, riel)], C.NEGRO)
    d.nodo(ext3[0] + 30, riel, C.NEGRO)

    # el cursor vuelve a GPIO34, que está en la columna opuesta: el
    # cable rodea la placa por debajo, como sobre la protoboard
    d.cable([cursor, (cursor[0], riel + 24), (LANE_IZQ, riel + 24),
             (LANE_IZQ, pin["GPIO34"][1]), pin["GPIO34"]], C.VIOLETA)

    d.cable([(catodo[0], riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "GPIO34 pertenece al ADC1 y está en la otra columna: el cable "
             "rodea la placa")
    return d, riel + 60


# =============================================================== 5.3
def lab_5_3():
    """Servomotor SG90."""
    d = C.Dibujo("5.3")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO4", "VIN", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    y4 = pin["GPIO4"][1]
    sv, cable = C.servomotor(360, y4 - 22)
    d.add(sv)
    d.texto(391, y4 + 54, "el aspa gira 180°", 6.6, C.GRIS,
            "middle", inclinada=True)

    # Cada cable del servo sigue su color: naranja la señal, rojo la
    # alimentación, marrón la masa. Son los mismos tres colores que
    # el estudiante tiene en la mano.
    d.cable([pin["GPIO4"], (290, y4), (290, cable["naranja"][1]),
             cable["naranja"]], C.NARANJA)
    d.cable([pin["VIN"], (LANE_IZQ, pin["VIN"][1]), (LANE_IZQ, riel + 22),
             (336, riel + 22), (336, cable["rojo"][1]),
             cable["rojo"]], C.ROJO)
    d.cable([cable["marron"], (282, cable["marron"][1]), (282, riel)],
            C.NEGRO)
    d.nodo(282, riel, C.NEGRO)
    d.cable([(282, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "el servo se alimenta de VIN: con 3V3 no tiene par y reinicia "
             "la placa")
    return d, riel + 58


# =============================================================== 5.5
def lab_5_5():
    """Buzzer pasivo."""
    d = C.Dibujo("5.5")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA, {"GPIO5", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    y5 = pin["GPIO5"][1]
    zx, zy = COL_A + 30, y5
    d.add('<circle cx="%g" cy="%g" r="22" fill="#3A3F46" stroke="%s" '
          'stroke-width="1"/>' % (zx, zy, C.PLACA_BORDE))
    d.add('<circle cx="%g" cy="%g" r="5" fill="#20242A"/>' % (zx, zy))
    d.texto(zx - 10, zy - 4, "+", 11, "#E8EDF2", "middle", "bold",
            serigrafia=True)
    d.texto(zx, zy - 31, "buzzer pasivo", 7.4, C.TEXTO, "middle")
    mas, menos = (zx - 9, zy + 22), (zx + 9, zy + 22)

    d.cable([pin["GPIO5"], (mas[0] - 20, y5), (mas[0] - 20, mas[1] + 10),
             (mas[0], mas[1] + 10), mas], C.SENAL)
    d.cable([menos, (menos[0], riel)], C.NEGRO)
    d.nodo(menos[0], riel, C.NEGRO)
    d.cable([(menos[0], riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "el activo trae su propio oscilador y no atiende la frecuencia")
    return d, riel + 30


TODOS = {"lab_5_2": lab_5_2, "lab_5_3": lab_5_3, "lab_5_5": lab_5_5}


def svg(nombre):
    d, alto = TODOS[nombre]()
    return d.svg(LIENZO, alto), len(d.cruces())
