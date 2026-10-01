# -*- coding: utf-8 -*-
"""Diagramas de conexión vectoriales para el libro.

Todo sale en SVG, de modo que la imprenta puede ampliarlo cuanto
quiera sin que se pixele, y el archivo pesa unos pocos kilobytes.

Dos decisiones de diseño que conviene no perder:

1. El color NO lleva informacion por si solo. Cada cable ademas
   termina rotulado con el nombre del pin, porque si el interior
   del libro se imprime en blanco y negro los colores se vuelven
   grises parecidos. El diagrama tiene que seguir siendo legible.

2. Las resistencias se dibujan con sus bandas de color reales, que
   es como el estudiante las va a reconocer en la caja de
   componentes.
"""

import re

# --------------------------------------------------------- colores
TINTA = "#1b1b1a"
AZUL_TITULO = "#1B3A6B"   # el azul de los titulos del libro
PLACA = "#2F3B4C"
PLACA_BORDE = "#1B2430"
ROJO = "#C0392B"        # alimentacion positiva
NEGRO = "#33383D"       # masa
SENAL = "#1B6B8C"       # señal
NARANJA = "#D2691E"     # segunda señal, para que no se confundan
VIOLETA = "#6C3FA0"     # tercera señal
TEXTO = "#1b1b1a"
GRIS = "#7A8290"

BANDAS = {
    "330":  ["#E67E22", "#E67E22", "#7B4B2A", "#C9A227"],   # naranja naranja marron
    "10k":  ["#7B4B2A", "#1b1b1a", "#E67E22", "#C9A227"],   # marron negro naranja
    "4k7":  ["#E8C31E", "#7D3C98", "#C0392B", "#C9A227"],   # amarillo violeta rojo
    "100k": ["#7B4B2A", "#1b1b1a", "#E8C31E", "#C9A227"],   # marron negro amarillo
    "15k":  ["#7B4B2A", "#2E8B57", "#E67E22", "#C9A227"],   # marron verde naranja
}

FUENTE = "font-family:'DejaVu Sans',sans-serif"


# ---------------------------------------------------------- piezas
def _txt(x, y, t, tam=8, color=TEXTO, anclaje="start", peso="normal", inclinada=False):
    est = "%s;font-size:%gpx;fill:%s;font-weight:%s" % (FUENTE, tam, color, peso)
    if inclinada:
        est += ";font-style:italic"
    return '<text x="%g" y="%g" text-anchor="%s" style="%s">%s</text>' % (
        x, y, anclaje, est, t)


_TEXTO_SVG = re.compile(
    r'<text\b([^>]*)>(.*?)</text>', re.S)
_ATRIBUTO = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
_TAMANO = re.compile(r'font-size:\s*([\d.]+)px')

# Ancho medio de un caracter en DejaVu Sans, como fraccion del cuerpo.
# Es una estimacion, y para vigilar solapamientos alcanza: el error es
# de decimas de pixel y el margen del detector es mayor.
_ANCHO_CAR = 0.60


_RECT_SVG = re.compile(r'<rect\b([^>]*)/?>')
_CIRC_SVG = re.compile(r'<(circle|ellipse)\b([^>]*)/?>')

# Por debajo de esta superficie una figura no es un "cuerpo": es una
# banda de resistencia, un pad, el reborde de un LED. Encima, es algo
# sobre lo que ningun rotulo deberia caer.
_AREA_MINIMA = 1200


def _cuerpos_opacos(svg):
    """Rectangulos y elipses rellenos lo bastante grandes para tapar texto."""
    cajas = []
    for atributos in _RECT_SVG.findall(svg):
        at = dict(_ATRIBUTO.findall(atributos))
        if "transform" in at or at.get("fill", "").lower() in ("none", ""):
            continue
        try:
            x, y = float(at.get("x", 0)), float(at.get("y", 0))
            w, h = float(at["width"]), float(at["height"])
        except (KeyError, ValueError):
            continue
        if w * h >= _AREA_MINIMA:
            cajas.append((x, y, x + w, y + h))
    for _etiqueta, atributos in _CIRC_SVG.findall(svg):
        at = dict(_ATRIBUTO.findall(atributos))
        if "transform" in at or at.get("fill", "").lower() in ("none", ""):
            continue
        try:
            cx, cy = float(at.get("cx", 0)), float(at.get("cy", 0))
            rx = float(at.get("r", at.get("rx", 0)))
            ry = float(at.get("r", at.get("ry", 0)))
        except ValueError:
            continue
        if rx * ry * 3.1416 >= _AREA_MINIMA:
            cajas.append((cx - rx, cy - ry, cx + rx, cy + ry))
    return cajas


def _cajas_de_texto(svg, con_texto=False):
    """Rectangulos que ocupan los <text> de un fragmento de SVG.

    Sirve para que el detector de rotulos tapados no dependa de que
    cada componente declare su caja a mano: si el dibujo tiene un
    rotulo, queda protegido.

    Se saltan los textos con transform —la serigrafia girada de la
    placa—, porque ningun cable pasa por encima del modulo.
    """
    cajas = []
    for atributos, contenido in _TEXTO_SVG.findall(svg):
        at = dict(_ATRIBUTO.findall(atributos))
        if "transform" in at:
            continue
        texto = re.sub(r'<[^>]+>', '', contenido).strip()
        if not texto:
            continue
        try:
            x = float(at.get("x", 0))
            y = float(at.get("y", 0))
        except ValueError:
            continue
        m = _TAMANO.search(at.get("style", ""))
        tam = float(m.group(1)) if m else 8.0
        ancho = len(texto) * tam * _ANCHO_CAR
        anclaje = at.get("text-anchor", "start")
        if anclaje == "middle":
            x1 = x - ancho / 2
        elif anclaje == "end":
            x1 = x - ancho
        else:
            x1 = x
        # La caja va de la altura de mayuscula a un pelo por debajo de
        # la linea base: es donde esta la tinta. Bajarla hasta el
        # trazo descendente daba por tapados rotulos que en la pagina
        # se leen perfectamente, y el margen del detector ya cubre la
        # cola de una "g".
        caja = (x1, y - tam * 0.74, x1 + ancho, y + tam * 0.10)
        cajas.append((caja, texto) if con_texto else caja)
    return cajas


def _cable(puntos, color, grosor=2.0):
    d = " ".join("%g,%g" % (x, y) for x, y in puntos)
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" '
            'stroke-linejoin="round" stroke-linecap="round"/>' % (d, color, grosor))


def _nodo(x, y, color):
    return '<circle cx="%g" cy="%g" r="2.6" fill="%s"/>' % (x, y, color)


