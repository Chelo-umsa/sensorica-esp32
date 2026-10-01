# -*- coding: utf-8 -*-
"""Capítulo 3 — Señales analógicas."""
from maqueta import (capitulo, lab, sec, codigo, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import circuitos_cap3 as CIR

PARTES = []
A = PARTES.append

A(capitulo(3, "Señales analógicas", p(
    "Una señal digital sólo dice sí o no. La mayoría de las magnitudes "
    "físicas no se dejan describir así: una temperatura no está «presente o "
    "ausente», vale 23,4 °C. Lo mismo la presión, el caudal, la posición de "
    "un pedal, el nivel de un tanque. Esas magnitudes llegan al "
    "microcontrolador como una <b>tensión continua</b> que varía con la "
    "medición, y traducirla a un número es el trabajo de este capítulo.",

    "El camino tiene tres tramos y conviene no confundirlos. Primero el "
    "sensor convierte la magnitud en tensión; después hay que acondicionar "
    "esa tensión para que entre sin riesgo en el pin; y recién entonces el "
    "conversor la vuelve un número, que todavía no está en las unidades "
    "que interesan. Los cinco laboratorios recorren esos tres tramos, y el "
    "último —la calibración— es el que separa una lectura que parece "
    "correcta de una que lo es.")))

# =================================================================== 3.1
A(lab("3.1", "Leer una tensión: el potenciómetro"))

A(sec("Objetivo"))
A(p("Convertir la posición de una perilla en un número, y entender qué "
    "significan los dos ajustes del conversor."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["1", "Potenciómetro de 10 kΩ"], ["—", "Cables de conexión"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_3_1")[0], ancha=True, epigrafe=
         "El potenciómetro con sus dos extremos entre 3V3 y masa. El cursor "
         "—la pata del medio— entrega la tensión, y va a GPIO34, que "
         "pertenece al ADC1 y está en la columna izquierda de la placa.",
         capitulo=3))

A(aviso("Por qué todos los sensores de este libro van al ADC1", p(
    "El ESP32 tiene dos conversores. El <b>ADC1</b> ocupa los pines GPIO32 a "
    "GPIO39; el <b>ADC2</b>, los GPIO 0, 2, 4, 12 a 15 y 25 a 27. La "
    "diferencia es que <b>el ADC2 deja de funcionar cuando el WiFi está "
    "encendido</b>, porque la radio lo usa internamente.",
    "En este capítulo todavía no hay WiFi y el ADC2 andaría. Pero en el "
    "capítulo 7 estos mismos montajes van a publicar su lectura en internet, "
    "y entonces dejarían de medir. Cablearlos al ADC1 desde ahora ahorra "
    "rehacer el montaje después, y es el motivo de que en los cuatro "
    "diagramas de este capítulo el cable de señal cruce al otro lado de la "
    "placa.")))

A(sec("Razonamiento"))

A(p(
    "El conversor tiene dos ajustes y los dos hacen falta.",

    "La <b>resolución</b> dice en cuántos escalones se parte el rango. Con "
    "<code>WIDTH_12BIT</code> son 4096 escalones, de 0 a 4095, que es lo "
    "máximo que da el ESP32.",

    "La <b>atenuación</b> dice cuál es el rango. Ésta es la que sorprende: el "
    "conversor no mide de 0 a 3,3 V por defecto, sino hasta poco más de 1 V. "
    "Para abarcar los 3,3 V hay que pedir <code>ATTN_11DB</code> "
    "explícitamente. Sin esa línea, la lectura satura en 4095 apenas pasa de "
    "1,1 V y parece que el sensor estuviera roto."))

A(tabla(
    ["Atenuación", "Abarca hasta", "Cuándo conviene"],
    [["<code>ATTN_0DB</code>", "≈ 1,1 V",
      "Señales muy chicas. Máxima resolución sobre un tramo angosto."],
     ["<code>ATTN_2_5DB</code>", "≈ 1,5 V", "Poco usada."],
     ["<code>ATTN_6DB</code>", "≈ 2,0 V",
      "El LM35 del laboratorio 3.3, que no pasa de 1 V."],
     ["<code>ATTN_11DB</code>", "≈ 3,3 V",
      "El caso general, y el que usa este libro salvo aviso."]],
    centradas=(0, 1)))

A(p(
    "La conversión a voltios es una regla de tres: si 4095 cuentas "
    "corresponden a 3,3 V, entonces <i>n</i> cuentas corresponden a "
    "<code>n × 3,3 / 4095</code>. Nada más."))

A(sec("Programa"))

A(codigo("""from machine import Pin, ADC
import time

# El ADC1 corresponde a los pines GPIO32 a GPIO39. Ver el recuadro.
PIN_ENTRADA = 34

TENSION_MAXIMA = 3.3      # con atenuacion de 11 dB
CUENTAS_MAXIMAS = 4095    # con resolucion de 12 bits

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)      # rango de entrada de 0 a 3,3 V
entrada.width(ADC.WIDTH_12BIT)    # resolucion de 12 bits


def leer_tension():
    \"\"\"Devuelve las cuentas crudas y su equivalente en voltios.\"\"\"
    cuentas = entrada.read()
    return cuentas, cuentas * TENSION_MAXIMA / CUENTAS_MAXIMAS


def main():
    print("Gire la perilla del potenciometro.")
    print("")
    print("  cuentas   tension     barra")

    while True:
        cuentas, tension = leer_tension()

        # una barra de veinticuatro posiciones para ver la variacion
        largo = int(cuentas * 24 / CUENTAS_MAXIMAS)
        barra = "#" * largo + "." * (24 - largo)

        print("   {:5d}    {:5.3f} V    {}".format(
            cuentas, tension, barra))
        time.sleep(0.5)


if __name__ == "__main__":
    main()""", archivo="lab_3_1_potenciometro.py"))

A(sec("Qué debe observarse"))

A(consola("""  cuentas   tension     barra
       0    0.000 V    ........................
    1024    0.825 V    ######..................
    2048    1.650 V    ############............
    4095    3.300 V    ########################"""))

A(p(
    "Girando la perilla de un extremo al otro las cuentas recorren todo el "
    "rango y la barra se llena. Con la perilla quieta, la lectura no se queda "
    "del todo fija: baila unas pocas cuentas. Eso es ruido del propio "
    "conversor y no un defecto del montaje; el laboratorio 3.5 se ocupa de "
    "él."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Marca 4095 casi siempre",
      "Falta <code>atten(ADC.ATTN_11DB)</code>: el conversor satura por "
      "encima de 1,1 V."],
     ["No baja de unas 100 cuentas ni sube de 4000",
      "Uno de los dos extremos del potenciómetro no está conectado."],
     ["La lectura no cambia al girar",
      "El cursor no es la pata que se cableó. Es la del medio."],
     ["Salta sola entre valores muy distintos",
      "Mal contacto en la protoboard, o se usó un pin del ADC2 con el WiFi "
      "encendido."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, el potenciómetro es el mando manual "
    "de consigna de un variador de velocidad, y la misma lectura sirve para "
    "cualquier sensor con salida de 0 a 10 V previo acondicionamiento —que es "
    "el laboratorio siguiente.",
    "<b>En el área mecánica</b>, es exactamente el sensor de posición del "
    "acelerador: un potenciómetro solidario al pedal. El programa que lee la "
    "perilla y el que lee el pedal son el mismo.")))

# =================================================================== 3.2
A(lab("3.2", "Señales de 5 V: el divisor de tensión"))

A(sec("Objetivo"))
A(p("Leer una señal que llega con más tensión de la que el pin admite, sin "
    "dañar la placa."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["1", "Potenciómetro de 10 kΩ, como fuente de señal variable"],
         ["1", "Resistencia de 10 kΩ (R1)"],
         ["1", "Resistencia de 15 kΩ (R2)"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_3_2")[0], ancha=True, epigrafe=
         "El potenciómetro alimentado con los 5 V de VIN hace de sensor de "
         "5 V. R1 y R2 forman el divisor, y el punto entre las dos es lo "
         "único que entra al conversor.", capitulo=3))

A(aviso("El pin no tolera 5 V", p(
    "Los pines del ESP32 trabajan con 3,3 V. Aplicarles 5 V los daña, a veces "
    "de inmediato y a veces despacio, que es peor porque el equipo empieza a "
    "fallar semanas después.",
    "Muchos sensores industriales entregan de 0 a 10 V y muchos sensores de "
    "vehículo trabajan con 5 V. Conectarlos directamente no es una opción: "
    "hay que bajar la tensión primero, y eso es lo que hace el divisor.")))

A(sec("Razonamiento"))

A(p(
    "Dos resistencias en serie entre la señal y masa reparten la tensión en "
    "proporción a sus valores. Midiendo en el punto del medio se obtiene:"))

A(codigo("""V_salida = V_entrada * R2 / (R1 + R2)"""))

A(p(
    "Con R1 de 10 kΩ y R2 de 15 kΩ, el factor es 15/25 = 0,6. Una entrada de "
    "5 V se convierte en 3,0 V, que entra con margen en el pin. Para "
    "recuperar la tensión original en el programa hay que multiplicar por el "
    "inverso:"))

A(codigo("""FACTOR = (R1 + R2) / R2          # 25/15 = 1,667"""))

A(tabla(
    ["Entrada real", "En el pin", "Lo que reconstruye el programa"],
    [["0 V", "0,00 V", "0,00 V"],
     ["2,5 V", "1,50 V", "2,50 V"],
     ["5,0 V", "3,00 V", "5,00 V"],
     ["<b>10 V</b>", "<b>6,00 V</b>", "<b>daña el pin</b>"]],
    centradas=(0, 1, 2)))

A(p(
    "La última fila importa: este divisor está calculado para 5 V. Para una "
    "señal de 0 a 10 V hay que recalcularlo —con R1 de 22 kΩ y R2 de 10 kΩ el "
    "factor deja 3,1 V a fondo de escala—, y el ejercicio 2 lo propone."))

A(nota("Por qué no se eligen resistencias mucho más grandes", p(
    "Con valores altos el divisor consume menos, y eso suena bien. Pero el "
    "conversor del ESP32 necesita que la fuente que lo alimenta tenga una "
    "resistencia interna baja, por debajo de unos 10 kΩ, o la lectura se "
    "vuelve inestable y baja. Con 10 k y 15 k se está en el límite cómodo. "
    "El laboratorio 3.4, que usa 100 kΩ por obligación, muestra cómo se "
    "resuelve cuando no queda otra.")))

A(sec("Antes de conectar el pin"))

A(aviso("Mida primero, conecte después", p(
    "Arme el divisor, alimente el potenciómetro desde VIN y <b>mida con el "
    "multímetro</b> la tensión en el punto medio, con la perilla al máximo. "
    "Debe leer alrededor de <b>3,0 V</b>. Si lee más de 3,3 V, no conecte el "
    "pin: las dos resistencias están intercambiadas.",
    "Es un minuto de trabajo y evita una placa quemada. En el taller esta "
    "costumbre se llama «comprobar antes de energizar» y vale exactamente "
    "igual aquí.")))

A(sec("Programa"))

A(codigo("""from machine import Pin, ADC
import time

PIN_ENTRADA = 35

R1 = 10000.0              # ohmios, del cursor al punto medio
R2 = 15000.0              # ohmios, del punto medio a masa
FACTOR = (R1 + R2) / R2   # cuanto hay que multiplicar para
                          # recuperar la tension original

TENSION_MAXIMA = 3.3
CUENTAS_MAXIMAS = 4095

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)
entrada.width(ADC.WIDTH_12BIT)


def leer_entrada():
    \"\"\"Devuelve la tension en el pin y la tension real de la senal.\"\"\"
    cuentas = entrada.read()
    en_el_pin = cuentas * TENSION_MAXIMA / CUENTAS_MAXIMAS
    return en_el_pin, en_el_pin * FACTOR


def main():
    print("Divisor de {:.0f}k / {:.0f}k, factor {:.3f}".format(
        R1 / 1000, R2 / 1000, FACTOR))
    print("")
    print("  en el pin    senal real")

    while True:
        en_el_pin, real = leer_entrada()

        aviso = ""
        if en_el_pin > 3.1:
            aviso = "   <-- revise el divisor"

        print("   {:5.3f} V     {:5.3f} V{}".format(
            en_el_pin, real, aviso))
        time.sleep(0.5)


if __name__ == "__main__":
    main()""", archivo="lab_3_2_divisor.py"))

A(sec("Qué debe observarse"))
A(p(
    "Con el cursor al mínimo las dos columnas marcan cerca de cero; al máximo, "
    "3,0 V en el pin y 5,0 V reconstruidos. Comparando la segunda columna con "
    "el multímetro puesto en el cursor del potenciómetro, las dos cifras deben "
    "coincidir dentro de unas décimas. Lo que sobre de esa diferencia es lo "
    "que corrige el laboratorio 3.5."))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el acondicionamiento de "
    "cualquier transmisor de 0 a 10 V: nivel, presión, caudal. Junto con la "
    "calibración del laboratorio 3.5 es todo lo que hace falta para leer "
    "instrumentación de planta con un ESP32.",
    "<b>En el área mecánica</b>, casi todos los sensores del vehículo trabajan "
    "sobre 5 V: posición de mariposa, caudalímetro, sensor de presión del "
    "múltiple. Ninguno se conecta directamente al pin; todos pasan por un "
    "divisor como éste.")))

