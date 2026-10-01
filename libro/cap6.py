# -*- coding: utf-8 -*-
"""Capítulo 6 — Sensores con bus y protocolo."""
from maqueta import (capitulo, lab, sec, codigo, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import circuitos_cap6 as CIR

PARTES = []
A = PARTES.append

A(capitulo(6, "Sensores con bus y protocolo", p(
    "Los capítulos anteriores trataron señales: un nivel, una tensión, un "
    "tren de pulsos. En todos los casos el sensor entregaba algo físico y el "
    "programa lo interpretaba.",

    "Hay otra familia de sensores que no entrega una señal sino <b>datos</b>. "
    "Adentro tienen su propio microcontrolador, que ya hizo la medición y la "
    "conversión, y lo que sale por el cable son números codificados según un "
    "acuerdo. Ahí el trabajo del programa deja de ser interpretar una señal y "
    "pasa a ser <b>conversar</b>.",

    "Ese cambio trae dos ventajas y un costo. Las ventajas son que la "
    "medición viene calibrada de fábrica y que varios sensores pueden "
    "compartir los mismos dos cables. El costo es que hay que respetar el "
    "acuerdo al pie de la letra, y cuando algo no funciona el sensor no dice "
    "por qué: simplemente no contesta. Los seis laboratorios de este capítulo "
    "recorren cuatro acuerdos distintos, de más a menos normalizado.")))

A(tabla(
    ["Acuerdo", "Cables", "Sensor de este capítulo", "Laboratorio"],
    [["<b>I²C</b>, bus normalizado", "2 compartidos", "Pantalla OLED",
      "6.1 y 6.2"],
     ["<b>Un hilo</b>, propio del fabricante", "1", "DHT11", "6.3"],
     ["<b>Con reloj</b>, propio del fabricante", "2", "HX710B", "6.4"],
     ["<b>Puerto serie</b> con Modbus", "2", "PZEM-004T", "6.5"]],
    centradas=(1, 3)))

# =================================================================== 6.1
A(lab("6.1", "Explorar el bus I²C"))

A(sec("Objetivo"))
A(p("Averiguar qué hay conectado al bus antes de escribir una sola línea de "
    "programa para usarlo."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Pantalla OLED de 128×64", "con controlador SSD1306, I²C"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_6_1")[0], ancha=True, epigrafe=
         "Los cuatro cables de la pantalla. SCL y SDA son el bus, y los "
         "mismos dos hilos servirán para cualquier otro dispositivo I²C que "
         "se agregue después.", capitulo=6))

A(sec("Razonamiento"))

A(p(
    "Un bus es una línea compartida. En I²C hay sólo dos hilos —"
    "<b>SCL</b>, el reloj, y <b>SDA</b>, los datos— y todos los dispositivos "
    "cuelgan de ellos en paralelo. Para que no se pisen, cada uno tiene una "
    "<b>dirección</b> de siete bits, y el ESP32 empieza cada conversación "
    "nombrando a quién le habla.",

    "La consecuencia práctica es que agregar un segundo sensor no cuesta "
    "cables: se conecta a los mismos dos. El límite está en las direcciones, "
    "y ahí aparece el problema típico: dos dispositivos iguales tienen la "
    "misma dirección de fábrica y no pueden convivir sin cambiarla —muchos "
    "módulos traen un puente para eso.",

    "Antes de programar nada conviene preguntarle al bus quién está. "
    "MicroPython lo resuelve en una línea."))

A(sec("Programa"))

