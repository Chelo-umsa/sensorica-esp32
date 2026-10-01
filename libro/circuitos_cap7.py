# -*- coding: utf-8 -*-
"""Los diagramas de conexión del capítulo 7."""
import circuitos as C

LIENZO = 440
X_PLACA, Y_PLACA = 96, 26
LANE_GND = 244
LANE_IZQ = 24        # por fuera de los rotulos, que
                     # llegan hasta x = 94


def _riel(alto):
    return Y_PLACA + alto + 38


def _nota(d, texto, y=13):
    d.texto(LIENZO / 2 + 40, y, texto, 6.6, C.GRIS, "middle", inclinada=True)


# =============================================================== 7.2
def lab_7_2():
    """DHT11 para los laboratorios de servidor web y de MQTT."""
    d = C.Dibujo("7.2")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO14", "3V3", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    sx, sy = 316, 96
    m, mp, cajas_dht = C.dht11(sx, sy)
    d.add(m, cajas_dht)

    y14 = pin["GPIO14"][1]

    # La masa se traza PRIMERO. Los saltos se dibujan sobre el cable
    # que se traza después, y conviene que el riel de masa quede
    # entero: es la referencia de todo el montaje y cortarlo con
    # puentecitos lo vuelve difícil de seguir.
    d.cable([mp["GND"], (mp["GND"][0] + 26, mp["GND"][1]),
             (mp["GND"][0] + 26, riel)], C.NEGRO)
    d.nodo(mp["GND"][0] + 26, riel, C.NEGRO)
    d.cable([(mp["GND"][0] + 26, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    # GPIO14 está en la columna izquierda: el cable rodea la placa
    d.cable([pin["GPIO14"], (LANE_IZQ, y14), (LANE_IZQ, riel + 24),
             (mp["DATA"][0], riel + 24), mp["DATA"]], C.SENAL)
    d.cable([pin["3V3"], (280, pin["3V3"][1]), (280, mp["VCC"][1] + 14),
             (mp["VCC"][0], mp["VCC"][1] + 14), mp["VCC"]], C.ROJO)

    _nota(d, "es el mismo montaje del laboratorio 6.3: no hay que recablear")
    return d, riel + 46


# =============================================================== 7.4
def lab_7_4():
    """Dos placas enlazadas por ESP-NOW, una con pulsador y otra con zumbador."""
    d = C.Dibujo("7.4")
    # La separacion es la justa para que quepan los dos rieles de
    # masa. Mas holgada, la figura pasa de 176 mm y ya no entra en
    # una pagina junto a su epigrafe.
    SEP = 270

    # ---------------------------------------------------- transmisora
    cuerpo, pinA, alto, cajas = C.placa_real(X_PLACA, Y_PLACA, {"GPIO4", "GND"})
    d.add(cuerpo, cajas)
    rielA = _riel(alto)
    d.texto(X_PLACA + 52, Y_PLACA - 14, "PLACA TRANSMISORA", 8,
            C.TEXTO, "middle", "bold")

    y4 = pinA["GPIO4"][1]
    bx, by = 316, y4 - 15
    b, patas = C.pulsador(bx, by)
    d.add(b)
    d.texto(bx + 15, by + 44, "pulsador", 7, C.TEXTO, "middle")
    d.cable([pinA["GPIO4"], (292, y4), (292, patas["a1"][1]),
             patas["a1"]], C.NARANJA)
    d.cable([patas["b1"], (400, patas["b1"][1]), (400, rielA)], C.NEGRO)
    d.nodo(400, rielA, C.NEGRO)
    d.cable([(400, rielA), (LANE_GND, rielA),
             (LANE_GND, pinA["GND"][1]), pinA["GND"]], C.NEGRO)

    # ------------------------------------------------------- receptora
    cuerpo2, pinB, alto2, cajas2 = C.placa_real(X_PLACA, Y_PLACA + SEP,
                                        {"GPIO4", "GND"})
    d.add(cuerpo2, cajas2)
    rielB = _riel(alto2) + SEP
    d.texto(X_PLACA + 52, Y_PLACA + SEP - 14, "PLACA RECEPTORA", 8,
            C.TEXTO, "middle", "bold")

    y4b = pinB["GPIO4"][1]
    zx, zy = 330, y4b
    d.add('<circle cx="%g" cy="%g" r="22" fill="#3A3F46" stroke="%s" '
          'stroke-width="1"/>' % (zx, zy, C.PLACA_BORDE))
    d.add('<circle cx="%g" cy="%g" r="5" fill="#20242A"/>' % (zx, zy))
    d.texto(zx - 10, zy - 4, "+", 11, "#E8EDF2", "middle", "bold",
            serigrafia=True)
    d.texto(zx, zy - 31, "zumbador activo", 7, C.TEXTO, "middle")
    mas, menos = (zx - 9, zy + 22), (zx + 9, zy + 22)

    d.cable([pinB["GPIO4"], (292, y4b), (292, mas[1] + 12),
             (mas[0], mas[1] + 12), mas], C.NARANJA)
    d.cable([menos, (menos[0], rielB)], C.NEGRO)
    d.nodo(menos[0], rielB, C.NEGRO)
    d.cable([(menos[0], rielB), (LANE_GND, rielB),
             (LANE_GND, pinB["GND"][1]), pinB["GND"]], C.NEGRO)

    # ------------------------------------------------- el enlace
    # El símbolo va al costado, en la franja entre las dos placas:
    # en el centro chocaba con los rótulos.
    d.add(C.enlace_radio(296, Y_PLACA + alto + 58, 122))

    return d, rielB + 20


TODOS = {"lab_7_2": lab_7_2, "lab_7_4": lab_7_4}


def svg(nombre):
    d, alto = TODOS[nombre]()
    return d.svg(LIENZO, alto), len(d.cruces())


# ------------------------------------------------ figura de apertura
def rutas():
    """Las tres maneras de sacar el dato de la placa, comparadas."""
    W = 340
    s = []
    filas = (
        (52, "La propia placa es el servidor", "7.2 y 7.3",
         "El teléfono entra a su dirección. No hace falta ninguna cuenta "
         "ni internet, pero sólo alcanza dentro de la misma red.", C.SENAL),
        (128, "Al teléfono, por Bluetooth", "7.4",
         "El teléfono se conecta directamente a la placa. No hace falta "
         "red de ninguna clase, pero hay que estar al lado.", C.NARANJA),
        (204, "De placa a placa, por radio", "7.5",
         "ESP-NOW usa la radio del WiFi sin conectarse a ninguna red. "
         "Llega lejos y no depende de nadie, pero sólo habla con otra placa.",
         C.VIOLETA),
        (280, "A un servidor de internet", "7.6 y 7.7",
         "MQTT publica en un servidor que guarda el histórico y se mira "
         "desde cualquier parte. Hace falta cuenta, clave y conexión.",
         C.ROJO),
    )
    for y, titulo, labs, texto, color in filas:
        s.append('<rect x="14" y="%g" width="4" height="58" rx="2" '
                 'fill="%s"/>' % (y - 12, color))
        s.append(C._txt(28, y, titulo, 8.6, C.TEXTO, "start", "bold"))
        rotulo = ("laboratorios " if " y " in labs
                  else "laboratorio ") + labs
        s.append(C._txt(W - 8, y, rotulo, 7, color, "end", "bold"))
        # el texto se parte a mano para no depender del ancho de la caja
        palabras, linea, lineas = texto.split(), "", []
        for p in palabras:
            if len(linea) + len(p) > 62:
                lineas.append(linea); linea = p
            else:
                linea = (linea + " " + p).strip()
        lineas.append(linea)
        for i, l in enumerate(lineas[:3]):
            s.append(C._txt(28, y + 13 + i * 10, l, 7.2, "#4a4a48", "start"))
    return C.envoltura("".join(s), W, 338)