# =================================================================== 3.3
A(lab("3.3", "Un sensor lineal: el LM35"))

A(sec("Objetivo"))
A(p("Medir temperatura con un sensor cuya salida es proporcional, y ver por "
    "qué conviene elegir la atenuación en vez de dejar la de siempre."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Sensor LM35", "encapsulado TO-92, como un transistor"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_3_3")[0], ancha=True, epigrafe=
         "El LM35 mirado de frente, con la cara plana hacia quien lo conecta. "
         "Se alimenta de VIN, no de 3V3.", capitulo=3))

A(aviso("El LM35 necesita al menos 4 V", p(
    "La hoja de datos pide de 4 a 30 V de alimentación. Con los 3,3 V de la "
    "placa el sensor <b>funciona igual</b> —enciende, entrega una tensión que "
    "sube con la temperatura, no da ningún error— pero queda fuera de "
    "especificación y <b>mide de menos</b>. Es la peor clase de falla: no hay "
    "síntoma, sólo un número equivocado.",
    "Por eso va a <code>VIN</code>, que entrega los 5 V del USB. Y conectarlo "
    "al revés lo calienta en segundos: si quema al tocarlo, desconecte de "
    "inmediato y revise la orientación.")))

A(sec("Razonamiento"))

A(p(
    "El LM35 entrega <b>10 mV por cada grado centígrado</b>. A 25 °C su "
    "salida vale 250 mV; a 100 °C, un volt. La conversión es una división y "
    "no hay más.",

    "Lo interesante es la atenuación. Dentro del rango útil el sensor nunca "
    "pasa de 1 V, de modo que pedir <code>ATTN_11DB</code> —que abarca hasta "
    "3,3 V— desperdicia dos tercios del conversor: la medición ocupa apenas "
    "un tercio de las 4096 cuentas. Con <code>ATTN_6DB</code>, que llega a "
    "unos 2,0 V, la misma medición ocupa la mitad y <b>se duplica la "
    "resolución</b>.",

    "Ese es el criterio general: elegir la atenuación más chica en la que la "
    "señal todavía entre entera, con algo de margen. No es un ajuste fino, "
    "son grados de resolución regalados."))