A(codigo("""from machine import Pin, SoftI2C

PIN_SCL = 22
PIN_SDA = 21

CONOCIDOS = {
    0x3C: "pantalla OLED SSD1306",
    0x3D: "pantalla OLED SSD1306 (direccion alternativa)",
    0x27: "pantalla LCD con adaptador PCF8574",
    0x68: "reloj DS1307 o acelerometro MPU6050",
    0x76: "sensor de presion BMP280 o BME280",
    0x77: "sensor de presion BMP280 (direccion alternativa)",
}

i2c = SoftI2C(scl=Pin(PIN_SCL), sda=Pin(PIN_SDA), freq=400000)

print("Explorando el bus I2C en SCL=GPIO{}, SDA=GPIO{}".format(
    PIN_SCL, PIN_SDA))
print("")

encontrados = i2c.scan()

if not encontrados:
    print("No contesta nadie.")
    print("  - Revise VCC y GND del modulo.")
    print("  - Revise que SCL y SDA no esten intercambiados.")
    print("  - Algunos modulos necesitan resistencias de elevacion.")
else:
    print("  direccion         que suele ser")
    for direccion in encontrados:
        nombre = CONOCIDOS.get(direccion, "desconocido")
        print("   0x{:02X}  ({:3d})    {}".format(
            direccion, direccion, nombre))
    print("")
    print("{} dispositivo(s) en el bus.".format(len(encontrados)))""",
    archivo="lab_6_1_explorar_i2c.py"))

A(sec("Qué debe observarse"))

A(consola("""Explorando el bus I2C en SCL=GPIO22, SDA=GPIO21

  direccion         que suele ser
   0x3C  ( 60)    pantalla OLED SSD1306

1 dispositivo(s) en el bus."""))

A(nota("Este programa vale para todo el capítulo", p(
    "Cada vez que un sensor I²C no responda, lo primero es correr este "
    "explorador. Si el dispositivo no aparece, el problema es de cableado o "
    "de alimentación y no tiene sentido revisar el programa. Si aparece, el "
    "cableado está bien y el problema es otro.",
    "Es el equivalente a comprobar la continuidad antes de buscar la falla en "
    "el circuito de mando.")))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["No contesta nadie",
      "SCL y SDA intercambiados —es lo más frecuente—, o el módulo sin "
      "alimentar."],
     ["Aparece una dirección inesperada",
      "El módulo es de otro fabricante. La dirección que importa es la que "
      "aparece, no la de la hoja de datos."],
     ["Aparecen muchísimas direcciones",
      "SDA está suelto y el bus lee ruido."],
     ["Aparece a veces sí y a veces no",
      "Faltan las resistencias de elevación, o el cable es demasiado largo "
      "para 400 kHz. Baje <code>freq</code> a 100000."]]))

# =================================================================== 6.2
A(lab("6.2", "La pantalla OLED"))

A(sec("Objetivo"))
A(p("Mostrar texto y gráficos en la pantalla, y entender por qué nada "
    "aparece hasta que se lo pide expresamente."))

A(sec("El circuito"))
A(p("El mismo del laboratorio 6.1 (figura 6.1)."))

A(aviso("Hace falta el módulo ssd1306.py", p(
    "MicroPython no trae el controlador de la pantalla. Hay que copiar el "
    "archivo <code>ssd1306.py</code> <b>dentro de la placa</b>, igual que "
    "<code>config.py</code> o <code>ble_uart.py</code>. Sin él, "
    "<code>import ssd1306</code> falla y no hay programa que lo arregle.")))

A(sec("Razonamiento"))

A(p(
    "La pantalla no se dibuja sola. Todas las instrucciones de dibujo "
    "—<code>text</code>, <code>rect</code>, <code>fill_rect</code>, "
    "<code>hline</code>— trabajan sobre una copia en la memoria del ESP32, y "
    "no se ve nada hasta que se llama a <code>show()</code>, que manda esa "
    "copia entera a la pantalla.",

    "Es la causa del problema más común con estas pantallas: el programa "
    "dibuja bien y la pantalla queda negra. Falta <code>show()</code>.",

    "Tiene una consecuencia útil: como el dibujo se arma completo antes de "
    "mostrarse, no hay parpadeo. Lo habitual es <code>fill(0)</code> para "
    "borrar, después todo el dibujo, y <code>show()</code> al final."))

A(tabla(
    ["Instrucción", "Qué hace"],
    [["<code>oled.fill(0)</code>", "Borra la copia en memoria."],
     ["<code>oled.text(s, x, y, 1)</code>",
      "Escribe. Cada carácter mide 8×8 píxeles."],
     ["<code>oled.rect(x, y, w, h, 1)</code>", "Dibuja el contorno."],
     ["<code>oled.fill_rect(x, y, w, h, 1)</code>", "Lo dibuja relleno."],
     ["<code>oled.hline(x, y, largo, 1)</code>", "Una línea horizontal."],
     ["<code>oled.show()</code>", "<b>Manda todo a la pantalla.</b>"]]))

