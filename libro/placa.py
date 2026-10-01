# -*- coding: utf-8 -*-
"""La placa ESP32 dibujada como se ve, en vista superior.

El orden de los pines está tomado del plano de la propia guía de
laboratorio de la asignatura (ESP32 de 30 pines), que es el que
tienen los estudiantes en la mano. Cambiar ese orden por el de otra
placa es cambiar una sola lista.

El color agrupa por lo que al libro le importa —qué pin sirve para
qué— y no por la familia de periféricos. En particular distingue el
ADC1 del ADC2, que es la trampa que más tiempo hace perder en el
laboratorio.
"""

# ------------------------------------------------- orden fisico real
# Placa vertical, con el conector USB abajo y mirando el lado de los
# componentes. Tomado de la guia de laboratorio, pagina 55.
IZQUIERDA = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25",
             "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
DERECHA = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5",
           "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]

# nombre visible -> (GPIO, categoria, nota)
INFO = {
    "EN":  ("",        "control", "reinicia la placa"),
    "VP":  ("GPIO36",  "adc1",    "solo entrada"),
    "VN":  ("GPIO39",  "adc1",    "solo entrada"),
    "D34": ("GPIO34",  "adc1",    "solo entrada"),
    "D35": ("GPIO35",  "adc1",    "solo entrada"),
    "D32": ("GPIO32",  "adc1",    ""),
    "D33": ("GPIO33",  "adc1",    ""),
    "D25": ("GPIO25",  "adc2",    "DAC1"),
    "D26": ("GPIO26",  "adc2",    "DAC2"),
    "D27": ("GPIO27",  "adc2",    ""),
    "D14": ("GPIO14",  "adc2",    ""),
    "D12": ("GPIO12",  "arranque", "ADC2"),
    "D13": ("GPIO13",  "adc2",    ""),
    "D23": ("GPIO23",  "digital", "MOSI"),
    "D22": ("GPIO22",  "digital", "SCL"),
    "TX0": ("GPIO1",   "consola", "no usar"),
    "RX0": ("GPIO3",   "consola", "no usar"),
    "D21": ("GPIO21",  "digital", "SDA"),
    "D19": ("GPIO19",  "digital", "MISO"),
    "D18": ("GPIO18",  "digital", "SCK"),
    "D5":  ("GPIO5",   "arranque", ""),
    "TX2": ("GPIO17",  "digital", ""),
    "RX2": ("GPIO16",  "digital", ""),
    "D4":  ("GPIO4",   "adc2",    ""),
    "D2":  ("GPIO2",   "arranque", "LED de la placa"),
    "D15": ("GPIO15",  "arranque", "ADC2"),
    "GND": ("",        "masa",    ""),
    "VIN": ("",        "poder",   "5 V"),
    "3V3": ("",        "poder",   "3,3 V"),
}

CATEGORIA = {
    "poder":    ("#C0392B", "#FFFFFF", "Alimentación"),
    "masa":     ("#33383D", "#FFFFFF", "Masa"),
    "adc1":     ("#2E7D5B", "#FFFFFF", "ADC1 — sirve con el WiFi encendido"),
    "adc2":     ("#B9770E", "#FFFFFF", "ADC2 — deja de medir con el WiFi encendido"),
    "digital":  ("#1B6B8C", "#FFFFFF", "Entrada o salida digital"),
    "arranque": ("#7D3C98", "#FFFFFF", "Se lee al arrancar: cuidado con lo que se conecte"),
    "consola":  ("#7A8290", "#FFFFFF", "Puerto serie del USB: no usar"),
    "control":  ("#4A5568", "#FFFFFF", "Control"),
}

# Alias: el programa dice Pin(16) y la serigrafia dice RX2. En el
# codigo de las figuras se escribe GPIO16, que es lo que el lector
# tiene delante cuando mira el programa.
ALIAS = {}
for _nombre, (_gpio, _c, _n) in INFO.items():
    if _gpio:
        ALIAS[_gpio] = _nombre


def resolver(nombre):
    """Acepta GPIO16 o RX2 y devuelve siempre el nombre de serigrafia."""
    return ALIAS.get(nombre, nombre)


FUENTE = "font-family:'DejaVu Sans',sans-serif"
PASO = 12.4          # separacion entre pines
BORDE = 18           # del canto de la placa a la primera pata
ANCHO = 104          # ancho de la placa


def _t(x, y, s, tam, color, anclaje="start", peso="normal", inclinada=False):
    est = "%s;font-size:%gpx;fill:%s;font-weight:%s" % (FUENTE, tam, color, peso)
    if inclinada:
        est += ";font-style:italic"
    return '<text x="%g" y="%g" text-anchor="%s" style="%s">%s</text>' % (
        x, y, anclaje, est, s)