A(tabla(
    ["Atenuación", "Rango", "Cuentas por grado", "Resolución"],
    [["<code>ATTN_11DB</code>", "0 – 3,3 V", "12,4", "≈ 0,08 °C"],
     ["<code>ATTN_6DB</code>", "0 – 2,0 V", "20,5", "≈ 0,05 °C"]],
    centradas=(0, 1, 2, 3)))

A(p("La diferencia es menor que el error del propio sensor, así que en este "
    "caso no cambia el resultado. Importa el criterio, que sí cambia el "
    "resultado cuando la señal es pequeña de verdad."))

A(sec("Programa"))

A(codigo("""from machine import Pin, ADC
import time

PIN_ENTRADA = 32
MILIVOLTIOS_POR_GRADO = 10.0
MUESTRAS = 16             # promedio para atenuar el ruido del conversor

# Con atenuacion de 6 dB el conversor llega a unos 2,0 V, que serian
# 200 C: de sobra, y con el doble de resolucion que usando los 3,3 V.
TENSION_MAXIMA = 2.0
CUENTAS_MAXIMAS = 4095

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_6DB)
entrada.width(ADC.WIDTH_12BIT)


def leer_milivoltios():
    \"\"\"Promedia varias lecturas y devuelve la salida en milivoltios.\"\"\"
    suma = 0
    for _ in range(MUESTRAS):
        suma = suma + entrada.read()
        time.sleep_ms(2)
    cuentas = suma / MUESTRAS
    return cuentas * TENSION_MAXIMA * 1000 / CUENTAS_MAXIMAS


def leer_temperatura():
    return leer_milivoltios() / MILIVOLTIOS_POR_GRADO


def main():
    print("Sensor LM35 en GPIO{}".format(PIN_ENTRADA))
    print("")
    print("  salida      temperatura")

    while True:
        mv = leer_milivoltios()
        print("   {:6.1f} mV    {:5.1f} C".format(
            mv, mv / MILIVOLTIOS_POR_GRADO))
        time.sleep(1)


if __name__ == "__main__":
    main()""", archivo="lab_3_3_lm35.py"))