def placa_esquematica(x, y, alto=150, pines_der=(), pines_izq=(), etiqueta="ESP32 DevKit V1"):
    """Dibuja la placa con solo los pines que el laboratorio usa.

    Se muestran los pines usados y no los treinta, para que el
    diagrama de cada laboratorio quede limpio. El plano completo de
    la placa aparece una sola vez, en el capitulo 1.

    Devuelve (svg, posiciones) donde posiciones['GPIO23'] = (x, y)
    del extremo del pin, listo para engancharle un cable.
    """
    ANCHO = 74
    s = []
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="5" '
             'fill="%s" stroke="%s" stroke-width="1"/>'
             % (x, y, ANCHO, alto, PLACA, PLACA_BORDE))
    # conector USB arriba
    s.append('<rect x="%g" y="%g" width="20" height="9" rx="1.5" '
             'fill="#9AA4B0" stroke="%s" stroke-width="0.8"/>'
             % (x + ANCHO / 2 - 10, y - 7, PLACA_BORDE))
    s.append(_txt(x + ANCHO / 2, y - 10, "USB", 6, GRIS, "middle"))
    # El nombre va girado contra el canto izquierdo. Puesto en el centro
    # chocaba con las etiquetas de los pines cuando el laboratorio usa
    # cuatro o mas, y el choque dependia del numero de pines: un defecto
    # que solo aparecia en algunas figuras.
    cx, cy = x + 15, y + alto / 2
    s.append('<g transform="rotate(-90 %g %g)">%s%s</g>' % (
        cx, cy,
        _txt(cx, cy - 3, "ESP32", 9, "#E8EDF2", "middle", "bold"),
        _txt(cx, cy + 7, "DevKit V1", 6.2, "#9AA4B0", "middle")))

    pos = {}
    for pines, lado in ((pines_izq, -1), (pines_der, 1)):
        if not pines:
            continue
        paso = alto / (len(pines) + 1)
        for i, nombre in enumerate(pines, 1):
            py = y + paso * i
            px = x + ANCHO if lado > 0 else x
            fin = px + 9 * lado
            s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                     'stroke-width="2.4" stroke-linecap="round"/>'
                     % (px, py, fin, py, "#C8CEd6"))
            s.append(_txt(px - 4 * lado, py + 2.6, nombre, 6.6, "#E8EDF2",
                          "end" if lado > 0 else "start", "bold"))
            pos[nombre] = (fin, py)
    return "".join(s), pos


def resistencia(x, y, valor="330", horizontal=True, rotulo=None):
    """Resistencia con sus bandas de color reales."""
    L, H = 26, 10
    s = []
    if horizontal:
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.6"/>' % (x - 8, y, x + L + 8, y, GRIS))
        s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="3" '
                 'fill="#E8D9B5"/>' % (x, y - H / 2, L, H))
        for i, c in enumerate(BANDAS.get(valor, BANDAS["330"])):
            bx = x + 4 + i * 5
            if i == 3:
                bx = x + L - 4
            s.append('<rect x="%g" y="%g" width="2.4" height="%g" fill="%s"/>'
                     % (bx, y - H / 2, H, c))
        if rotulo:
            s.append(_txt(x + L / 2, y + H / 2 + 9, rotulo, 7, TEXTO, "middle"))
        return "".join(s), (x - 8, y), (x + L + 8, y)
    else:
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.6"/>' % (x, y - 8, x, y + L + 8, GRIS))
        s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="3" fill="#E8D9B5"/>'
                 % (x - H / 2, y, H, L))
        for i, c in enumerate(BANDAS.get(valor, BANDAS["330"])):
            by = y + 4 + i * 5
            if i == 3:
                by = y + L - 4
            s.append('<rect x="%g" y="%g" width="%g" height="2.4" fill="%s"/>'
                     % (x - H / 2, by, H, c))
        if rotulo:
            s.append(_txt(x + H / 2 + 4, y + L / 2 + 2, rotulo, 7, TEXTO, "start"))
        return "".join(s), (x, y - 8), (x, y + L + 8)


def led(x, y, color="#C0392B", etiqueta=None, rotular=True):
    """LED de pie, como se ve sobre la protoboard.

    (x, y) es el centro de la cupula. Las dos patas bajan, la
    izquierda mas larga que la derecha, y cada una queda rotulada
    debajo con su nombre y su signo: de pie no hay manera de
    confundir cual es cual, que es lo que pasaba con el LED tumbado.

    Devuelve (svg, anodo, catodo) con el extremo de cada pata.
    """
    R = 11
    LARGA, CORTA = 46, 32
    ax, cx = x - 5, x + 5
    s = []

    # cupula
    s.append('<path d="M %g %g a %g %g 0 0 1 %g 0 l 0 %g l %g 0 z" '
             'fill="%s" stroke="%s" stroke-width="0.9" opacity="0.93"/>'
             % (x - R, y, R, R, 2 * R, R + 2, -2 * R, color, PLACA_BORDE))
    # brillo
    s.append('<ellipse cx="%g" cy="%g" rx="2.6" ry="4" fill="#FFFFFF" '
             'opacity="0.35"/>' % (x - 4, y - 3))
    # reborde
    s.append('<rect x="%g" y="%g" width="%g" height="5" rx="1.5" '
             'fill="%s" stroke="%s" stroke-width="0.7"/>'
             % (x - R - 3, y + R + 1, 2 * R + 6, color, PLACA_BORDE))

    # patas
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
             'stroke-width="2.4" stroke-linecap="round"/>'
             % (ax, y + R + 6, ax, y + R + 6 + LARGA, GRIS))
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
             'stroke-width="2.4" stroke-linecap="round"/>'
             % (cx, y + R + 6, cx, y + R + 6 + CORTA, GRIS))

    anodo = (ax, y + R + 6 + LARGA)
    catodo = (cx, y + R + 6 + CORTA)

    if rotular:
        # cada pata rotulada a su propio lado y a distinta altura
        # El ánodo se rotula DEBAJO de su pata. Puesto al costado se
        # lo comía el cable que baja por fuera del cuerpo.
        # Alineado por la derecha y terminando antes de la pata corta:
        # el cable del catodo baja justo por ahi y, centrado, le
        # pasaba por encima.
        s.append(_txt(ax + 3, anodo[1] + 11, "ánodo  +", 6.6, TEXTO, "end", "bold"))
        s.append(_txt(ax + 3, anodo[1] + 18, "pata larga", 6, GRIS, "end"))
        s.append(_txt(cx + 9, catodo[1] - 4, "cátodo  −", 6.6, TEXTO, "start", "bold"))
        s.append(_txt(cx + 9, catodo[1] + 3, "pata corta", 6, GRIS, "start"))
    if etiqueta:
        s.append(_txt(x, y - R - 8, etiqueta, 7, TEXTO, "middle"))
    return "".join(s), anodo, catodo