def placa(x, y, usados=None, con_rotulos=True, gnd_lado="der",
          serigrafia=True):
    """Dibuja la placa en vista superior.

    usados: nombres de pin que este laboratorio ocupa (se admite el
    numero de GPIO, que se traduce solo a la serigrafia). Si se pasa,
    solo esos se rotulan y el resto queda como pata sin marcar, que
    es como debe verse en el diagrama de un laboratorio concreto.

    Devuelve (svg, posiciones) con el punto de cada pin.
    """
    if usados is not None:
        usados = {resolver(u) for u in usados}
    n = len(IZQUIERDA)
    alto = BORDE * 2 + PASO * (n - 1)
    s = []

    # ---- cuerpo de la placa
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="6" '
             'fill="#1F2A24" stroke="#0E1512" stroke-width="1.2"/>'
             % (x, y, ANCHO, alto))

    # ---- agujeros de montaje, uno en cada esquina
    for ax in (x + 11, x + ANCHO - 11):
        for ay in (y + 11, y + alto - 11):
            s.append('<circle cx="%g" cy="%g" r="5" fill="#0B1310" '
                     'stroke="#3C4A42" stroke-width="1"/>' % (ax, ay))

    # ---- modulo ESP-WROOM-32 con su antena
    mx, my, mw, mh = x + 21, y + 24, ANCHO - 42, 96
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="2" '
             'fill="#B9BFC6" stroke="#8A9199" stroke-width="1"/>'
             % (mx, my, mw, mh))
    # serpentina de la antena, arriba
    px = mx + 6
    puntos = []
    for i in range(7):
        puntos += [(px + i * (mw - 12) / 6.0, my + 5),
                   (px + i * (mw - 12) / 6.0, my + 13)]
    s.append('<polyline points="%s" fill="none" stroke="#7D858D" '
             'stroke-width="1.6"/>'
             % " ".join("%g,%g" % p for p in puntos))
    cx, cy = mx + mw / 2, my + mh / 2
    s.append('<g transform="rotate(-90 %g %g)">%s</g>'
             % (cx, cy, _t(cx, cy + 3, "ESP-WROOM-32", 7.4,
                           "#4A5058", "middle", "bold")))

    # ---- conector USB, abajo
    s.append('<rect x="%g" y="%g" width="26" height="13" rx="2" '
             'fill="#9AA4B0" stroke="#6B7580" stroke-width="1"/>'
             % (x + ANCHO / 2 - 13, y + alto - 9))
    s.append(_t(x + ANCHO / 2, y + alto + 16, "USB", 7, "#5A6068", "middle"))

    # ---- pulsadores EN y BOOT
    for bx, nombre in ((x + 15, "EN"), (x + ANCHO - 29, "BOOT")):
        s.append('<rect x="%g" y="%g" width="14" height="14" rx="2" '
                 'fill="#6E7780" stroke="#4A5058" stroke-width="0.8"/>'
                 % (bx, y + alto - 34))
        s.append(_t(bx + 7, y + alto - 37, nombre, 5.6, "#C8CED6", "middle"))

    # ---- pines
    pos = {}
    cajas = []
    for columna, lado in ((IZQUIERDA, -1), (DERECHA, 1)):
        px = x + 9 if lado < 0 else x + ANCHO - 9
        for i, nombre in enumerate(columna):
            py = y + BORDE + i * PASO
            lado_txt = "izq" if lado < 0 else "der"
            # GND esta en las dos columnas. En el diagrama de un
            # laboratorio se rotula solo el del lado por donde va a
            # salir el cable, o el dibujo pide un rotulo que caeria
            # fuera del lienzo.
            marcado = usados is None or nombre in usados
            if marcado and nombre == "GND" and usados is not None \
                    and lado_txt != gnd_lado:
                marcado = False
            # GND aparece en las dos columnas. Rotular las dos en el
            # diagrama de un laboratorio sugiere que hay que cablear
            # ambas, que no es el caso.
            if nombre == "GND" and usados is not None and lado_txt != gnd_lado:
                marcado = False
            # pastilla de la pata
            s.append('<circle cx="%g" cy="%g" r="4.4" fill="#0B1310" '
                     'stroke="%s" stroke-width="1.6"/>'
                     % (px, py, "#C9A227" if marcado else "#4A5A52"))
            # GND aparece en las dos columnas, asi que se guarda con
            # el lado explicito y ademas como nombre suelto, apuntando
            # al primero que se encuentre.
            punto = (px + 9 * lado, py)   # provisional: la pata desnuda
            pos[(lado_txt, nombre)] = punto
            if nombre != "GND" or lado_txt == gnd_lado:
                pos.setdefault(nombre, punto)

            if con_rotulos and marcado:
                gpio, categoria, _nota = INFO.get(nombre, ("", "digital", ""))
                fondo, tinta, _ = CATEGORIA[categoria]
                etiqueta = gpio if gpio else nombre
                ancho_et = 6.2 * len(etiqueta) + 10
                if _nota == "solo entrada":
                    ancho_et += 9      # sitio para la punta, sin pisar el texto
                ex = px - 11 - ancho_et if lado < 0 else px + 11
                s.append('<rect x="%g" y="%g" width="%g" height="13" rx="2.6" '
                         'fill="%s"/>' % (ex, py - 6.5, ancho_et, fondo))
                cajas.append((ex, py - 6.5, ex + ancho_et, py + 6.5))
                desplazado = -4.5 if _nota == "solo entrada" and lado < 0 else (
                    4.5 if _nota == "solo entrada" else 0)
                s.append(_t(ex + ancho_et / 2 + desplazado, py + 3.4, etiqueta,
                            7.2, tinta, "middle", "bold"))
                # Cuatro pines del ADC1 no pueden ser salida nunca. Se
                # marcan con una punta hacia adentro: la señal entra,
                # no sale.
                if _nota == "solo entrada":
                    # la punta mira hacia la placa: la señal entra
                    tx = ex + ancho_et - 4 if lado < 0 else ex + 4
                    d = 5 if lado < 0 else -5
                    s.append('<path d="M %g %g l %g 4 l 0 -8 z" fill="#FFFFFF" '
                             'opacity="0.9"/>' % (tx, py, d))
                # Lo que dice la serigrafia, cuando no es el numero de
                # GPIO: el estudiante busca VP o RX2 sobre el cobre, no
                # GPIO36 ni GPIO16. En el diagrama de un laboratorio
                # estorba, porque ahi va el cable, y se apaga.
                if serigrafia and gpio and nombre != "D" + gpio[4:]:
                    sx = ex - 4 if lado < 0 else ex + ancho_et + 4
                    s.append(_t(sx, py + 3, nombre, 6,
                                "#6B7580", "end" if lado < 0 else "start"))
                # linea corta de la pata al rotulo
                s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                         'stroke-width="1.4"/>'
                         % (px + 4.6 * lado, py, px + 11 * lado, py, "#8A9199"))
                # El cable se engancha en el borde exterior del rotulo.
                # Enganchado en la pata cruzaria por encima de su propia
                # etiqueta, que es justo donde el lector mira.
                borde = (ex if lado < 0 else ex + ancho_et, py)
                pos[(lado_txt, nombre)] = borde
                if nombre != "GND" or lado_txt == gnd_lado:
                    pos[nombre] = borde
    return "".join(s), pos, alto, cajas