A(nota("128 por 64, y ni un píxel más", p(
    "Con caracteres de 8×8 píxeles entran <b>16 columnas y 8 filas</b> de "
    "texto. Dibujar fuera de esos límites no da error: el controlador "
    "simplemente descarta lo que sobra, de modo que una barra mal calculada "
    "aparece cortada sin ninguna pista de por qué. Conviene calcular las "
    "posiciones con la altura de celda como unidad y no con números sueltos.")))

A(sec("Programa"))

A(codigo("""from machine import Pin, SoftI2C
import ssd1306
import time

ANCHO, ALTO, CELDA = 128, 64, 8

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(ANCHO, ALTO, i2c)


def centrar(texto, fila):
    \"\"\"Escribe centrado en una fila, contando en celdas de 8x8.\"\"\"
    x = (ANCHO - len(texto) * CELDA) // 2
    oled.text(texto, max(0, x), fila * CELDA, 1)


def barra(valor, minimo, maximo, x, y, ancho, alto):
    \"\"\"Barra de progreso. Recorta el valor para no salirse.\"\"\"
    oled.rect(x, y, ancho, alto, 1)
    recorrido = maximo - minimo
    if recorrido <= 0:
        return
    proporcion = (valor - minimo) / recorrido
    if proporcion < 0:
        proporcion = 0
    if proporcion > 1:
        proporcion = 1
    lleno = int((ancho - 2) * proporcion)
    if lleno > 0:
        oled.fill_rect(x + 1, y + 1, lleno, alto - 2, 1)


def main():
    # --- texto centrado
    oled.fill(0)
    centrar("SENSORICA", 2)
    centrar("ESP32", 4)
    oled.show()          # sin esta linea la pantalla queda negra
    time.sleep(2)

    # --- una barra que se llena
    for valor in range(0, 101, 5):
        oled.fill(0)
        centrar("CARGA", 0)
        oled.text("{:3d} %".format(valor), 48, 2 * CELDA, 1)
        barra(valor, 0, 100, 8, 4 * CELDA, 112, 14)
        oled.show()
        time.sleep_ms(80)

    # --- lo que no entra, se recorta solo
    oled.fill(0)
    centrar("RECORTE", 0)
    barra(150, 0, 100, 8, 3 * CELDA, 112, 14)   # 150 sobre 100
    barra(-20, 0, 100, 8, 5 * CELDA, 112, 14)   # -20 sobre 100
    oled.show()


if __name__ == "__main__":
    main()""", archivo="lab_6_2_oled.py"))

A(sec("Qué debe observarse"))
A(p(
    "Primero dos líneas centradas, después una barra que se llena sin "
    "parpadear, y al final dos barras con valores imposibles: una llena del "
    "todo y otra vacía. Que un valor fuera de rango no rompa el dibujo es "
    "deliberado, y es la misma idea que el indicador del laboratorio 7.3."))

# =================================================================== 6.3
A(lab("6.3", "DHT11: un hilo y un acuerdo propio"))

A(sec("Objetivo"))
A(p("Leer un sensor que habla por un solo cable con un protocolo que no es de "
    "nadie más, y convivir con que a veces se equivoque."))

A(sec("El circuito"))
A(p("VCC a 3V3, GND a masa y DATA a GPIO14. Es el montaje que reaparece en "
    "los laboratorios 7.2, 7.4 y 7.6 (figura 7.2)."))

A(sec("Razonamiento"))

A(p(
    "El DHT11 usa un solo hilo y un protocolo inventado por su fabricante: el "
    "ESP32 lo baja un rato para pedir la medición, y el sensor contesta con "
    "40 bits cuya duración de pulso codifica cada uno. Todo eso lo hace el "
    "módulo <code>dht</code>, que viene con MicroPython: el programa sólo "
    "llama a <code>measure()</code> y después lee.",

    "Lo que sí es asunto del programa es que <b>esa lectura falla de vez en "
    "cuando</b>. Los últimos 8 de los 40 bits son una suma de verificación, y "
    "cuando no cuadra MicroPython levanta un <code>OSError</code>. No "
    "significa que el sensor esté malo: significa que esa trama llegó mal y "
    "hay que pedir otra.",

    "Un programa que no atrape ese error se detiene, y lo hará en algún "
    "momento: es cuestión de minutos. Todo programa de este libro que use un "
    "DHT11 tiene el <code>try</code>, y no es una precaución teórica."))