def pulsador(x, y):
    """Pulsador de cuatro patas visto desde arriba."""
    s = []
    s.append('<rect x="%g" y="%g" width="30" height="30" rx="2.5" fill="#D8DCE2" '
             'stroke="%s" stroke-width="1"/>' % (x, y, PLACA_BORDE))
    s.append('<circle cx="%g" cy="%g" r="7.5" fill="#4A5568" stroke="%s" '
             'stroke-width="0.8"/>' % (x + 15, y + 15, PLACA_BORDE))
    patas = {}
    for dx, dy, nombre in ((0, 6, "a1"), (0, 24, "a2"), (30, 6, "b1"), (30, 24, "b2")):
        x2 = x + dx + (-7 if dx == 0 else 7)
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.6"/>' % (x + dx, y + dy, x2, y + dy, GRIS))
        patas[nombre] = (x2, y + dy)
    # las patas de un mismo lado estan unidas de fabrica
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1" '
             'stroke-dasharray="2,2"/>' % (x + 3, y + 6, x + 3, y + 24, GRIS))
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1" '
             'stroke-dasharray="2,2"/>' % (x + 27, y + 6, x + 27, y + 24, GRIS))
    return "".join(s), patas


def modulo(x, y, ancho, alto, titulo, pines, color="#2E6B4F"):
    """Un modulo de tres o cuatro patas: PIR, DHT11, sensor, etc."""
    s = []
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="3" fill="%s" '
             'stroke="%s" stroke-width="1"/>' % (x, y, ancho, alto, color, PLACA_BORDE))
    s.append(_txt(x + ancho / 2, y + 13, titulo, 7.6, "#EAF2ED", "middle", "bold"))
    pos = {}
    paso = alto / (len(pines) + 1)
    for i, nombre in enumerate(pines, 1):
        py = y + paso * i + 4
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (x, py, x - 9, py, "#C8CED6"))
        s.append(_txt(x + 5, py + 2.6, nombre, 6.6, "#EAF2ED", "start", "bold"))
        pos[nombre] = (x - 9, py)
    return "".join(s), pos


def envoltura(cuerpo, ancho, alto, pie=None):
    """Cierra el SVG.

    El parametro pie se conserva por compatibilidad pero ya no se
    dibuja: la advertencia va en el epigrafe numerado de la figura,
    que es donde el lector la busca, y asi no aparece dos veces.
    """
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" '
            'width="100%%" style="display:block;margin:1mm auto 1.5mm;">'
            '%s</svg>' % (ancho, alto - 14, cuerpo))


# --------------------------------------------------- reticula comun
# Todos los diagramas del libro se arman sobre estas coordenadas, para
# que la placa quede siempre del mismo tamaño y en el mismo lugar, y el
# lector reconozca la figura de un vistazo.
LIENZO = 340        # ancho de todos los diagramas
X_PLACA = 14        # borde izquierdo de la placa
X_PIN = 97          # donde terminan los pines de la placa
COL_A = 150         # primera columna de componentes
COL_B = 252         # segunda columna de componentes
Y_NOTA = 13         # notas en cursiva, sobre la placa
Y_PLACA = 34        # borde superior de la placa
MARGEN_PIE = 46     # altura reservada para el riel de masa y el pie


def riel(alto):
    """Altura del riel de masa comun."""
    return alto - MARGEN_PIE + 12


def cable_encima(puntos, color, grosor=2.0):
    """Cable que cruza por encima de otro.

    Con la placa dibujada en su posicion real, hay cruces que no se
    pueden evitar: el GPIO5 esta mas arriba que el GPIO4 y a veces el
    componente del GPIO5 va mas abajo. Dos rectas que se cortan sin
    mas dejan al lector sin saber si estan unidas.

    La solucion de toda la vida en el dibujo tecnico: el cable de
    encima lleva una funda del color del papel, de modo que se ve
    pasar por arriba y el cruce queda sin ambiguedad.
    """
    d = " ".join("%g,%g" % (x, y) for x, y in puntos)
    return ('<polyline points="%s" fill="none" stroke="#FFFFFF" '
            'stroke-width="%g" stroke-linejoin="round" stroke-linecap="round"/>'
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" '
            'stroke-linejoin="round" stroke-linecap="round"/>'
            % (d, grosor + 3.4, d, color, grosor))


def potenciometro(x, y, rotulo="10 kΩ"):
    """Potenciometro visto desde arriba, con sus tres patas abajo.

    Devuelve (svg, extremo1, cursor, extremo2).
    """
    s = []
    s.append('<rect x="%g" y="%g" width="54" height="34" rx="3" '
             'fill="#2B5F8A" stroke="%s" stroke-width="1"/>'
             % (x, y, PLACA_BORDE))
    s.append('<circle cx="%g" cy="%g" r="13" fill="#D8DCE2" stroke="%s" '
             'stroke-width="1"/>' % (x + 27, y + 17, PLACA_BORDE))
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
             'stroke-width="2.4" stroke-linecap="round"/>'
             % (x + 27, y + 17, x + 27, y + 6, "#3A3F46"))
    patas = []
    for i in range(3):
        px = x + 11 + i * 16
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.8" stroke-linecap="round"/>'
                 % (px, y + 34, px, y + 43, GRIS))
        patas.append((px, y + 43))
    s.append(_txt(x + 27, y - 5, rotulo, 7, TEXTO, "middle"))
    s.append(_txt(patas[1][0], y + 52, "cursor", 6, GRIS, "middle"))
    return "".join(s), patas[0], patas[1], patas[2]


def servo(x, y, rotulo="SG90"):
    """Servomotor con sus tres cables de color normalizado.

    Devuelve (svg, marron, rojo, naranja) = (masa, alimentacion, señal).
    """
    s = []
    s.append('<rect x="%g" y="%g" width="56" height="72" rx="3" '
             'fill="#2E7D8A" stroke="%s" stroke-width="1"/>' % (x, y, PLACA_BORDE))
    # eje y brazo
    s.append('<circle cx="%g" cy="%g" r="9" fill="#E8EDF2" stroke="%s" '
             'stroke-width="1"/>' % (x + 14, y - 3, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="26" height="5" rx="2.4" '
             'fill="#E8EDF2" stroke="%s" stroke-width="0.8"/>'
             % (x + 10, y - 20, PLACA_BORDE))
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#E8EDF2" '
             'stroke-width="4"/>' % (x + 14, y - 3, x + 14, y - 16))
    s.append(_txt(x + 28, y + 66, rotulo, 7.4, "#EAF2ED", "middle", "bold"))
    cables = []
    colores = ("#5A4632", "#C0392B", "#D68910")
    nombres = ("GND", "V+", "PWM")
    for i, (c, n) in enumerate(zip(colores, nombres)):
        # Separados 20 unidades: con 13 los cables salian tan juntos
        # que cualquier trazado hacia la placa se pisaba a si mismo.
        py = y + 8 + i * 20
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.6" stroke-linecap="round"/>'
                 % (x, py, x - 11, py, c))
        s.append(_txt(x + 5, py + 2.6, n, 6.4, "#EAF2ED", "start", "bold"))
        cables.append((x - 11, py))
    return "".join(s), cables[0], cables[1], cables[2]


