# -*- coding: utf-8 -*-
"""Los diagramas de conexión del capítulo 2, sobre la placa real.

Las patas ya no están donde conviene al dibujo sino donde están en la
placa: GPIO23 arriba a la derecha, GPIO5 por encima de GPIO4, VIN abajo
a la izquierda. Los recorridos salen más largos que con una placa
esquemática, y eso es justamente lo que el estudiante va a ver sobre la
protoboard.

Cada figura se arma con circuitos.Dibujo, que además comprueba que
ningún cable cruce a otro: en un diagrama de conexión un cruce se lee
como un empalme, y a mano se escapan.
"""
import circuitos as C

LIENZO = 440
X_PLACA, Y_PLACA = 96, 26
COL_A = 290          # primera columna de componentes
COL_B = 366          # segunda columna
Y_NOTA = 13
LANE_GND = 244
LANE_IZQ = 24        # por fuera de los rotulos, que
                     # llegan hasta x = 94       # por donde sube el riel hasta la pata GND


def _riel(alto):
    return Y_PLACA + alto + 38


def _nota(d, texto):
    d.texto(LIENZO / 2 + 40, Y_NOTA, texto, 6.6, C.GRIS, "middle",
            inclinada=True)


# =============================================================== 2.1
def lab_2_1():
    d = C.Dibujo("2.1")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA, {"GPIO23", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)
    y = pin["GPIO23"][1]

    r, r_izq, r_der = C.resistencia(COL_A, y, "330", rotulo="330 Ω")
    d.add(r)
    l, anodo, catodo = C.led(COL_B + 10, y + 26)
    d.add(l)

    # el LED va de pie: la resistencia entra por arriba y baja al
    # ánodo, y el cátodo cae directo al riel de masa
    d.cable([pin["GPIO23"], r_izq], C.SENAL)
    d.cable(C.hasta_el_anodo(r_der, anodo), C.SENAL)
    d.cable([catodo, (catodo[0], riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "la resistencia puede ir de cualquiera de los dos lados")
    return d


# =============================================================== 2.2
def lab_2_2():
    d = C.Dibujo("2.2")
    cuerpo, pin, alto, cajas = C.placa_real(
        X_PLACA, Y_PLACA, {"GPIO23", "GPIO21", "GPIO17", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)

    # Los tres LED van en fila, de pie, bien por debajo de las
    # resistencias. El de la pata mas alta ocupa el carril mas a la
    # derecha: asi los tres cables bajan sin cruzarse entre si.
    Y_LED = 176
    # El LED de abajo se alinea con la salida de su resistencia: puesto
    # mas a la izquierda, su cable volvia sobre la resistencia y se le
    # dibujaba encima.
    filas = (("GPIO23", "#C0392B", "rojo", 424, C.SENAL),
             ("GPIO21", "#E8C31E", "amarillo", 372, C.NARANJA),
             ("GPIO17", "#2E8B57", "verde", 320, C.VIOLETA))

    for nombre, color, etiqueta, lx, tinta in filas:
        y = pin[nombre][1]
        r, r_izq, r_der = C.resistencia(268, y, "330")
        d.add(r)
        l, anodo, catodo = C.led(lx, Y_LED, color, rotular=False)
        d.add(l)
        d.cable([pin[nombre], r_izq], tinta)
        d.cable(C.hasta_el_anodo(r_der, anodo), tinta)
        d.cable([catodo, (catodo[0], riel)], C.NEGRO)
        d.nodo(catodo[0], riel, C.NEGRO)
        d.texto(lx, Y_LED - 22, etiqueta, 7, C.TEXTO, "middle")

    d.cable([(424 + 5, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "una resistencia de 330 Ω y un pin distinto para cada luz")
    return d


# =============================================================== 2.3
def lab_2_3():
    d = C.Dibujo("2.3")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"GPIO16", "GPIO5", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)
    y16, y5 = pin["GPIO16"][1], pin["GPIO5"][1]

    # GPIO5 está por encima de GPIO16 en la placa, así que el LED va
    # arriba y el pulsador abajo: siguiendo el orden de las patas, los
    # cables no necesitan cruzarse.
    r, r_izq, r_der = C.resistencia(276, y5, "330", rotulo="330 Ω")
    d.add(r)
    l, anodo, catodo = C.led(398, y5 + 24, rotular=False)
    d.add(l)
    d.cable([pin["GPIO5"], r_izq], C.SENAL)
    d.cable(C.hasta_el_anodo(r_der, anodo), C.SENAL)
    d.cable([catodo, (catodo[0], riel)], C.NEGRO)
    d.nodo(catodo[0], riel, C.NEGRO)

    # El pulsador va en su propia fila, a la altura de GPIO16 y bien
    # separado de la resistencia: antes se le montaba encima y tapaba
    # el valor impreso.
    # El pulsador queda a la derecha de la resistencia y su rótulo
    # va debajo: encima se le montaba al valor impreso de 330 Ω.
    bx, by = 322, y16 - 15
    b, patas = C.pulsador(bx, by)
    d.add(b)
    d.texto(bx + 15, by + 44, "pulsador", 7, C.TEXTO, "middle")
    d.cable([pin["GPIO16"], (292, y16), (292, patas["a1"][1]),
             patas["a1"]], C.NARANJA)
    d.cable([patas["b1"], (424, patas["b1"][1]), (424, riel)], C.NEGRO)
    d.nodo(424, riel, C.NEGRO)

    d.cable([(424, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "las patas de un mismo lado están unidas de fábrica: "
             "tome una de cada lado")
    return d


# =============================================================== 2.4
def lab_2_4():
    d = C.Dibujo("2.4")
    cuerpo, pin, alto, cajas = C.placa_real(X_PLACA, Y_PLACA,
                                     {"VIN", "GPIO4", "GPIO5", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)
    y5, y4 = pin["GPIO5"][1], pin["GPIO4"][1]

    # ---- zumbador arriba, a la altura de GPIO5
    zx, zy = 286, y5 - 34
    d.add('<circle cx="%g" cy="%g" r="22" fill="#3A3F46" stroke="%s" '
          'stroke-width="1"/>' % (zx, zy, C.PLACA_BORDE))
    d.add('<circle cx="%g" cy="%g" r="5" fill="#20242A"/>' % (zx, zy))
    d.texto(zx - 10, zy - 4, "+", 11, "#E8EDF2", "middle", "bold",
            serigrafia=True)
    d.texto(zx, zy - 31, "zumbador pasivo", 7, C.TEXTO, "middle")
    mas, menos = (zx - 8, zy + 22), (zx + 8, zy + 22)

    # ---- módulo PIR abajo, a la altura de GPIO4
    m, mp = C.pir(330, y4 + 8)
    d.add(m)

    # Cada red con su color: la señal del PIR en azul, la del zumbador
    # en naranja, la alimentación en rojo y la masa en negro. Asi los
    # recorridos se siguen sin depender de cual pasa por encima.
    d.cable([pin["GPIO4"], (262, y4), (262, mp["OUT"][1]), mp["OUT"]],
            C.SENAL)
    d.cable([pin["GPIO5"], (250, y5), (250, mas[1] + 10),
             (mas[0], mas[1] + 10), mas], C.NARANJA)

    d.cable([menos, (menos[0], menos[1] + 8), (322, menos[1] + 8),
             (322, riel)], C.NEGRO)
    d.nodo(322, riel, C.NEGRO)
    d.cable([mp["GND"], (306, mp["GND"][1]), (306, riel)], C.NEGRO)
    d.nodo(306, riel, C.NEGRO)

    # VIN sale por el lado opuesto de la placa: rodea por abajo y sube
    # por fuera del módulo hasta VCC.
    # Sube por fuera del módulo y entra a VCC desde arriba: llevada
    # directo a la altura de VCC, la línea roja cruzaba el cuerpo del
    # sensor de lado a lado.
    d.cable([pin["VIN"], (LANE_IZQ, pin["VIN"][1]), (LANE_IZQ, riel + 22),
             (436, riel + 22), (436, 166), (312, 166),
             (312, mp["VCC"][1]), mp["VCC"]], C.ROJO)

    d.cable([(322, riel), (LANE_GND, riel),
             (LANE_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)

    _nota(d, "el PIR se alimenta con 5 V (VIN), que está del otro lado "
             "de la placa")
    return d



# =============================================================== 2.5
def lab_2_5():
    """El modulo de rele gobernado por un pulsador. Solo el mando."""
    d = C.Dibujo("2.5")
    # Los tres pines de este montaje estan en la columna DERECHA, de
    # modo que a la izquierda de la placa no hay nada que dibujar. Con
    # el origen habitual la figura ocupaba las tres cuartas partes
    # derechas del lienzo y en la pagina salia un 20% mas chica que
    # las demas. Aqui la placa arranca pegada al borde y el lienzo se
    # recorta a la medida del dibujo.
    X, Y = 16, Y_PLACA
    cuerpo, pin, alto, cajas = C.placa_real(X, Y,
                                            {"GPIO19", "GPIO16", "GND"})
    d.add(cuerpo, cajas)
    riel = _riel(alto)
    y19, y16 = pin["GPIO19"][1], pin["GPIO16"][1]
    CARRIL_GND = 164              # el riel sube por fuera de los rotulos

    # ---- el modulo de rele, arriba a la derecha
    m, mando, carga, cajas_m = C.modulo_rele(196, 52)
    d.add(m, cajas_m)

    # ---- el pulsador, a la altura de GPIO16
    bx, by = 196, 186
    b, patas = C.pulsador(bx, by)
    d.add(b)
    d.texto(bx + 15, by + 44, "pulsador", 7, C.TEXTO, "middle")

    # ---- la fuente de la bobina, que no sale de la placa
    f, mas, menos = C.fuente(272, 200, "12 V")
    d.add(f)

    # la orden: un solo cable de mando
    d.cable([pin["GPIO19"], (182, y19), (182, 162), (mando["IN"][0], 162),
             mando["IN"]], C.SENAL)

    # el pulsador contra masa, igual que en el 2.3
    d.cable([pin["GPIO16"], (176, y16), (176, patas["a1"][1]),
             patas["a1"]], C.NARANJA)
    d.cable([patas["b1"], (patas["b1"][0], riel)], C.NEGRO)
    d.nodo(patas["b1"][0], riel, C.NEGRO)

    # La masa comun, que es el punto del laboratorio: la placa, el
    # modulo y la fuente cuelgan todos del mismo riel. El riel se traza
    # entero, de la fuente hasta la pata GND, y cada bajada se le une
    # con un nodo.
    d.cable([mando["GND"], (mando["GND"][0], riel)], C.NEGRO)
    d.nodo(mando["GND"][0], riel, C.NEGRO)
    d.cable([menos, (menos[0], riel), (CARRIL_GND, riel),
             (CARRIL_GND, pin["GND"][1]), pin["GND"]], C.NEGRO)
    d.nodo(menos[0], riel, C.NEGRO)

    # los 12 V de la bobina rodean la fuente por fuera
    d.cable([mas, (mas[0], 258), (340, 258), (340, 166),
             (mando["VCC"][0], 166), mando["VCC"]], C.ROJO)

    d.texto(176, Y_NOTA, "la bobina se alimenta de su propia fuente; "
            "lo único que sale de la placa es la orden",
            6.6, C.GRIS, "middle", inclinada=True)
    return d


# =============================================================== 2.6
def lab_2_6():
    """El lado de la carga: el contacto, el foco y la red."""
    d = C.Dibujo("2.6")
    # La toma va a la IZQUIERDA y el foco a la derecha, con el modulo
    # en el medio. Puesta la toma a la derecha, el cable de vuelta
    # tenia que cruzar el que sale por NA: el circuito es un lazo, y
    # el lazo se cierra por fuera o se cruza.
    t, izq, der = C.toma_red(40, 96)
    d.add(t)
    neutro, fase = izq, der
    d.texto(neutro[0] - 4, 88, "N", 6, C.GRIS, "end", "bold")
    d.texto(fase[0] + 4, 88, "F", 6, C.ROJO, "start", "bold")
    m, mando, carga, cajas_m = C.modulo_rele(150, 150)
    d.add(m, cajas_m)
    l, foco_a, foco_b = C.foco(330, 52)
    d.add(l)

    # La FASE es la que entra por COM: el rele tiene que cortar el
    # conductor vivo. Cortando el neutro la lampara se apaga igual,
    # pero queda con tension en el portalamparas.
    d.cable([fase, (fase[0], 76), (carga["COM"][0], 76),
             carga["COM"]], C.ROJO)
    # y sale por NA hacia el foco: NA sólo conduce con el rele activado
    d.cable([carga["NA"], (carga["NA"][0], 98), (foco_a[0], 98),
             foco_a], C.ROJO)
    # el neutro vuelve por arriba, sin cruzar nada
    d.cable([foco_b, (406, foco_b[1]), (406, 26), (neutro[0], 26),
             neutro], C.NEGRO)

    d.texto(carga["NC"][0], 126, "NC: sin usar", 6, C.GRIS, "middle")

    # La frontera. Va pegada al borde inferior del modulo porque la
    # separacion de verdad esta adentro, en el optoacoplador: de la
    # bornera para arriba todo esta a 220 V, y las tres patas de abajo
    # no lo estan nunca.
    d.add('<line x1="6" y1="228" x2="434" y2="228" stroke="%s" '
          'stroke-width="1.2" stroke-dasharray="6,4"/>' % C.GRIS)
    d.texto(138, 216, "de aquí para arriba, 220 V~", 7.4,
            C.TEXTO, "end", "bold")
    d.texto(138, 246, "abajo, el mando (figura 2.5)",
            6.6, C.GRIS, "end", inclinada=True)
    return d


TODOS = {"lab_2_1": lab_2_1, "lab_2_2": lab_2_2,
         "lab_2_3": lab_2_3, "lab_2_4": lab_2_4,
         "lab_2_5": lab_2_5, "lab_2_6": lab_2_6}

ALTOS = {"lab_2_1": 44, "lab_2_2": 44, "lab_2_3": 44, "lab_2_4": 58,
         "lab_2_5": 24, "lab_2_6": 0}


# El 2.6 no lleva placa: su alto es absoluto y no se mide desde ella.
ALTO_FIJO = {"lab_2_6": 268}
# El 2.5 dibuja solo la mitad derecha de la retícula comun.
ANCHO_FIJO = {"lab_2_5": 356}


def svg(nombre):
    d = TODOS[nombre]()
    ancho = ANCHO_FIJO.get(nombre, LIENZO)
    if nombre in ALTO_FIJO:
        return d.svg(ancho, ALTO_FIJO[nombre]), len(d.cruces())
    _c, _p, alto, _cj = C.placa_real(X_PLACA, Y_PLACA, set())
    return d.svg(ancho, _riel(alto) + ALTOS[nombre]), len(d.cruces())