A(aviso("Dos segundos entre lecturas, como mínimo", p(
    "El DHT11 no admite que se le pida una medición más seguido que cada dos "
    "segundos. Pidiéndosela antes, devuelve la anterior o directamente falla. "
    "Es la causa de la mitad de los <code>OSError</code> que aparecen en "
    "clase: no es el cableado, es el ritmo.")))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time
import dht

PIN_DATOS = 14
INTERVALO = 2             # segundos. El DHT11 no admite menos.
AVISAR_TRAS = 5           # fallas seguidas antes de sospechar del cable

sensor = dht.DHT11(Pin(PIN_DATOS))


def leer():
    \"\"\"Temperatura y humedad, o None si la trama llego mal.

    La suma de verificacion del DHT11 falla cada tanto y no
    significa que el sensor este malo: hay que pedir otra trama.
    Sin este try, el programa se detiene.
    \"\"\"
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError:
        return None


def main():
    print("DHT11 en GPIO{}".format(PIN_DATOS))
    print("")
    fallas = 0

    while True:
        lectura = leer()

        if lectura is None:
            fallas = fallas + 1
            print("Lectura fallida ({}).".format(fallas))
            if fallas == AVISAR_TRAS:
                print("Varias seguidas: revise el cable y la")
                print("resistencia de elevacion en la linea.")
        else:
            temperatura, humedad = lectura
            fallas = 0
            print("Temperatura: {} C    Humedad: {} %".format(
                temperatura, humedad))

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()""", archivo="lab_6_3_dht11.py"))

A(sec("Qué debe observarse"))
A(p(
    "Las lecturas salen cada dos segundos. De tanto en tanto aparece una "
    "línea de falla y enseguida vuelve a andar: eso es normal. Lo que no es "
    "normal es que fallen muchas seguidas, y por eso el programa avisa.",

    "Soplando sobre el sensor la humedad sube enseguida y baja despacio. La "
    "temperatura se mueve poco: el DHT11 da grados enteros y no tiene "
    "resolución para cambios finos."))

# =================================================================== 6.4
A(lab("6.4", "HX710B: un protocolo con reloj propio"))

A(sec("Objetivo"))
A(p("Leer un conversor de 24 bits marcándole el compás, y resolver el "
    "problema de signo que eso trae."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Transmisor de presión con HX710B", "de 0 a 40 kPa"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_6_4")[0], ancha=True, epigrafe=
         "Dos hilos de datos: OUT trae el dato y SCK lleva el reloj. La placa "
         "marca el ritmo y el integrado contesta bit a bit.", capitulo=6))

A(sec("Razonamiento"))

A(p(
    "Aquí no hay bus ni norma. El HX710B avisa que tiene un dato listo "
    "poniendo su salida en cero, y a partir de ahí el ESP32 le da "
    "<b>veinticuatro pulsos de reloj</b>; en cada uno el integrado pone un "
    "bit en la salida. Veinticuatro pulsos, veinticuatro bits. Después hay un "
    "pulso más que le dice con qué ganancia debe hacer la medición "
    "siguiente.",

    "Todo eso hay que escribirlo a mano, y es lo que hace este laboratorio "
    "distinto de los anteriores: no hay módulo que lo resuelva."))

A(aviso("El error de signo que sólo ocurre en Python", p(
    "El HX710B entrega un número con signo en complemento a dos de 24 bits. "
    "Los ejemplos en C lo convierten así:",
    "<code>if (dato &amp; 0x800000) dato |= 0xFF000000;</code>",
    "Esa línea traducida a Python <b>no funciona</b>. En C las variables "
    "tienen 32 bits y poner los ocho de arriba produce el número negativo "
    "correcto. En Python los enteros no tienen tamaño: la misma operación da "
    "<b>4 294 967 196</b> en lugar de <b>−100</b>.",
    "La conversión correcta en Python es restar el rango completo: "
    "<code>dato = dato - 0x1000000</code>. Es un error que no da ningún "
    "síntoma hasta que el sensor mide por debajo del cero, y entonces "
    "aparecen valores astronómicos.")))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time

PIN_DATOS = 16
PIN_RELOJ = 4
INTERVALO = 2

# Calibracion. No son numeros magicos: son los dos puntos de la
# recta del laboratorio 3.5. CERO es lo que entrega el sensor sin
# presion y FONDO lo que entrega a fondo de escala.
CERO = 1037416
FONDO = 8388607
KPA_FONDO = 40.0
KPA_A_PSI = 0.145038

salida = Pin(PIN_DATOS, Pin.IN)
reloj = Pin(PIN_RELOJ, Pin.OUT)
reloj.value(0)


def leer_crudo(espera_ms=200):
    \"\"\"Los 24 bits del HX710B, o None si el sensor no responde.

    El integrado avisa que tiene un dato listo poniendo su salida
    en cero. Si eso no ocurre dentro del plazo se abandona, en
    lugar de quedar esperando para siempre.
    \"\"\"
    limite = time.ticks_add(time.ticks_ms(), espera_ms)
    while salida.value() == 1:
        if time.ticks_diff(limite, time.ticks_ms()) <= 0:
            return None
        time.sleep_ms(1)

    dato = 0
    for _ in range(24):
        reloj.value(1)
        dato = (dato << 1) | salida.value()
        reloj.value(0)

    reloj.value(1)          # pulso 25: fija la ganancia de la proxima
    reloj.value(0)

    # Complemento a dos de 24 bits. En Python NO se hace poniendo
    # los bits de arriba: los enteros no tienen tamano y saldria un
    # numero enorme. Se resta el rango completo.
    if dato & 0x800000:
        dato = dato - 0x1000000
    return dato


def presion(crudo):
    \"\"\"Pasa las cuentas a kPa y a psi, con la recta de calibracion.\"\"\"
    kpa = (crudo - CERO) * KPA_FONDO / (FONDO - CERO)
    return kpa, kpa * KPA_A_PSI


def main():
    print("HX710B en OUT=GPIO{}  SCK=GPIO{}".format(
        PIN_DATOS, PIN_RELOJ))
    print("Calibracion: {} = 0 kPa, {} = {:.0f} kPa".format(
        CERO, FONDO, KPA_FONDO))
    print("")

    while True:
        crudo = leer_crudo()

        if crudo is None:
            print("El sensor no responde. Revise OUT, SCK y VCC.")
        else:
            kpa, psi = presion(crudo)
            print("{:9d} cuentas   {:7.2f} kPa   {:6.2f} psi".format(
                crudo, kpa, psi))

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()""", archivo="lab_6_4_presion.py"))