A(sec("Qué debe observarse"))
A(p(
    "A temperatura ambiente marca entre 18 y 25 °C. Tomando el sensor con los "
    "dedos sube varios grados en pocos segundos y baja al soltarlo: la "
    "respuesta es rápida porque el encapsulado es pequeño.",

    "Conviene comparar con un termómetro. La diferencia que aparezca —y va a "
    "aparecer— es lo que corrige el laboratorio 3.5."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Marca unos grados de menos, siempre",
      "Está alimentado con 3V3. Es el caso del recuadro."],
     ["Se calienta al tocarlo",
      "Está al revés. Desconecte de inmediato."],
     ["Marca cerca de cero y no cambia",
      "La pata del medio no llegó al pin, o se cableó la de al lado."],
     ["Marca valores altísimos",
      "La atenuación quedó en 11 dB pero <code>TENSION_MAXIMA</code> dice "
      "2,0: las dos constantes tienen que corresponderse."]]))

# =================================================================== 3.4
A(lab("3.4", "Un sensor que no es lineal: el termistor NTC"))

A(sec("Objetivo"))
A(p("Medir temperatura con un sensor cuya resistencia varía de manera "
    "exponencial, y resolver el problema que eso trae al conversor."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Termistor NTC de 100 kΩ", "Beta 3950, el de sonda con cable"],
         ["1", "Resistencia de 100 kΩ", "la resistencia fija del divisor"],
         ["1", "Condensador de 100 nF", "<b>no es opcional</b>, ver el recuadro"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_3_4")[0], ancha=True, epigrafe=
         "El termistor y la resistencia fija forman un divisor; el punto "
         "medio es la señal. El condensador va en paralelo con el termistor, "
         "entre el pin y masa.", capitulo=3))

A(aviso("Cien kilohmios son demasiados para el conversor", p(
    "El conversor del ESP32 no mide una tensión de manera pasiva: internamente "
    "carga un pequeño condensador con la señal, y para hacerlo necesita que la "
    "fuente tenga una resistencia baja, <b>por debajo de unos 10 kΩ</b>.",
    "Un divisor de 100 kΩ presenta unos 50 kΩ, cinco veces más de lo "
    "admisible. La consecuencia es que la lectura sale baja e inestable, y "
    "parece ruido cuando en realidad es que el conversor no alcanza a "
    "cargarse.",
    "El condensador de <b>100 nF</b> entre el pin y masa resuelve el problema: "
    "es el que entrega la carga instantánea que el conversor pide, y el "
    "divisor sólo tiene que reponerla despacio. Sin él este laboratorio no "
    "funciona, y el síntoma no dice nada de la causa.")))

A(sec("Razonamiento"))

A(p(
    "Un termistor no entrega tensión: cambia de resistencia. Para leerlo se lo "
    "pone en serie con una resistencia fija y se mide el punto medio, igual "
    "que en el laboratorio 3.2. De la tensión medida se despeja la resistencia "
    "del termistor:"))

A(codigo("""R_ntc = R_fija * V_medida / (V_alimentacion - V_medida)"""))

A(p(
    "Y ahí empieza lo distinto. La resistencia no varía en proporción a la "
    "temperatura sino de manera exponencial, y la relación se describe con la "
    "<b>ecuación de Beta</b>, donde las temperaturas van en kelvin:"))

A(codigo("""1/T = 1/T0 + ln(R / R0) / BETA"""))

A(tabla(
    ["Constante", "Qué es", "Este termistor"],
    [["<code>R0</code>", "Resistencia a la temperatura nominal", "100 kΩ"],
     ["<code>T0</code>", "Temperatura nominal", "25 °C = 298,15 K"],
     ["<code>BETA</code>", "Constante del material, la da el fabricante",
      "3950 K"]],
    centradas=(2,)))

A(p(
    "Las tres salen de la hoja de datos y están en constantes al principio del "
    "programa. Si el termistor es de otro valor —los de 10 kΩ son los más "
    "comunes— se cambian esas tres líneas y <b>la resistencia fija</b>, que "
    "debe ser del mismo valor que el nominal del termistor."))

A(sec("Programa"))

A(codigo("""from machine import Pin, ADC
import math
import time

PIN_ENTRADA = 33

R_FIJA = 100000.0         # ohmios, la resistencia de arriba
R_NOMINAL = 100000.0      # ohmios del termistor a T_NOMINAL
T_NOMINAL = 25.0          # grados centigrados
BETA = 3950.0             # kelvin, constante del material

ALIMENTACION = 3.3
CERO_ABSOLUTO = 273.15
CUENTAS_MAXIMAS = 4095
MUESTRAS = 16

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)
entrada.width(ADC.WIDTH_12BIT)


def leer_tension():
    suma = 0
    for _ in range(MUESTRAS):
        suma = suma + entrada.read()
        time.sleep_ms(2)
    return (suma / MUESTRAS) * ALIMENTACION / CUENTAS_MAXIMAS


def resistencia_del_ntc(tension):
    \"\"\"Despeja la resistencia. None si el sensor esta desconectado.\"\"\"
    if tension <= 0 or tension >= ALIMENTACION:
        return None
    return R_FIJA * tension / (ALIMENTACION - tension)


def temperatura(resistencia):
    \"\"\"Aplica la ecuacion de Beta. Devuelve grados centigrados.\"\"\"
    t0 = T_NOMINAL + CERO_ABSOLUTO
    inversa = 1.0 / t0 + math.log(resistencia / R_NOMINAL) / BETA
    return 1.0 / inversa - CERO_ABSOLUTO


def main():
    print("Termistor NTC de {:.0f}k, Beta {:.0f}".format(
        R_NOMINAL / 1000, BETA))
    print("")
    print("  tension   resistencia   temperatura")

    while True:
        tension = leer_tension()
        r = resistencia_del_ntc(tension)

        if r is None:
            print("   {:5.3f} V    sensor desconectado".format(tension))
        else:
            print("   {:5.3f} V   {:8.0f} ohm   {:5.1f} C".format(
                tension, r, temperatura(r)))

        time.sleep(1)


if __name__ == "__main__":
    main()""", archivo="lab_3_4_termistor.py"))

A(nota("Por qué se comprueba el rango antes de dividir", p(
    "Si el termistor se desconecta, la tensión sube hasta la alimentación y la "
    "fórmula de la resistencia divide por cero. Si se pone en corto, baja a "
    "cero y el logaritmo recibe un cero. Los dos casos detienen el programa "
    "con una excepción poco clara.",
    "Comprobar el rango antes convierte una falla del cableado en un mensaje "
    "que dice qué pasa. En un equipo que queda instalado, ésta es la "
    "diferencia entre «sensor desconectado» y un programa muerto.")))

A(sec("Qué debe observarse"))
A(p(
    "A temperatura ambiente la resistencia ronda los 100 kΩ y la temperatura "
    "cae cerca de 25 °C, que es justamente la condición nominal del sensor. "
    "A 0 °C la resistencia sube a unos 336 kΩ y a 80 °C baja a 12,7 kΩ. Tomando la sonda con la mano la resistencia "
    "<b>baja</b> —es lo que significa NTC, coeficiente negativo— y la "
    "temperatura sube.",

    "Vale la pena mirar las dos primeras columnas juntas. Entre 20 y 30 °C la "
    "resistencia cae unos <b>45 000 Ω</b>; entre 75 y 85 °C, el mismo salto "
    "de diez grados mueve apenas <b>4 000 Ω</b>, once veces menos. Eso es la "
    "no linealidad vista de frente, y es la razón por la que un termistor "
    "mide muy bien cerca de su temperatura nominal y cada vez peor al "
    "alejarse."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["La lectura baila mucho y marca de menos",
      "Falta el condensador de 100 nF. Es el caso del recuadro."],
     ["«sensor desconectado»",
      "Una de las dos patas no hace contacto, o la resistencia fija no está."],
     ["Marca una temperatura constante y absurda",
      "La resistencia fija no es de 100 kΩ, o el termistor no es el de 100 kΩ."],
     ["Sube cuando debería bajar",
      "El termistor y la resistencia fija están intercambiados de lugar."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, el termistor es el sensor de "
    "temperatura de bobinado de un motor y el de los equipos de refrigeración. "
    "La protección térmica de un motor es, en el fondo, este laboratorio con "
    "un umbral y un relé.",
    "<b>En el área mecánica</b>, es el sensor de temperatura de refrigerante y el de "
    "aire de admisión: los dos son termistores NTC leídos exactamente así. La "
    "diferencia es que en el vehículo la resistencia fija está dentro de la "
    "computadora y el termistor cuelga del motor.")))

# =================================================================== 3.5
A(lab("3.5", "Calibración de dos puntos"))

A(sec("Objetivo"))
A(p("Corregir la diferencia entre lo que el sensor dice y lo que realmente "
    "hay, sin cambiar de sensor ni de fórmula."))

A(sec("Razonamiento"))

A(p(
    "Los cuatro laboratorios anteriores usan las constantes del fabricante, y "
    "esas constantes casi nunca coinciden con el componente que uno tiene en "
    "la mano. Las resistencias tienen tolerancia del 5 %, los cables tienen "
    "caída, el propio sensor tiene desvío y el conversor del ESP32 tiene un "
    "error conocido de varias decenas de milivoltios.",

    "La calibración de dos puntos resuelve todo eso junto y sin teoría: se "
    "mide en dos condiciones conocidas, se anota qué dijo el instrumento en "
    "cada una, y se traza la recta que las une. Esa recta corrige de una vez "
    "todos los desvíos anteriores, sin importar de dónde vengan.",

    "La recta es <code>y = m·x + b</code>, y de dos puntos salen los dos "
    "coeficientes:"))

A(codigo("""pendiente = (real2 - real1) / (crudo2 - crudo1)
ordenada  = real1 - pendiente * crudo1"""))

A(aviso("Los dos puntos deben estar separados", p(
    "Cuanto más juntos estén, más se amplifica cualquier error al calcular la "
    "pendiente. Calibrar con dos puntos que difieren en dos grados es peor "
    "que no calibrar.",
    "Para temperatura, los dos puntos clásicos son agua con hielo (0 °C) y "
    "agua hirviendo (100 °C, algo menos en altura). En La Paz el agua hierve "
    "cerca de 88 °C, de modo que ese valor hay que corregirlo o usar otro "
    "punto conocido.")))

A(sec("Filtrar antes de calibrar"))

A(p(
    "Calibrar sobre una lectura que baila no sirve. Hay dos maneras de "
    "estabilizarla y no dan lo mismo."))

A(tabla(
    ["Filtro", "Qué hace", "Cuándo conviene"],
    [["<b>Promedio</b>", "Suma varias lecturas y divide.",
      "Ruido parejo, el caso normal. Es el que usan los laboratorios "
      "anteriores."],
     ["<b>Mediana</b>", "Ordena las lecturas y toma la del medio.",
      "Cuando hay picos aislados: motores arrancando, contactores, soldadura "
      "cerca. Un solo valor disparatado no la mueve; al promedio sí."]]))

A(sec("Programa"))

A(codigo("""from machine import Pin, ADC
import time

PIN_ENTRADA = 34

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)
entrada.width(ADC.WIDTH_12BIT)


# ------------------------------------------------------- filtrado
def leer_promedio(muestras=32, espera_ms=2):
    \"\"\"Promedia varias lecturas. Atenua el ruido de fondo.\"\"\"
    suma = 0
    for _ in range(muestras):
        suma = suma + entrada.read()
        time.sleep_ms(espera_ms)
    return suma / muestras


def leer_mediana(muestras=15, espera_ms=2):
    \"\"\"Valor central de varias lecturas ordenadas.

    A diferencia del promedio, no se deja arrastrar por una lectura
    disparatada. Conviene cuando hay motores o contactores cerca.
    \"\"\"
    valores = []
    for _ in range(muestras):
        valores.append(entrada.read())
        time.sleep_ms(espera_ms)
    valores.sort()
    return valores[len(valores) // 2]


# ---------------------------------------------------- calibracion
def recta_de_calibracion(crudo1, real1, crudo2, real2):
    \"\"\"Pendiente y ordenada de la recta que une los dos puntos.\"\"\"
    if crudo2 == crudo1:
        raise ValueError("los dos puntos dan la misma lectura")
    pendiente = (real2 - real1) / (crudo2 - crudo1)
    ordenada = real1 - pendiente * crudo1
    return pendiente, ordenada


def aplicar(crudo, pendiente, ordenada):
    return pendiente * crudo + ordenada


def calibrar(unidad="C"):
    \"\"\"Guia la toma de los dos puntos y devuelve la recta.\"\"\"
    print("Punto 1: lleve el sensor a la primera condicion conocida.")
    input("   Pulse Enter cuando este estable... ")
    crudo1 = leer_promedio()
    real1 = float(input("   Valor real, en {}: ".format(unidad)))

    print("Punto 2: lleve el sensor a la segunda condicion.")
    input("   Pulse Enter cuando este estable... ")
    crudo2 = leer_promedio()
    real2 = float(input("   Valor real, en {}: ".format(unidad)))

    pendiente, ordenada = recta_de_calibracion(
        crudo1, real1, crudo2, real2)
    print("")
    print("   pendiente = {:.6f}".format(pendiente))
    print("   ordenada  = {:.4f}".format(ordenada))
    print("   Copie estas dos cifras al programa definitivo.")
    return pendiente, ordenada


def main():
    pendiente, ordenada = calibrar()
    print("")
    print("  crudo    calibrado")

    while True:
        crudo = leer_promedio()
        print("   {:6.0f}    {:7.2f}".format(
            crudo, aplicar(crudo, pendiente, ordenada)))
        time.sleep(1)


if __name__ == "__main__":
    main()""", archivo="lab_3_5_calibracion.py"))

A(sec("Qué debe observarse"))
A(p(
    "El programa pide las dos condiciones, calcula la recta y muestra las dos "
    "columnas en paralelo. Las dos cifras que imprime —pendiente y ordenada— "
    "son el resultado del laboratorio: se copian como constantes al programa "
    "definitivo y no hace falta volver a calibrar hasta que se cambie el "
    "sensor o el cableado.",

    "<b>Una advertencia sobre la que conviene insistir:</b> la calibración "
    "vale para <i>ese</i> sensor con <i>ese</i> cableado. Cambiar el cable por "
    "uno más largo, o el sensor por otro igual, obliga a repetirla."))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, esto es literalmente lo que se hace "
    "al poner en marcha un lazo de instrumentación: se ajusta el cero y el "
    "span del transmisor contra un patrón. La pendiente es el span y la "
    "ordenada es el cero, y el procedimiento de la norma es este mismo.",
    "<b>En el área mecánica</b>, es el aprendizaje de posición que hace la "
    "computadora con el sensor de mariposa: se le enseña qué lectura "
    "corresponde a cerrado y cuál a pleno, y de ahí en más interpola.")))