# ------------------------------------------------- la placa de verdad
def placa_real(x, y, usados, gnd_lado="der"):
    """La misma placa del plano del capitulo 1, con las patas en su
    posicion fisica real y rotuladas solo las que este laboratorio usa.

    Devuelve (svg, pos, alto). En pos, la clave puede ser el nombre
    suelto ("GPIO23") o la tupla con el lado (("izq", "GND")), que
    hace falta porque GND aparece en las dos columnas.
    """
    import placa as _P
    # La serigrafia se apaga: en el diagrama de un laboratorio va el
    # cable justo donde iria ese texto. El plano del capitulo 1 la trae.
    cuerpo, crudo, alto, cajas = _P.placa(x, y, usados=usados,
                                          serigrafia=False,
                                          gnd_lado=gnd_lado)
    pos = dict(crudo)
    for clave, punto in list(crudo.items()):
        nombre = clave[1] if isinstance(clave, tuple) else clave
        gpio = _P.INFO.get(nombre, ("", "", ""))[0]
        if gpio:
            pos[(clave[0], gpio)] = punto if isinstance(clave, tuple) else punto
            if not isinstance(clave, tuple):
                pos.setdefault(gpio, punto)
    return cuerpo, pos, alto, cajas


# ------------------------------------------- deteccion de cruces
def _segmentos(puntos):
    return list(zip(puntos, puntos[1:]))


def _se_cruzan(a, b, holgura=1.5):
    """True si dos segmentos ortogonales se cruzan o se rozan.

    Solo se comprueban cruces entre un tramo horizontal y uno
    vertical, que es lo unico que producen estos diagramas.
    """
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    a_horiz = abs(ay1 - ay2) < 0.01
    b_horiz = abs(by1 - by2) < 0.01
    if a_horiz == b_horiz:
        return False
    if b_horiz:
        a, b = b, a
        (ax1, ay1), (ax2, ay2) = a
        (bx1, by1), (bx2, by2) = b
    # a es horizontal, b vertical
    xi, xf = sorted((ax1, ax2))
    yi, yf = sorted((by1, by2))
    return (xi - holgura <= bx1 <= xf + holgura
            and yi - holgura <= ay1 <= yf + holgura)


def _comparten_extremo(a, b, holgura=2.0):
    for p in a:
        for q in b:
            if abs(p[0] - q[0]) < holgura and abs(p[1] - q[1]) < holgura:
                return True
    return False


class Dibujo:
    """Acumula el SVG y, de paso, vigila que ningun cable cruce a otro.

    Rutear a mano treinta diagramas garantiza que alguno salga con dos
    cables cruzados, y en un libro de laboratorio un cruce se lee como
    una conexion. Que lo compruebe la maquina.
    """

    def __init__(s, nombre):
        s.nombre = nombre
        s.piezas = []
        s.cables = []        # (recorrido, color, grosor)
        s.protegidas = []    # cajas de rotulo que ningun cable debe tapar
        s.rotulos = []       # (caja, texto, numero de pieza)
        s.macizos = []       # (caja, numero de pieza) de las piezas opacas

    def add(s, svg, cajas=None):
        pieza = len(s.piezas)
        s.piezas.append(svg)
        if cajas:
            s.protegidas.extend(cajas)
            for c in cajas:
                s.rotulos.append((c, "", pieza))
        # Todo rotulo del dibujo queda protegido, no solo los de la
        # placa: el nombre de un componente tapado por un cable es el
        # mismo defecto que el numero de un pin tapado.
        for caja, texto in _cajas_de_texto(svg, con_texto=True):
            s.protegidas.append(caja)
            s.rotulos.append((caja, texto, pieza))
        s.macizos.extend((c, pieza) for c in _cuerpos_opacos(svg))

    def proteger(s, *cajas):
        """Rotulos que ningun cable puede cruzar por encima."""
        s.protegidas.extend(cajas)

    def cable(s, puntos, color, grosor=2.0):
        """Anota el cable. El trazo se emite al cerrar el dibujo, para
        poder dibujar los saltos donde haga falta."""
        s.cables.append((list(puntos), color, grosor))
        s.piezas.append(("CABLE", len(s.cables) - 1))

    def nodo(s, x, y, color):
        s.piezas.append(_nodo(x, y, color))

    def texto(s, *a, **k):
        """Un rotulo suelto.

        Con serigrafia=True el rotulo va impreso a proposito sobre una
        pieza —el "+" del zumbador, por ejemplo— y el detector de
        encimados lo deja pasar.
        """
        serigrafia = k.pop("serigrafia", False)
        svg = _txt(*a, **k)
        pieza = len(s.piezas)
        s.piezas.append(svg)
        for caja, texto in _cajas_de_texto(svg, con_texto=True):
            s.protegidas.append(caja)
            if not serigrafia:
                s.rotulos.append((caja, texto, pieza))

    def encimados(s):
        """Rótulos que caen sobre el cuerpo de otra pieza.

        Un texto sobre la placa o sobre el cuerpo de un módulo es tan
        ilegible como uno tapado por un cable, y es el error más fácil
        de cometer: la nota va escrita en coordenadas absolutas y basta
        que la figura cambie de alto para que se le venga encima.

        No cuenta la serigrafía de la pieza misma —EN, BOOT, USB están
        impresos sobre la placa a propósito—, sólo el texto de una
        pieza sobre el cuerpo de otra.
        """
        malos = []
        for (rx1, ry1, rx2, ry2), texto, pieza in s.rotulos:
            for (mx1, my1, mx2, my2), otra in s.macizos:
                if otra == pieza:
                    continue
                if rx1 < mx2 and rx2 > mx1 and ry1 < my2 and ry2 > my1:
                    malos.append((texto, (rx1, ry1, rx2, ry2)))
                    break
        return malos

    def cruces(s):
        """Lista de cruces entre cables de distinta red.

        Devuelve (indice_del_cable_posterior, punto) para cada uno, que
        es donde hay que dibujar el salto.
        """
        malos = []
        for i, (ra, ca, _ga) in enumerate(s.cables):
            for j, (rb, cb, _gb) in enumerate(s.cables[i + 1:], i + 1):
                # La masa es un riel: todos sus tramos se juntan, y un
                # empalme no es un cruce. Entre redes distintas, en
                # cambio, cualquier contacto es un error.
                if ca == cb == NEGRO:
                    continue
                if ca == cb and _comparten_extremo(ra, rb):
                    continue
                for sa in _segmentos(ra):
                    for sb in _segmentos(rb):
                        if _se_cruzan(sa, sb):
                            malos.append((j, _punto_de_cruce(sa, sb)))
        return malos

    def tapados(s, margen=1.0):
        """Tramos de cable que pasan por encima de un rotulo.

        Un cable sobre el numero de un pin lo vuelve ilegible, y es un
        defecto que no se ve al escribir las coordenadas: hay que
        mirar la figura. Que lo compruebe la maquina.
        """
        malos = []
        for recorrido, color, _g in s.cables:
            for (x1, y1), (x2, y2) in _segmentos(recorrido):
                for (cx1, cy1, cx2, cy2) in s.protegidas:
                    if abs(y1 - y2) < 0.01:            # tramo horizontal
                        dentro_y = cy1 - margen <= y1 <= cy2 + margen
                        solapa_x = min(x1, x2) < cx2 - margen and \
                            max(x1, x2) > cx1 + margen
                        if dentro_y and solapa_x:
                            malos.append(((x1, y1), (x2, y2),
                                          (cx1, cy1, cx2, cy2)))
                    else:                              # tramo vertical
                        dentro_x = cx1 - margen <= x1 <= cx2 + margen
                        solapa_y = min(y1, y2) < cy2 - margen and \
                            max(y1, y2) > cy1 + margen
                        if dentro_x and solapa_y:
                            malos.append(((x1, y1), (x2, y2),
                                          (cx1, cy1, cx2, cy2)))
        return malos

    def svg(s, ancho, alto):
        """Cierra el dibujo, con un salto en cada cruce.

        Un cruce sin marcar se lee como un empalme. El salto —el
        puentecito de media circunferencia— es la convencion de
        cualquier esquema electrico para decir que los dos cables se
        cruzan sin tocarse.
        """
        saltos = {}
        for idx, punto in s.cruces():
            saltos.setdefault(idx, []).append(punto)

        partes = []
        for pieza in s.piezas:
            if isinstance(pieza, tuple) and pieza[0] == "CABLE":
                i = pieza[1]
                puntos, color, grosor = s.cables[i]
                partes.append(_cable_con_saltos(puntos, color, grosor,
                                                saltos.get(i, [])))
            else:
                partes.append(pieza)
        return envoltura("".join(partes), ancho, alto + 14)