A(sec("Qué debe observarse"))
A(p(
    "Sin presión la lectura ronda el valor de <code>CERO</code> y la columna "
    "de kPa queda cerca de cero. Soplando por el tubo la presión sube y "
    "vuelve al soltar. Las dos constantes de calibración son de <i>ese</i> "
    "sensor: para otro hay que rehacerlas con el procedimiento del "
    "laboratorio 3.5."))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el transmisor de presión de "
    "una línea neumática o de un filtro. La lectura de presión diferencial "
    "entre la entrada y la salida de un filtro es lo que dice cuándo hay que "
    "cambiarlo.",
    "<b>En el área mecánica</b>, el mismo integrado se usa en los sensores de "
    "presión de múltiple y en los medidores de presión de aceite de tablero "
    "digital.")))

# =================================================================== 6.5
A(lab("6.5", "PZEM-004T: conversar con un instrumento"))

A(sec("Objetivo"))
A(p("Leer cuatro magnitudes eléctricas de un instrumento que habla Modbus por "
    "puerto serie."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Medidor PZEM-004T", "con su bobina toroidal"],
         ["1", "Carga para ensayar", "una lámpara sirve"]],
        centradas=(0,)))

A(aviso("Este laboratorio trabaja sobre 220 V", p(
    "El PZEM se conecta a la red de corriente alterna. El montaje se hace con "
    "la línea <b>desconectada</b>, se revisa completo y recién entonces se "
    "energiza. La parte de baja tensión —los cuatro hilos al ESP32— está "
    "aislada de la de red dentro del módulo, pero eso no autoriza a manipular "
    "el conjunto con tensión presente.",
    "Si el curso no tiene un puesto preparado para trabajar con red, este "
    "laboratorio se demuestra y no se arma.")))