A(ejercicios([
    "En el laboratorio 3.1, calcule cuántos milivoltios representa una sola "
    "cuenta con cada una de las cuatro atenuaciones.",

    "Calcule R1 y R2 para leer una señal de 0 a 10 V dejando como máximo "
    "3,1 V en el pin, con resistencias de valores comerciales y sin pasarse "
    "de 25 kΩ en total.",

    "El LM35 del laboratorio 3.3 y el termistor del 3.4, puestos juntos, "
    "¿marcan lo mismo? Anote la diferencia y explique de dónde puede venir.",

    "Modifique el laboratorio 3.4 para un termistor de 10 kΩ. ¿Qué cuatro "
    "cosas hay que cambiar? ¿Sigue haciendo falta el condensador?",

    "Aplique la calibración del 3.5 al LM35 usando agua con hielo y agua "
    "caliente medida con termómetro. ¿Cuánto vale la ordenada? ¿Qué "
    "significaría que valiera exactamente cero?",

    "Con el potenciómetro quieto, tome cien lecturas y anote la mayor y la "
    "menor. ¿Cuántas cuentas de ruido hay? ¿Cuántos grados serían si fuera el "
    "termistor del 3.4 a temperatura ambiente?",

    "Explique por qué la mediana de quince lecturas resiste un pico y el "
    "promedio de treinta y dos no. ¿En qué caso preferiría igual el promedio?",
]))