def _punto_de_cruce(a, b):
    """Donde se cortan un tramo horizontal y uno vertical."""
    (ax1, ay1), (ax2, ay2) = a
    if abs(ay1 - ay2) < 0.01:
        return (b[0][0], ay1)
    return (ax1, b[0][1])


def _cable_con_saltos(puntos, color, grosor, saltos, radio=3.6):
    """Traza el cable, levantando un puente en cada cruce marcado."""
    if not saltos:
        return _cable(puntos, color, grosor)

    d = []
    d.append("M %g,%g" % puntos[0])
    for (x1, y1), (x2, y2) in zip(puntos, puntos[1:]):
        horiz = abs(y1 - y2) < 0.01
        # los saltos que caen sobre este tramo, en orden de avance
        en_tramo = []
        for (sx, sy) in saltos:
            if horiz and abs(sy - y1) < 1.5 and min(x1, x2) < sx < max(x1, x2):
                en_tramo.append(sx)
            elif not horiz and abs(sx - x1) < 1.5 and min(y1, y2) < sy < max(y1, y2):
                en_tramo.append(sy)
        en_tramo.sort(reverse=(x2 < x1) if horiz else (y2 < y1))

        for v in en_tramo:
            if horiz:
                signo = 1 if x2 > x1 else -1
                d.append("L %g,%g" % (v - radio * signo, y1))
                d.append("A %g %g 0 0 %d %g,%g"
                         % (radio, radio, 1 if signo > 0 else 0,
                            v + radio * signo, y1))
            else:
                signo = 1 if y2 > y1 else -1
                d.append("L %g,%g" % (x1, v - radio * signo))
                d.append("A %g %g 0 0 %d %g,%g"
                         % (radio, radio, 0 if signo > 0 else 1,
                            x1, v + radio * signo))
        d.append("L %g,%g" % (x2, y2))

    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%g" '
            'stroke-linejoin="round" stroke-linecap="round"/>'
            % (" ".join(d), color, grosor))


def potenciometro(x, y, rotulo="10 kΩ"):
    """Potenciometro visto desde arriba, con sus tres patas.

    Devuelve (svg, extremo1, cursor, extremo3). El cursor es la pata
    del medio, que es la que entrega la tension variable.
    """
    s = []
    s.append('<circle cx="%g" cy="%g" r="18" fill="#3F4750" stroke="%s" '
             'stroke-width="1"/>' % (x, y, PLACA_BORDE))
    s.append('<circle cx="%g" cy="%g" r="12" fill="#9AA4B0"/>' % (x, y))
    # marca de la perilla
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
             'stroke-width="2.4" stroke-linecap="round"/>'
             % (x, y, x + 8, y - 8, "#3F4750"))
    patas = {}
    for dx, nombre in ((-9, "ext1"), (0, "cursor"), (9, "ext3")):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.8" stroke-linecap="round"/>'
                 % (x + dx, y + 18, x + dx, y + 30, GRIS))
        patas[nombre] = (x + dx, y + 30)
    s.append(_txt(x, y - 24, rotulo, 7, TEXTO, "middle"))
    # A la derecha y a la altura del cuerpo: debajo baja el cable del
    # cursor, a la izquierda pasa el carril que lleva la señal al
    # ADC1, y a la altura de las patas entra la alimentacion.
    s.append(_txt(x + 13, y + 20, "cursor", 6, GRIS, "start"))
    return "".join(s), patas["ext1"], patas["cursor"], patas["ext3"]


def servomotor(x, y):
    """Servo SG90 visto desde arriba, con su aspa de cuatro brazos.

    Los tres cables salen por la izquierda con sus colores
    normalizados y terminan en el conector negro, que es como el
    estudiante lo tiene en la mano.

    Devuelve (svg, {"marron": p, "rojo": p, "naranja": p}).
    """
    ANCHO, ALTO = 62, 50
    s = []
    # cuerpo, con las dos orejas de sujecion
    s.append('<rect x="%g" y="%g" width="%g" height="14" rx="2" '
             'fill="#2C6BA8" stroke="%s" stroke-width="1"/>'
             % (x - 9, y + ALTO / 2 - 7, ANCHO + 18, PLACA_BORDE))
    s.append('<circle cx="%g" cy="%g" r="3.4" fill="#F2F5F8" stroke="%s" '
             'stroke-width="0.7"/>' % (x + ANCHO + 4, y + ALTO / 2, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="2.5" '
             'fill="#2C6BA8" stroke="%s" stroke-width="1"/>'
             % (x, y, ANCHO, ALTO, PLACA_BORDE))
    s.append(_txt(x + 15, y + ALTO - 8, "SG90", 7.4, "#DCE6F0", "middle", "bold"))

    # eje y aspa de cuatro brazos
    ex, ey = x + ANCHO - 17, y + ALTO / 2
    for ang in (0, 90, 180, 270):
        import math
        rad = math.radians(ang)
        dx, dy = math.cos(rad), math.sin(rad)
        s.append('<rect x="%g" y="%g" width="22" height="5.5" rx="2.6" '
                 'fill="#E4E9ED" stroke="%s" stroke-width="0.7" '
                 'transform="rotate(%g %g %g)"/>'
                 % (ex, ey - 2.75, PLACA_BORDE, ang, ex, ey))
    s.append('<circle cx="%g" cy="%g" r="9" fill="#E4E9ED" stroke="%s" '
             'stroke-width="0.9"/>' % (ex, ey, PLACA_BORDE))
    s.append('<circle cx="%g" cy="%g" r="2.6" fill="#AEB6BD"/>' % (ex, ey))

    # conector y cables
    cables = {}
    cy0 = y + ALTO / 2 - 11
    s.append('<rect x="%g" y="%g" width="13" height="26" rx="2" '
             'fill="#2B2F35" stroke="%s" stroke-width="0.8"/>'
             % (x - 44, cy0, PLACA_BORDE))
    for i, (nombre, color) in enumerate((("naranja", "#E67E22"),
                                         ("rojo", ROJO),
                                         ("marron", "#5A4632"))):
        py = cy0 + 5 + i * 8
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="3" stroke-linecap="round"/>'
                 % (x - 9, py, x - 31, py, color))
        cables[nombre] = (x - 44, py)
    return "".join(s), cables