A(sec("El circuito"))

A(figura(CIR.svg("lab_6_5")[0], ancha=True, epigrafe=
         "Los cuatro hilos de baja tensión. TX de la placa va a RX del "
         "módulo y al revés: en un enlace serie los nombres se cruzan "
         "siempre.", capitulo=6))

A(aviso("La bobina abraza UN solo conductor", p(
    "El toroide mide el campo magnético que produce la corriente. Si se lo "
    "cierra alrededor de los <b>dos</b> conductores de la línea, los dos "
    "campos son iguales y opuestos, se cancelan, y la corriente medida da "
    "<b>cero</b> con todo perfectamente conectado.",
    "Es el error más frecuente de este montaje y el más desconcertante, "
    "porque la tensión se mide bien y sólo la corriente sale mal.")))

A(sec("Razonamiento"))

A(p(
    "Un puerto serie tiene dos hilos, uno para cada sentido, y los nombres "
    "están puestos desde el punto de vista de cada extremo: lo que uno "
    "transmite el otro lo recibe. Por eso <b>TX va siempre a RX</b>. "
    "Conectarlos derecho —TX con TX— es el otro error clásico, y el síntoma "
    "es silencio absoluto.",

    "Sobre esos dos hilos el PZEM habla <b>Modbus</b>, que es el protocolo "
    "industrial más extendido: el maestro pide un grupo de registros, el "
    "esclavo contesta, y cada mensaje lleva una verificación al final. El "
    "módulo <code>pzem.py</code> se ocupa de armar y comprobar esas tramas; "
    "hay que copiarlo a la placa.",

    "Como cualquier conversación, ésta puede fallar: el instrumento puede no "
    "contestar a tiempo o contestar mal. El programa lo comprueba antes de "
    "usar los valores, en lugar de dar por bueno lo que haya."))

A(sec("Programa"))

A(codigo("""from machine import UART
from pzem import PZEM
import time

INTERVALO = 3

uart = UART(1, baudrate=9600, tx=17, rx=16)
medidor = PZEM(uart)

MAGNITUDES = (("Tension", "getVoltage", "{:7.2f} V"),
              ("Corriente", "getCurrent", "{:7.3f} A"),
              ("Potencia activa", "getActivePower", "{:7.2f} W"),
              ("Factor de potencia", "getPowerFactor", "{:7.3f}"))


def potencia_aparente(tension, corriente):
    \"\"\"Los voltiamperios: lo que la instalacion tiene que soportar.\"\"\"
    return tension * corriente


def main():
    print("Medidor PZEM-004T")
    print("")

    while True:
        if not medidor.read():
            print("Sin lectura valida. Revise el cableado serie.")
            time.sleep(INTERVALO)
            continue

        valores = []
        for nombre, metodo, formato in MAGNITUDES:
            valor = getattr(medidor, metodo)()
            valores.append(valor)
            print("  {:<20}{}".format(nombre, formato.format(valor)))

        # Lo que el instrumento no da y conviene calcular
        aparente = potencia_aparente(valores[0], valores[1])
        reactiva = (aparente ** 2 - valores[2] ** 2) ** 0.5
        print("  {:<20}{:7.2f} VA".format(
            "Potencia aparente", aparente))
        print("  {:<20}{:7.2f} var".format(
            "Potencia reactiva", reactiva))
        print("")

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()""", archivo="lab_6_5_pzem.py"))