def leyenda(x, y, ancho=420, columnas=2):
    """La tabla de colores que acompaña al plano de la placa."""
    s = []
    orden = ["poder", "masa", "adc1", "adc2", "digital", "arranque",
             "consola", "control"]
    extra = "los cuatro pines con punta blanca solo pueden ser entrada"
    paso_y, paso_x = 15, ancho / columnas
    for i, clave in enumerate(orden):
        fondo, tinta, texto = CATEGORIA[clave]
        cx = x + (i % columnas) * paso_x
        cy = y + (i // columnas) * paso_y
        s.append('<rect x="%g" y="%g" width="15" height="10" rx="2.2" '
                 'fill="%s"/>' % (cx, cy - 7.5, fondo))
        s.append(_t(cx + 20, cy, texto, 7, "#1b1b1a"))
    fin = y + ((len(orden) + columnas - 1) // columnas) * paso_y
    s.append('<path d="M %g %g l -5 4 l 0 -8 z" fill="#2E7D5B"/>' % (x + 13, fin))
    s.append(_t(x + 20, fin + 3, extra, 7, "#1b1b1a", inclinada=True))
    return "".join(s), fin + 8


# =================================================================
#  Enrutado de cables
#
#  Con la placa realista, cada pata esta donde esta de verdad: el
#  GPIO23 arriba a la derecha, el VIN abajo a la izquierda. Eso hace
#  que los cables ya no salgan todos en linea recta, y colocarlos a
#  mano en cada figura es lento y se presta a colisiones. Estas dos
#  funciones resuelven los dos casos que aparecen siempre.
# =================================================================
LADO_DE = {}
for _i, _n in enumerate(IZQUIERDA):
    LADO_DE.setdefault(_n, "izq")
for _i, _n in enumerate(DERECHA):
    if _n not in LADO_DE:
        LADO_DE[_n] = "der"
LADO_DE["GND"] = "der"          # se prefiere la masa del lado derecho


def canal(desde, hasta, x_canal):
    """Cable en escuadra: sale, baja o sube por un canal, y entra.

    Es el trazado normal cuando las dos puntas estan del mismo lado.
    """
    return [desde, (x_canal, desde[1]), (x_canal, hasta[1]), hasta]


def por_arriba(desde, hasta, y_canal, x_salida):
    """Cable que rodea la placa por encima.

    Sirve para las patas del lado izquierdo cuando el componente esta
    a la derecha: en la protoboard el cable tambien pasa por encima de
    la placa, asi que el dibujo no esta inventando nada.
    """
    return [desde, (x_salida, desde[1]), (x_salida, y_canal),
            (hasta[0], y_canal), hasta]


def recto(desde, hasta):
    """Cable con un solo quiebre, cuando alcanza."""
    if abs(desde[1] - hasta[1]) < 0.5:
        return [desde, hasta]
    return [desde, ((desde[0] + hasta[0]) / 2.0, desde[1]),
            ((desde[0] + hasta[0]) / 2.0, hasta[1]), hasta]