def pir(x, y):
    """Sensor PIR HC-SR501 visto desde arriba.

    El domo es la lente de Fresnel, que es lo que el estudiante
    reconoce: el modulo se identifica por esa media esfera blanca
    facetada y no por su placa.

    Devuelve (svg, {"VCC": p, "OUT": p, "GND": p}) con los pines
    saliendo por la izquierda.
    """
    ANCHO, ALTO = 96, 76
    s = []
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="3" '
             'fill="#2E6B4F" stroke="%s" stroke-width="1"/>'
             % (x, y, ANCHO, ALTO, PLACA_BORDE))

    # la lente
    cx, cy, r = x + ANCHO - 30, y + ALTO / 2, 27
    s.append('<circle cx="%g" cy="%g" r="%g" fill="#E9EDF0" stroke="#AEB6BD" '
             'stroke-width="1"/>' % (cx, cy, r))
    s.append('<circle cx="%g" cy="%g" r="%g" fill="#F4F7F9"/>' % (cx, cy, r - 5))
    # facetas: dos anillos de segmentos, como la lente real
    import math
    for anillo, n in ((r - 5, 10), (r - 13, 7)):
        for i in range(n):
            a1 = 2 * math.pi * i / n
            a2 = 2 * math.pi * (i + 1) / n
            s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#C6CED4" '
                     'stroke-width="0.7"/>'
                     % (cx + anillo * math.cos(a1), cy + anillo * math.sin(a1),
                        cx + (anillo - 8) * math.cos(a1),
                        cy + (anillo - 8) * math.sin(a1)))
        s.append('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="#C6CED4" '
                 'stroke-width="0.7"/>' % (cx, cy, anillo))

    s.append(_txt(x + 5, y + ALTO - 6, "HC-SR501", 6.6, "#BEDCCB",
                  "start", "bold"))

    pos = {}
    for i, nombre in enumerate(("VCC", "OUT", "GND")):
        py = y + 19 + i * 19
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.4" stroke-linecap="round"/>'
                 % (x, py, x - 11, py, "#C8CED6"))
        s.append(_txt(x + 5, py + 2.6, nombre, 6.4, "#EAF2ED", "start", "bold"))
        pos[nombre] = (x - 11, py)
    return "".join(s), pos


def hasta_el_anodo(r_der, anodo, separacion=13):
    """Recorrido desde la salida de la resistencia hasta el ánodo.

    Baja por fuera del cuerpo del LED y entra a la pata por el
    costado. Bajar por la vertical del ánodo cruzaría la cúpula y el
    cable quedaría dibujado por encima del componente.
    """
    lane = anodo[0] - separacion
    return [r_der, (lane, r_der[1]), (lane, anodo[1]), anodo]


def dht11(x, y):
    """Módulo DHT11 de tres patas, como el de la caja de componentes.

    Devuelve (svg, {"VCC": p, "DATA": p, "GND": p}).
    """
    ANCHO, ALTO = 40, 54
    s = []
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="2.5" '
             'fill="#3F7FBF" stroke="%s" stroke-width="1"/>'
             % (x, y, ANCHO, ALTO, PLACA_BORDE))
    # la rejilla de la camara de medicion
    for i in range(4):
        for j in range(5):
            s.append('<rect x="%g" y="%g" width="4.5" height="4.5" rx="1" '
                     'fill="#2B5A87"/>' % (x + 7 + i * 7, y + 7 + j * 7))
    s.append(_txt(x + ANCHO / 2, y + ALTO - 5, "DHT11", 6.6, "#DCE8F4",
                  "middle", "bold"))
    pos = {}
    for i, nombre in enumerate(("VCC", "DATA", "GND")):
        px = x + 9 + i * 11
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (px, y + ALTO, px, y + ALTO + 16, GRIS))
        pos[nombre] = (px, y + ALTO + 16)
    s.append(_txt(x - 4, y + ALTO + 10, "VCC", 5.8, GRIS, "end"))
    s.append(_txt(x + ANCHO + 4, y + ALTO + 10, "GND", 5.8, GRIS, "start"))
    cajas = [(x - 20, y + ALTO + 3, x - 3, y + ALTO + 13),
             (x + ANCHO + 3, y + ALTO + 3, x + ANCHO + 20, y + ALTO + 13)]
    return "".join(s), pos, cajas


def enlace_radio(x, y, ancho=96, etiqueta="ESP-NOW"):
    """Símbolo de enlace inalámbrico entre dos placas."""
    import math
    s = []
    for lado in (-1, 1):
        cx = x + ancho / 2 + lado * ancho / 2
        for k in (1, 2, 3):
            r = k * 9
            d = []
            for paso in range(13):
                a = math.radians(-52 + paso * 104 / 12) 
                d.append((cx - lado * r * math.cos(a), y + r * math.sin(a)))
            s.append('<polyline points="%s" fill="none" stroke="%s" '
                     'stroke-width="1.6" opacity="%.2f"/>'
                     % (" ".join("%g,%g" % p for p in d), SENAL,
                        0.9 - 0.2 * k))
    # En el hueco entre las dos antenas y no encima: arriba pasa el
    # riel de masa de la placa de la izquierda.
    s.append(_txt(x + ancho / 2, y + 3, etiqueta, 7.6, SENAL, "middle", "bold"))
    s.append(_txt(x + ancho / 2, y + 30, "sin red ni router", 6.4, GRIS,
                  "middle", inclinada=True))
    return "".join(s)