A(nota("Por qué se calculan la aparente y la reactiva", p(
    "El instrumento entrega la potencia <b>activa</b>, que es la que hace "
    "trabajo. Pero el conductor y la protección se dimensionan por la "
    "<b>aparente</b>, que es tensión por corriente sin importar el desfase. "
    "Con un factor de potencia de 0,7, una carga de 700 W exige una "
    "instalación de 1000 VA.",
    "Que el libro las calcule y no sólo las muestre es deliberado: es la "
    "diferencia entre leer un instrumento y entender lo que dice.")))

A(sec("Qué debe observarse"))
A(p(
    "Con una lámpara incandescente el factor de potencia da cerca de 1 y la "
    "aparente coincide con la activa. Con una carga inductiva —un motor "
    "pequeño, un balasto— el factor baja y la diferencia entre las dos "
    "potencias se hace visible. Ése es el experimento que vale la pena "
    "hacer."))

# =================================================================== 6.6
A(lab("6.6", "Tablero local: leer, decidir y mostrar"))

A(sec("Objetivo"))
A(p("Juntar lo del capítulo en un solo programa, repartido de manera que el "
    "capítulo 7 pueda agregarle el envío sin tocar nada."))

A(sec("El circuito"))
A(p("La pantalla del laboratorio 6.1, el DHT11 del 6.3 en GPIO14 y el "
    "termistor del 3.4 en GPIO33, todos a la vez."))

A(sec("Razonamiento"))

A(p(
    "Este laboratorio no trae ninguna técnica nueva. Lo que trae es una "
    "manera de repartir el programa, y conviene detenerse en ella porque es "
    "lo que hace posible el capítulo siguiente.",

    "El programa se parte en tres responsabilidades que no se mezclan:"))

A(tabla(
    ["Responsabilidad", "Qué hace", "Qué NO hace"],
    [["<b>Leer</b>", "Habla con los sensores y devuelve números, o None si "
      "algo falló.", "No decide nada ni muestra nada."],
     ["<b>Decidir</b>", "Compara con los umbrales y saca conclusiones.",
      "No sabe de dónde salieron los números ni adónde van."],
     ["<b>Mostrar</b>", "Dibuja en la pantalla.",
      "No lee sensores ni decide."]]))

A(p(
    "Escrito así, agregar la publicación en internet del capítulo 7 es "
    "agregar una <b>cuarta</b> responsabilidad al lado de las otras tres, sin "
    "tocar ninguna. Si en cambio la lectura del sensor estuviera metida "
    "dentro del dibujo —que es lo que sale naturalmente— habría que "
    "desarmarlo todo.",

    "El ejercicio 6 del capítulo 7 pide justamente eso, y sirve para "
    "comprobar si la separación era real o sólo aparente."))

A(sec("Programa"))