def to92(x, y, etiqueta="LM35", patas=("izq", "centro", "der")):
    """Encapsulado TO-92 visto de frente, con la cara plana adelante.

    Es como el estudiante lo va a mirar para identificar sus patas, y
    por eso se dibuja la cara plana y no una vista de arriba.

    Devuelve (svg, [p1, p2, p3]) de izquierda a derecha.
    """
    R = 15
    s = []
    s.append('<path d="M %g %g a %g %g 0 0 1 %g 0 l 0 %g l %g 0 z" '
             'fill="#2B2F35" stroke="%s" stroke-width="0.9"/>'
             % (x - R, y, R, R, 2 * R, R + 4, -2 * R, PLACA_BORDE))
    # la cara plana, marcada con una linea vertical del mismo tono
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#4A5058" '
             'stroke-width="1.2"/>' % (x - R, y, x - R, y + R + 4))
    s.append(_txt(x, y + 11, etiqueta, 6.8, "#DDE3E9", "middle", "bold"))

    puntos = []
    for i, dx in enumerate((-8, 0, 8)):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2" stroke-linecap="round"/>'
                 % (x + dx, y + R + 4, x + dx, y + R + 34, GRIS))
        puntos.append((x + dx, y + R + 34))
    s.append(_txt(x, y - R - 6, "cara plana al frente", 6, GRIS, "middle",
                  inclinada=True))
    return "".join(s), puntos


def termistor(x, y, etiqueta="NTC 100 k"):
    """Termistor de perla con sus dos patas hacia abajo."""
    s = []
    s.append('<ellipse cx="%g" cy="%g" rx="9" ry="11" fill="#1F2A24" '
             'stroke="%s" stroke-width="0.9"/>' % (x, y, PLACA_BORDE))
    s.append('<ellipse cx="%g" cy="%g" rx="3" ry="4" fill="#3C4A42"/>'
             % (x - 3, y - 3))
    for dx in (-5, 5):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2" stroke-linecap="round"/>'
                 % (x + dx, y + 9, x + dx, y + 34, GRIS))
    # Al costado y no encima: por encima del termistor baja el cable
    # que trae la señal del punto medio del divisor.
    s.append(_txt(x + 13, y + 2, etiqueta, 7, TEXTO, "start"))
    return "".join(s), (x - 5, y + 34), (x + 5, y + 34)


def condensador(x, y, etiqueta="100 nF"):
    """Condensador ceramico de disco, con sus dos patas hacia abajo."""
    s = []
    s.append('<path d="M %g %g a 11 9 0 1 1 22 0 z" fill="#C9822A" '
             'stroke="%s" stroke-width="0.9"/>' % (x - 11, y, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="22" height="3" fill="#C9822A" '
             'stroke="%s" stroke-width="0.7"/>' % (x - 11, y, PLACA_BORDE))
    for dx in (-5, 5):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.8" stroke-linecap="round"/>'
                 % (x + dx, y + 3, x + dx, y + 26, GRIS))
    s.append(_txt(x, y - 12, etiqueta, 6.6, TEXTO, "middle"))
    return "".join(s), (x - 5, y + 26), (x + 5, y + 26)


def motor_cc(x, y, etiqueta="motor"):
    """Motor de corriente continua, visto de costado."""
    s = []
    s.append('<rect x="%g" y="%g" width="52" height="40" rx="6" '
             'fill="#5A6470" stroke="%s" stroke-width="1"/>'
             % (x, y, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="10" height="14" rx="2" '
             'fill="#8A9199" stroke="%s" stroke-width="0.8"/>'
             % (x + 52, y + 13, PLACA_BORDE))
    s.append('<circle cx="%g" cy="%g" r="13" fill="none" stroke="#9AA4B0" '
             'stroke-width="1.4"/>' % (x + 26, y + 20))
    s.append(_txt(x + 26, y + 24, "M", 13, "#E8EDF2", "middle", "bold"))
    s.append(_txt(x + 26, y - 7, etiqueta, 7, TEXTO, "middle"))
    bornes = {}
    for i, (dy, nombre) in enumerate(((11, "a"), (29, "b"))):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (x, y + dy, x - 12, y + dy, GRIS))
        bornes[nombre] = (x - 12, y + dy)
    return "".join(s), bornes


def disco_ranurado(x, y):
    """Sensor optico de ranura con el disco de marcas pasando por el medio."""
    s = []
    # la horquilla
    s.append('<rect x="%g" y="%g" width="14" height="46" rx="2" '
             'fill="#2B2F35" stroke="%s" stroke-width="0.9"/>'
             % (x, y, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="14" height="46" rx="2" '
             'fill="#2B2F35" stroke="%s" stroke-width="0.9"/>'
             % (x + 34, y, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="48" height="12" rx="2" '
             'fill="#2B2F35" stroke="%s" stroke-width="0.9"/>'
             % (x, y + 46, PLACA_BORDE))
    # el disco, entrando por la ranura
    import math
    cx, cy, r = x + 24, y + 20, 30
    s.append('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="#9AA4B0" '
             'stroke-width="1.6" stroke-dasharray="3,4"/>' % (cx, cy, r))
    for k in range(4):
        a = math.radians(k * 90 + 20)
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#C9A227" '
                 'stroke-width="2.4"/>'
                 % (cx + (r - 9) * math.cos(a), cy + (r - 9) * math.sin(a),
                    cx + r * math.cos(a), cy + r * math.sin(a)))
    s.append(_txt(cx, cy - r - 8, "disco de 4 marcas", 6.6, TEXTO, "middle"))
    pos = {}
    # El orden de las patas es GND, OUT, VCC de izquierda a derecha:
    # asi el riel de masa sale por el lado en que esta el riel y no
    # tiene que cruzar por delante de las otras dos.
    for i, nombre in enumerate(("GND", "OUT", "VCC")):
        px = x + 8 + i * 16
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (px, y + 58, px, y + 76, GRIS))
        pos[nombre] = (px, y + 76)
    # Pegados al cuerpo y no a media pata: por media pata pasan los
    # cables que vienen de la placa.
    s.append(_txt(x - 4, y + 62, "GND", 5.8, GRIS, "end"))
    s.append(_txt(x + 52, y + 62, "VCC", 5.8, GRIS, "start"))
    cajas = [(x - 20, y + 55, x - 3, y + 65),
             (x + 51, y + 55, x + 68, y + 65)]
    return "".join(s), pos, cajas


def oled(x, y, texto=("TABLERO", "Amb 23.4C 55%")):
    """Pantalla OLED de 128x64 con sus cuatro patas de I2C."""
    ANCHO, ALTO = 96, 58
    s = []
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="3" '
             'fill="#1B2430" stroke="%s" stroke-width="1"/>'
             % (x, y, ANCHO, ALTO, PLACA_BORDE))
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="1" '
             'fill="#0A0E14"/>' % (x + 6, y + 5, ANCHO - 12, ALTO - 22))
    for i, linea in enumerate(texto[:3]):
        s.append(_txt(x + ANCHO / 2, y + 16 + i * 10, linea, 6.4, "#5FE3F0",
                      "middle"))
    s.append(_txt(x + ANCHO / 2, y + ALTO - 5, "OLED 128x64", 6, "#8A9199",
                  "middle"))
    pos = {}
    cajas = []
    for i, nombre in enumerate(("GND", "VCC", "SCL", "SDA")):
        px = x + 16 + i * 21
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (px, y + ALTO, px, y + ALTO + 18, GRIS))
        # El rotulo va al COSTADO de la pata y no debajo: debajo
        # pasan los cuatro cables y lo tapaban.
        s.append(_txt(px - 4, y + ALTO + 12, nombre, 5.8, GRIS, "end"))
        pos[nombre] = (px, y + ALTO + 18)
        cajas.append((px - 16, y + ALTO + 6, px - 3, y + ALTO + 15))
    return "".join(s), pos, cajas


def modulo_rele(x, y):
    """Modulo de rele de un canal, de los rojos con optoacoplador.

    Se dibujan las tres piezas que el estudiante tiene que reconocer
    para no equivocarse: la bornera de tres tornillos del lado de la
    carga, el rele encapsulado con su tension de bobina impresa, y el
    puente H/L que decide si el modulo dispara con nivel alto o bajo.

    Devuelve (svg, mando, carga, cajas): 'mando' son las patas del
    lado de baja tension y 'carga' los tornillos de la bornera.
    """
    ANCHO, ALTO = 112, 74
    s = []
    s.append('<rect x="%g" y="%g" width="%g" height="%g" rx="3" '
             'fill="#8E2B22" stroke="%s" stroke-width="1"/>'
             % (x, y, ANCHO, ALTO, PLACA_BORDE))

    # el rele encapsulado
    s.append('<rect x="%g" y="%g" width="40" height="30" rx="2" '
             'fill="#2A4C8A" stroke="%s" stroke-width="0.8"/>'
             % (x + 40, y + 30, PLACA_BORDE))
    s.append(_txt(x + 60, y + 44, "12 V", 6.4, "#DCE6F5", "middle", "bold"))
    s.append(_txt(x + 60, y + 52, "10 A 250 V~", 5.2, "#B8C6DE", "middle"))

    # el optoacoplador, que es lo que separa los dos lados
    s.append('<rect x="%g" y="%g" width="16" height="22" rx="1.5" '
             'fill="#1B2430"/>' % (x + 16, y + 34))
    s.append(_txt(x + 24, y + 62, "opto", 5.2, "#E8C9C5", "middle"))

    # el puente H/L
    s.append('<rect x="%g" y="%g" width="20" height="9" rx="1.5" '
             'fill="#1B2430"/>' % (x + 8, y + 8))
    s.append(_txt(x + 18, y + 15, "H | L", 5.4, "#F0D9A0", "middle", "bold"))

    s.append(_txt(x + ANCHO - 6, y + 14, "MÓDULO DE RELÉ", 6.4, "#F3DEDB",
                  "end", "bold"))

    # --- lado de mando, tres patas hacia abajo
    mando, cajas = {}, []
    for i, nombre in enumerate(("IN", "GND", "VCC")):
        px = x + 24 + i * 30
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (px, y + ALTO, px, y + ALTO + 18, GRIS))
        s.append(_txt(px - 4, y + ALTO + 12, nombre, 5.8, GRIS, "end"))
        mando[nombre] = (px, y + ALTO + 18)
        cajas.append((px - 20, y + ALTO + 6, px - 3, y + ALTO + 15))

    # --- bornera de la carga, arriba: NC, COM, NA
    carga = {}
    for i, nombre in enumerate(("NC", "COM", "NA")):
        bx = x + 14 + i * 32
        s.append('<rect x="%g" y="%g" width="26" height="16" rx="2" '
                 'fill="#2B6BA8" stroke="%s" stroke-width="0.8"/>'
                 % (bx, y - 16, PLACA_BORDE))
        s.append('<circle cx="%g" cy="%g" r="3.5" fill="#C8CED6"/>'
                 % (bx + 13, y - 11))
        # El rotulo va DENTRO de la bornera, debajo del tornillo: por
        # encima llegan los cables de la red y lo tapaban.
        s.append(_txt(bx + 13, y - 2.5, nombre, 5, "#DCE6F5", "middle",
                      "bold"))
        carga[nombre] = (bx + 13, y - 16)
    return "".join(s), mando, carga, cajas


def foco(x, y, etiqueta="foco 220 V~"):
    """Lampara incandescente, con sus dos bornes hacia abajo."""
    R = 17
    s = []
    s.append('<path d="M %g %g a %g %g 0 1 1 %g 0 z" fill="#F2D06B" '
             'stroke="%s" stroke-width="1"/>'
             % (x - R, y + 6, R, R, 2 * R, PLACA_BORDE))
    s.append('<path d="M %g %g q 5 -12 10 0" fill="none" stroke="#8A6A18" '
             'stroke-width="1.2"/>' % (x - 5, y + 2))
    # el casquillo
    for k in range(3):
        s.append('<rect x="%g" y="%g" width="20" height="4" rx="1" '
                 'fill="#B9BFC7" stroke="%s" stroke-width="0.5"/>'
                 % (x - 10, y + 7 + k * 5, PLACA_BORDE))
    for dx in (-6, 6):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2" stroke-linecap="round"/>'
                 % (x + dx, y + 21, x + dx, y + 40, GRIS))
    s.append(_txt(x + 24, y - 2, etiqueta, 6.6, TEXTO, "start"))
    return "".join(s), (x - 6, y + 40), (x + 6, y + 40)


def toma_red(x, y, etiqueta="red 220 V~"):
    """Toma de la red domiciliaria: la fuente de peligro del montaje."""
    s = []
    s.append('<rect x="%g" y="%g" width="34" height="26" rx="4" '
             'fill="#3A3F46" stroke="%s" stroke-width="1"/>'
             % (x, y, PLACA_BORDE))
    for dx in (11, 23):
        s.append('<circle cx="%g" cy="%g" r="3.4" fill="#0A0E14"/>'
                 % (x + dx, y + 11))
    s.append(_txt(x + 17, y + 36, etiqueta, 6.4, TEXTO, "middle", "bold"))
    return "".join(s), (x + 11, y), (x + 23, y)


def fuente(x, y, etiqueta="12 V"):
    """Fuente de continua aparte, la que alimenta la bobina del rele."""
    s = []
    s.append('<rect x="%g" y="%g" width="46" height="30" rx="3" '
             'fill="#455160" stroke="%s" stroke-width="1"/>'
             % (x, y, PLACA_BORDE))
    s.append(_txt(x + 23, y + 13, etiqueta, 7.4, "#E8EDF2", "middle", "bold"))
    s.append(_txt(x + 23, y + 23, "continua", 5.4, "#B4BDC8", "middle"))
    # El negativo va a la izquierda porque en los diagramas de este
    # libro la masa baja al riel, que esta del lado izquierdo, y el
    # positivo sube por fuera: al reves, los dos cables se cruzaban.
    for dx, signo in ((13, "−"), (33, "+")):
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="2.2" stroke-linecap="round"/>'
                 % (x + dx, y + 30, x + dx, y + 46, GRIS))
        s.append(_txt(x + dx, y + 42, signo, 7, TEXTO, "middle", "bold"))
    return "".join(s), (x + 33, y + 46), (x + 13, y + 46)