A(codigo("""from machine import Pin, SoftI2C, ADC
import math
import time
import dht
import ssd1306

ANCHO, ALTO, CELDA = 128, 64, 8
INTERVALO = 3
TEMPERATURA_ALTA = 30.0        # umbral del aviso en pantalla

# ----------------------------------------------------------- leer
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(ANCHO, ALTO, i2c)

sensor = dht.DHT11(Pin(14))

ntc = ADC(Pin(33))
ntc.atten(ADC.ATTN_11DB)
ntc.width(ADC.WIDTH_12BIT)

R_FIJA = 100000.0
R_NOMINAL = 100000.0
T_NOMINAL = 25.0
BETA = 3950.0
ALIMENTACION = 3.3
CERO_ABSOLUTO = 273.15


def leer_dht():
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError:
        return None


def leer_ntc(muestras=16):
    suma = 0
    for _ in range(muestras):
        suma = suma + ntc.read()
        time.sleep_ms(2)
    tension = (suma / muestras) * ALIMENTACION / 4095

    if tension <= 0 or tension >= ALIMENTACION:
        return None

    resistencia = R_FIJA * tension / (ALIMENTACION - tension)
    t0 = T_NOMINAL + CERO_ABSOLUTO
    inversa = 1.0 / t0 + math.log(resistencia / R_NOMINAL) / BETA
    return 1.0 / inversa - CERO_ABSOLUTO


# -------------------------------------------------------- mostrar
def centrar(texto, fila):
    x = (ANCHO - len(texto) * CELDA) // 2
    oled.text(texto, max(0, x), fila * CELDA, 1)


def barra(valor, minimo, maximo, x, y, ancho, alto):
    oled.rect(x, y, ancho, alto, 1)
    recorrido = maximo - minimo
    if recorrido <= 0:
        return
    proporcion = (valor - minimo) / recorrido
    proporcion = max(0, min(1, proporcion))
    lleno = int((ancho - 2) * proporcion)
    if lleno > 0:
        oled.fill_rect(x + 1, y + 1, lleno, alto - 2, 1)


def dibujar(temperatura, humedad, temperatura_ntc, aviso):
    oled.fill(0)
    centrar("TABLERO", 0)
    oled.hline(0, 10, ANCHO, 1)

    if temperatura is None:
        oled.text("DHT11 sin datos", 0, 2 * CELDA, 1)
    else:
        oled.text("Amb {:4.1f}C {:3d}%".format(temperatura, humedad),
                  0, 2 * CELDA, 1)

    if temperatura_ntc is None:
        oled.text("NTC desconectado", 0, 3 * CELDA, 1)
    else:
        oled.text("NTC {:5.1f} C".format(temperatura_ntc),
                  0, 3 * CELDA, 1)
        barra(temperatura_ntc, 0, 60, 4, 4 * CELDA + 4, 120, 10)

    if aviso:
        centrar("TEMP ALTA", 7)

    oled.show()


def main():
    print("Tablero local en marcha.")

    while True:
        # leer
        lectura = leer_dht()
        temperatura, humedad = lectura if lectura else (None, None)
        temperatura_ntc = leer_ntc()

        # decidir: el umbral se evalua con el sensor que haya
        referencia = temperatura_ntc
        if referencia is None:
            referencia = temperatura
        aviso = (referencia is not None
                 and referencia >= TEMPERATURA_ALTA)

        # mostrar
        dibujar(temperatura, humedad, temperatura_ntc, aviso)

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()""", archivo="lab_6_6_tablero.py"))

A(sec("Qué debe observarse"))
A(p(
    "La pantalla muestra las dos temperaturas y la humedad, con una barra "
    "para el termistor. Calentando la sonda con la mano hasta pasar el "
    "umbral aparece el aviso abajo.",

    "Desconectando cualquiera de los dos sensores, la pantalla lo dice y el "
    "otro sigue funcionando. Un tablero que se apaga entero porque falló un "
    "sensor no sirve, y esa es la razón de que cada lectura devuelva "
    "<code>None</code> en vez de detener el programa."))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, este reparto es el de cualquier "
    "autómata: la imagen de entradas, la lógica y la imagen de salidas son "
    "tres cosas separadas, y por eso un programa de autómata se puede "
    "modificar sin desarmarlo. Lo que aquí se hace a mano, ahí lo impone la "
    "arquitectura.",
    "<b>En el área mecánica</b>, es la estructura de una unidad de control: leer "
    "sensores, aplicar los mapas, mandar a los actuadores. Que el tablero "
    "siga funcionando con un sensor caído es exactamente lo que hace la "
    "computadora del vehículo cuando enciende la luz de avería.")))

A(ejercicios([
    "Agregue un segundo dispositivo I²C al bus del laboratorio 6.1 y "
    "compruebe que el explorador encuentra los dos. ¿Cuántos cables hubo que "
    "agregar?",

    "En el laboratorio 6.2, escriba una función que dibuje un marco alrededor "
    "de toda la pantalla. ¿Qué coordenadas son las últimas válidas?",

    "Quite el <code>try</code> del laboratorio 6.3 y deje el programa "
    "corriendo. Cronometre cuánto tarda en detenerse.",

    "En el laboratorio 6.4, calcule qué valor en kPa daría una lectura cruda "
    "de −100 si la conversión de signo estuviera mal hecha al estilo de C.",

    "Con el PZEM del 6.5 y una carga inductiva, anote el factor de potencia y "
    "calcule cuánta corriente de más circula respecto de una carga resistiva "
    "de la misma potencia activa.",

    "Tome el laboratorio 6.6 y agregue un tercer sensor sin tocar "
    "<code>dibujar()</code> más que para una línea. Si tuvo que tocar más, "
    "¿dónde estaba mal separado?",
]))
