# -*- coding: utf-8 -*-
"""Capítulo 5 — Salidas moduladas."""
from maqueta import (capitulo, lab, sec, codigo, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import circuitos_cap5 as CIR
import figuras_cap5 as FIG

PARTES = []
A = PARTES.append

A(capitulo(5, "Salidas moduladas", p(
    "Un pin digital sólo sabe hacer dos cosas: poner 3,3 V o poner 0 V. No hay "
    "manera de pedirle 1,7 V. Y sin embargo, con ese único recurso se regula el "
    "brillo de una lámpara, la velocidad de un motor, la posición de un "
    "servomotor y la nota de un zumbador.",

    "El truco consiste en conmutar muy rápido y repartir el tiempo. Si el pin "
    "está en alto la cuarta parte de cada ciclo, el valor medio es la cuarta "
    "parte de 3,3 V, y una lámpara —que no alcanza a apagarse entre ciclo y "
    "ciclo— se comporta como si recibiera esa fracción. A eso se le llama "
    "<b>modulación por ancho de pulso</b>, y en los programas aparece "
    "abreviada como PWM, de <i>pulse width modulation</i>.",

    "Este capítulo es el reverso del capítulo 3. Allí el problema era traer "
    "hacia adentro una magnitud continua; aquí es sacarla hacia afuera. Y el "
    "laboratorio que los une —un potenciómetro que gobierna el brillo de un "
    "LED— es el primero de los cinco.")))

# =================================================================== 5.1
A(lab("5.1", "Qué se controla y qué no"))

A(p(
    "Una salida modulada tiene <b>dos</b> parámetros, y conviene no "
    "confundirlos porque cada aplicación gobierna uno distinto."))

A(tabla(
    ["Parámetro", "Qué es", "Se fija con"],
    [["<b>Frecuencia</b>", "Cuántos ciclos por segundo. No cambia la "
      "intensidad: cambia sólo cuán rápido se conmuta.",
      "<code>PWM(pin, freq=1000)</code> o <code>.freq(1000)</code>"],
     ["<b>Ciclo de trabajo</b>", "Qué proporción de cada ciclo pasa en alto. "
      "Esto sí es la intensidad.",
      "<code>.duty(0…1023)</code> o <code>.duty_u16(0…65535)</code>"]]))

A(figura(FIG.onda_pwm(),
         "Tres ciclos de trabajo sobre la misma frecuencia. La onda no cambia "
         "de altura ni de ritmo: lo único que cambia es cuánto dura la parte "
         "alta, y con ella el valor medio.", capitulo=5))

A(aviso("Dos escalas para lo mismo", p(
    "MicroPython ofrece dos maneras de fijar el ciclo de trabajo y no son "
    "intercambiables. <code>duty()</code> trabaja sobre <b>1023</b> y "
    "<code>duty_u16()</code> sobre <b>65535</b>. Escribir "
    "<code>duty(32767)</code> pensando en la mitad no da la mitad: da el "
    "máximo, porque cualquier valor por encima de 1023 se satura.",
    "Este libro usa <code>duty()</code> donde el valor viene del conversor "
    "analógico —que también entrega una escala corta— y "
    "<code>duty_u16()</code> donde el valor se escribe a mano. Cada "
    "laboratorio dice cuál, y mezclarlas es la causa más común de que un "
    "programa de PWM «no haga nada» o «esté siempre al máximo».")))

A(sec("Qué frecuencia conviene"))

A(tabla(
    ["Aplicación", "Frecuencia", "Por qué"],
    [["LED, iluminación", "500 – 5000 Hz",
      "Por debajo de unos 100 Hz el parpadeo se nota, sobre todo al mover la "
      "vista."],
     ["Motor de corriente continua", "1 – 20 kHz",
      "Por debajo de 1 kHz el motor chilla: la propia bobina reproduce la "
      "frecuencia de conmutación."],
     ["Servomotor", "<b>50 Hz, fija</b>",
      "No es una elección: el servo espera un pulso cada 20 ms y mide su "
      "ancho. Ver el laboratorio 5.3."],
     ["Zumbador pasivo", "la nota que se quiera",
      "Aquí la frecuencia <i>es</i> la información: 440 Hz es un la."]]))

A(nota("El caso del servomotor es distinto", p(
    "En los tres primeros casos lo que importa es el ciclo de trabajo y la "
    "frecuencia es un detalle de implementación. En el servomotor ocurre al "
    "revés: la frecuencia está fijada por la norma y lo que el servo mide es "
    "el <b>ancho del pulso en milisegundos</b>. El ciclo de trabajo es apenas "
    "la manera que tiene MicroPython de expresar ese ancho. Tenerlo claro "
    "evita el error del laboratorio 5.4.")))

# =================================================================== 5.2
A(lab("5.2", "Brillo de un LED gobernado por un potenciómetro"))

A(sec("Objetivo"))
A(p("Unir la entrada analógica del capítulo 3 con la salida modulada de éste: "
    "leer la posición de una perilla y convertirla en brillo."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["1", "Potenciómetro de 10 kΩ"],
         ["1", "LED de 5 mm y resistencia de 330 Ω"],
         ["—", "Cables de conexión"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_5_2")[0], ancha=True, epigrafe=
         "El potenciómetro va a GPIO34, que pertenece al ADC1 y está en la "
         "columna opuesta: su cable rodea la placa. El LED cuelga de GPIO18, "
         "que sí admite PWM.", capitulo=5))

A(aviso("Por qué GPIO34 y no cualquier otro", p(
    "El cursor del potenciómetro tiene que ir a una pata del <b>ADC1</b>. En "
    "este laboratorio todavía no hay WiFi y el ADC2 funcionaría, pero en el "
    "capítulo 7 este mismo montaje va a publicar su lectura en internet, y "
    "entonces el ADC2 dejaría de medir. Cablearlo bien desde ahora ahorra "
    "rehacerlo después.",
    "Obsérvese además que GPIO34 es uno de los cuatro pines que <b>sólo "
    "pueden ser entrada</b>. Para un potenciómetro es perfecto; para el LED "
    "no serviría.")))

A(sec("Razonamiento"))

A(p(
    "El conversor entrega un número de 0 a 4095, porque tiene 12 bits. El "
    "PWM acepta de 0 a 1023, porque <code>duty()</code> trabaja con 10 bits. "
    "Hay que llevar una escala a la otra, y como 4096 es exactamente cuatro "
    "veces 1024, basta con dividir entre cuatro.",

    "Dividir entre cuatro es desplazar dos lugares en binario, y eso es lo "
    "que hace <code>cuentas >> 2</code>. Podría escribirse "
    "<code>cuentas // 4</code> y el resultado sería idéntico; se usa el "
    "desplazamiento porque es la forma habitual en programación de "
    "microcontroladores y conviene reconocerla al leer código ajeno.",

    "No hay que redondear ni ajustar nada más: el extremo bajo del "
    "potenciómetro da 0, que apaga el LED, y el alto da 4095, que al "
    "desplazarse queda en 1023, el máximo."))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM, ADC
import time

led = PWM(Pin(18), freq=1000)
led.duty(0)

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)      # rango de entrada de 0 a 3,3 V

DUTY_MAXIMO = 1023            # duty() trabaja con 10 bits

while True:
    cuentas = pot.read()      # 0 a 4095, porque el ADC tiene 12 bits

    # Cuatro mil noventa y seis niveles no entran en mil veinticuatro.
    # Desplazar dos lugares a la derecha divide entre cuatro y ajusta
    # una escala a la otra sin perder el extremo: 4095 >> 2 da 1023.
    brillo = cuentas >> 2

    led.duty(brillo)
    print("Perilla: {:4d}    Brillo: {:4d}  ({:3.0f} %)".format(
        cuentas, brillo, brillo * 100 / DUTY_MAXIMO))
    time.sleep(0.1)""", archivo="lab_5_2_brillo.py"))

A(sec("Qué debe observarse"))
A(p(
    "Al girar la perilla el LED pasa de apagado a pleno brillo de manera "
    "continua, y la consola muestra las dos escalas en paralelo. Vale la pena "
    "mirar los números: la columna de la izquierda avanza de cuatro en cuatro "
    "por cada unidad de la derecha.",

    "El brillo no se percibe proporcional a la cifra. Entre el 0 y el 20 % el "
    "cambio se nota mucho; entre el 80 y el 100 %, casi nada. No es un defecto "
    "del montaje: el ojo responde de manera logarítmica, y es el motivo por el "
    "cual los reguladores de iluminación comerciales no usan una recta. El "
    "ejercicio 3 propone corregirlo."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El LED está siempre encendido al máximo",
      "Se usó <code>duty_u16()</code> con un valor pensado para "
      "<code>duty()</code>, o al revés."],
     ["El brillo no llega nunca al máximo",
      "Falta <code>atten(ADC.ATTN_11DB)</code>: sin esa línea el conversor "
      "satura cerca de 1,1 V y nunca alcanza las 4095 cuentas."],
     ["El LED parpadea de manera visible",
      "La frecuencia quedó por debajo de unos 100 Hz."],
     ["La lectura salta sola con la perilla quieta",
      "El cursor no hace buen contacto, o el potenciómetro no tiene sus dos "
      "extremos conectados."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el regulador de intensidad de "
    "un circuito de iluminación, o la consigna de velocidad de un variador. "
    "El potenciómetro se reemplaza por la señal de 0 a 10 V de un mando "
    "remoto —acondicionada con el divisor del laboratorio 3.2— y el LED por "
    "la etapa de potencia.",
    "<b>En el área mecánica</b>, es la atenuación de la iluminación del tablero, "
    "que en el vehículo se manda con una rueda dentada idéntica a este "
    "potenciómetro. El mismo programa, con otra etapa de salida.")))

# =================================================================== 5.3
A(lab("5.3", "El servomotor: la posición va en el ancho del pulso"))

A(sec("Objetivo"))
A(p("Llevar un servomotor a un ángulo determinado y entender por qué aquí el "
    "ciclo de trabajo no significa «intensidad»."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Servomotor SG90", "el de 9 g, con sus aspas"],
         ["—", "Cables de conexión", ""]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_5_3")[0], ancha=True, epigrafe=
         "Los tres cables del SG90 tienen colores normalizados: marrón a masa, "
         "rojo a la alimentación y naranja a la señal.", capitulo=5))

A(aviso("Alimentación del servo", p(
    "El servo va a <code>VIN</code>, no a <code>3V3</code>. Con 3,3 V puede "
    "llegar a moverse en vacío, pero apenas encuentra resistencia consume un "
    "pico de corriente que el regulador de 3,3 V no sostiene, y la placa se "
    "reinicia sola. El síntoma es un servo que da un tirón y un ESP32 que "
    "vuelve a arrancar.",
    "Si el servo mueve carga, conviene alimentarlo de una fuente aparte de "
    "5 V y unir <b>solamente las masas</b> de las dos fuentes. Alimentarlo "
    "desde el USB del computador a través de la placa está bien para el "
    "laboratorio y no para nada más.")))

A(sec("Razonamiento"))

A(p(
    "El servomotor no interpreta el ciclo de trabajo como una cantidad. "
    "Espera un pulso cada 20 milisegundos —de ahí los 50 Hz, que no son "
    "negociables— y <b>mide cuánto dura ese pulso</b>. Un pulso de 1 ms lo "
    "manda a un extremo del recorrido; uno de 2 ms, al otro; uno de 1,5 ms, "
    "al centro. Entre medio interpola.",

    "MicroPython no permite pedir «un pulso de 1,5 ms»: pide un ciclo de "
    "trabajo. Hay entonces que traducir, y la cuenta es directa. Con "
    "<code>duty()</code>, que va de 0 a 1023, y un período de 20 ms:"))

A(codigo("""ancho_del_pulso = duty / 1023 * 20 ms"""))

A(p("De donde salen los dos extremos que usa este libro:"))

A(tabla(
    ["Ciclo de trabajo", "Ancho del pulso", "Posición"],
    [["<code>40</code>", "0,78 ms", "un extremo, cerca de 0°"],
     ["<code>77</code>", "1,51 ms", "el centro, 90°"],
     ["<code>115</code>", "2,25 ms", "el otro extremo, cerca de 180°"],
     ["<code>150</code>", "<b>2,93 ms</b>",
      "<b>fuera de rango: el tope mecánico</b>"]],
    centradas=(0, 1)))

A(p(
    "Los valores exactos varían de un servo a otro, y por eso están en "
    "constantes al principio del programa. La manera de ajustarlos es "
    "empírica: bajar <code>DUTY_MINIMO</code> hasta que el servo deje de "
    "moverse, y subir <code>DUTY_MAXIMO</code> hasta lo mismo, retrocediendo "
    "después un par de unidades."))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import time

servo = PWM(Pin(4), freq=50)     # 50 Hz: un ciclo cada 20 ms

DUTY_MINIMO = 40                 # unos 0,78 ms, extremo de 0 grados
DUTY_MAXIMO = 115                # unos 2,25 ms, extremo de 180 grados
RECORRIDO = DUTY_MAXIMO - DUTY_MINIMO


def angulo_a_duty(angulo):
    \"\"\"Convierte un angulo de 0 a 180 grados en ciclo de trabajo.

    Los dos extremos se recortan a proposito. Pedir 200 grados no
    consigue mas recorrido: manda al servo contra su tope, donde
    zumba, se calienta y termina rompiendo el engranaje de salida.
    \"\"\"
    if angulo < 0:
        angulo = 0
    if angulo > 180:
        angulo = 180
    return int(angulo * RECORRIDO / 180 + DUTY_MINIMO)


for angulo in (0, 45, 90, 135, 180, 90):
    servo.duty(angulo_a_duty(angulo))
    print("{:3d} grados  ->  duty {:3d}".format(
        angulo, angulo_a_duty(angulo)))
    time.sleep(1)

servo.deinit()                   # suelta el pin y deja de mandar pulsos""",
    archivo="lab_5_3_servo.py"))

A(nota("Por qué termina con deinit()", p(
    "Mientras el ESP32 siga mandando pulsos, el servo sigue sosteniendo la "
    "posición, y para sostenerla consume corriente y se calienta. "
    "<code>deinit()</code> apaga la salida y lo deja libre. En un montaje que "
    "sólo posiciona de vez en cuando —una compuerta, una válvula— esto es lo "
    "correcto; en uno que debe resistir una fuerza, no.")))

A(sec("Qué debe observarse"))
A(p(
    "El aspa se detiene en cinco posiciones bien diferenciadas y vuelve al "
    "centro. Conviene marcar con lápiz la posición del aspa a 0° y a 180° y "
    "comprobar que el recorrido se acerca a media vuelta. Si queda "
    "notablemente corto, los valores de las dos constantes son conservadores "
    "para ese servo y pueden ampliarse."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El servo zumba y se calienta sin moverse",
      "Está contra el tope: el ciclo de trabajo se fue del rango. Es el error "
      "que corrige el laboratorio siguiente."],
     ["La placa se reinicia al mover el servo",
      "Alimentación insuficiente. Es el caso del recuadro anterior."],
     ["No se mueve en absoluto",
      "La frecuencia no es 50 Hz, o el cable naranja no llegó al pin."],
     ["Tiembla en reposo",
      "Normal en los servos económicos. Se reduce con <code>deinit()</code> "
      "una vez alcanzada la posición."]]))

# =================================================================== 5.4
A(lab("5.4", "Barrido continuo"))

A(sec("Objetivo"))
A(p("Recorrer todo el rango de manera suave, y entender por qué el límite "
    "superior no puede elegirse al azar."))

A(sec("El circuito"))
A(p("El mismo del laboratorio 5.3, sin cambios."))

A(sec("Razonamiento"))

A(p(
    "Un barrido es la repetición del posicionamiento anterior sobre una "
    "sucesión de ángulos. Lo único que hay que decidir es el paso y la espera "
    "entre pasos: juntos determinan la velocidad aparente. Dos grados cada "
    "30 milisegundos dan un recorrido completo en unos 2,7 segundos, que se "
    "ve fluido sin ser brusco.",

    "Este laboratorio se incluye sobre todo por el error que contenía. La "
    "versión de la que parte llevaba el ciclo de trabajo hasta <b>150</b>, "
    "convencida de que así se aprovechaba todo el recorrido. Con la fórmula "
    "del laboratorio anterior, 150 equivale a un pulso de <b>2,93 ms</b>, muy "
    "por encima de los 2,4 ms que el SG90 admite. El servo no gira más: llega "
    "a su tope y empuja contra él en cada barrido.",

    "El síntoma es engañoso, porque el servo <i>parece</i> funcionar. Zumba un "
    "poco en los extremos y se calienta, y a las pocas horas el engranaje de "
    "salida —que es de plástico— pierde dientes. Por eso el recorrido se "
    "recorta en el propio conversor de ángulos y no en el lazo: así ningún "
    "programa que use esa función puede pasarse, aunque se equivoque al "
    "llamarla."))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import time

servo = PWM(Pin(4), freq=50)

DUTY_MINIMO = 40
DUTY_MAXIMO = 115                # 2,25 ms. Subirlo a 150 da 2,93 ms:
RECORRIDO = DUTY_MAXIMO - DUTY_MINIMO     # el tope mecanico del servo

PASO = 2                         # grados por escalon
ESPERA_MS = 30                   # cuanto se detiene en cada escalon


def angulo_a_duty(angulo):
    \"\"\"Recorta el angulo ANTES de convertirlo, de modo que ningun
    programa que use esta funcion pueda mandar al servo al tope.\"\"\"
    if angulo < 0:
        angulo = 0
    if angulo > 180:
        angulo = 180
    return int(angulo * RECORRIDO / 180 + DUTY_MINIMO)


def barrer(desde, hasta):
    paso = PASO if hasta > desde else -PASO
    for angulo in range(desde, hasta + paso, paso):
        servo.duty(angulo_a_duty(angulo))
        time.sleep_ms(ESPERA_MS)


while True:
    barrer(0, 180)
    barrer(180, 0)
    print("Barrido completo")""", archivo="lab_5_4_barrido.py"))

A(sec("Qué debe observarse"))
A(p(
    "El aspa recorre media vuelta de ida y de vuelta sin tirones, y la consola "
    "escribe una línea por ciclo completo. En los extremos el servo debe "
    "<b>callarse</b>: si zumba, todavía está llegando al tope y hay que bajar "
    "<code>DUTY_MAXIMO</code> de a cinco unidades hasta que deje de hacerlo."))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, un servomotor de este tipo mueve "
    "compuertas de ventilación, válvulas de tres vías y desviadores en cintas "
    "transportadoras. El recorte del recorrido no es una precaución teórica: "
    "es el equivalente al final de carrera de una máquina, y en un actuador "
    "grande la diferencia entre recortarlo y no hacerlo es una reparación.",
    "<b>En el área mecánica</b>, el mismo esquema gobierna las compuertas del "
    "sistema de climatización y el actuador de ralentí. Los servos del "
    "vehículo trabajan con realimentación de posición, pero el pulso de mando "
    "responde a la misma norma de 20 ms que se usa aquí.")))

# =================================================================== 5.5
A(lab("5.5", "Tonos y sirena con zumbador pasivo"))

A(sec("Objetivo"))
A(p("Usar la frecuencia como información, no como detalle: aquí lo que se "
    "controla es la nota."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Zumbador <b>pasivo</b>", "el activo no sirve"],
         ["—", "Cables de conexión", ""]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_5_5")[0], ancha=True, epigrafe=
         "El zumbador pasivo no tiene oscilador propio: la frecuencia se la "
         "entrega el pin, y por eso se lo puede hacer sonar en cualquier nota.",
         capitulo=5))

A(nota("Cómo distinguir un zumbador pasivo de uno activo", p(
    "Mirados por debajo, el activo suele venir sellado con resina y el pasivo "
    "deja ver la bobina. La prueba segura es conectarlo un instante a 3,3 V "
    "continuos: el <b>activo</b> suena con una nota fija; el <b>pasivo</b> "
    "hace un chasquido y se calla. Sólo este último sirve para el "
    "laboratorio.")))

A(sec("Razonamiento"))

A(p(
    "Aquí se invierte todo lo dicho hasta ahora. La frecuencia deja de ser un "
    "detalle de implementación y pasa a ser el dato: 440 Hz es un la, 880 Hz "
    "es el la de la octava siguiente. El ciclo de trabajo, en cambio, casi no "
    "importa, y se deja en la mitad porque ahí la onda cuadrada es simétrica y "
    "el tono sale más limpio.",

    "Un detalle de programación que vale para todo el libro: el zumbador debe "
    "quedar callado cuando el programa termina. Si se interrumpe con "
    "<code>Ctrl+C</code> a mitad de un tono, el PWM sigue funcionando por su "
    "cuenta y el zumbador sigue sonando hasta que se reinicie la placa. El "
    "programa atrapa esa interrupción y lo apaga."))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import time

buzzer = PWM(Pin(5))
buzzer.duty_u16(0)              # arranca en silencio

MITAD = 32767                   # 50 % de 65535: onda cuadrada simetrica
NOTAS = (("do", 262), ("re", 294), ("mi", 330), ("fa", 349),
         ("sol", 392), ("la", 440), ("si", 494))

try:
    print("Escala")
    buzzer.duty_u16(MITAD)
    for nombre, hz in NOTAS:
        buzzer.freq(hz)
        print("  {:4s} {:3d} Hz".format(nombre, hz))
        time.sleep_ms(400)

    print("Sirena. Interrumpa con Ctrl+C.")
    while True:
        for hz in (400, 800):
            buzzer.freq(hz)
            time.sleep_ms(200)

except KeyboardInterrupt:
    pass

finally:
    # Pase lo que pase, el zumbador queda callado. Sin esto, una
    # interrupcion a mitad de un tono lo deja sonando hasta que
    # alguien reinicie la placa.
    buzzer.duty_u16(0)
    buzzer.deinit()
    print("Silencio.")""", archivo="lab_5_5_buzzer.py"))

A(sec("Qué debe observarse"))
A(p(
    "Primero suena una escala de siete notas, cada una un poco más aguda, y "
    "después arranca la sirena de dos tonos. Al interrumpir con "
    "<code>Ctrl+C</code> el zumbador se calla de inmediato y la consola "
    "escribe la última línea."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Suena siempre la misma nota",
      "Es un zumbador activo. No hay programa que lo arregle."],
     ["No suena nada",
      "Falta <code>duty_u16(MITAD)</code>: fijar la frecuencia no basta, "
      "hay que abrir el ciclo de trabajo."],
     ["Sigue sonando después de detener el programa",
      "Se ejecutó una versión sin el bloque <code>finally</code>. El botón "
      "<b>EN</b> lo calla."],
     ["El sonido es muy débil",
      "Normal: el zumbador pasivo suena poco alimentado desde un pin. No "
      "conviene subir la corriente; si hace falta volumen, va un transistor."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, la sirena de dos tonos es la señal "
    "acústica de alarma de una máquina, y la escala sirve para distinguir "
    "avisos: un tono grave para el arranque inminente, uno agudo para la "
    "parada de emergencia. Que el programa pueda elegir la nota es lo que "
    "permite codificar el tipo de aviso con un solo zumbador.",
    "<b>En el área mecánica</b>, es el avisador acústico del tablero. Un solo "
    "elemento distingue el cinturón sin abrochar, la puerta abierta y la "
    "marcha atrás, cambiando frecuencia y cadencia.")))

A(ejercicios([
    "En el laboratorio 5.2, invierta el sentido: que el LED esté al máximo "
    "con la perilla al mínimo. ¿Hace falta tocar el cableado?",

    "Modifique el 5.2 para que el brillo cambie por escalones de 10 %, en "
    "lugar de hacerlo de manera continua. ¿Cuántos niveles distintos quedan?",

    "El ojo percibe el brillo de manera aproximadamente logarítmica. Sustituya "
    "<code>brillo = cuentas >> 2</code> por una relación cuadrática "
    "—<code>brillo = cuentas * cuentas // 16392</code>— y compare. ¿Cuál de "
    "las dos se siente más uniforme al girar la perilla?",

    "Con el potenciómetro del 5.2 y el servo del 5.3, escriba un programa que "
    "posicione el servo según la perilla. Recorte el recorrido como corresponde.",

    "Calcule qué ciclo de trabajo produce un pulso de 1,5 ms a 50 Hz usando "
    "<code>duty_u16()</code> en lugar de <code>duty()</code>. Verifique que el "
    "servo va al centro.",

    "En el laboratorio 5.5, escriba una función <code>tono(hz, ms)</code> que "
    "suene una nota y se calle, y úsela para tocar una melodía corta a partir "
    "de una lista de pares.",

    "Un LED regulado al 50 % de ciclo de trabajo, ¿consume la mitad de "
    "corriente media que al 100 %? ¿Y disipa la mitad de potencia? Justifique.",
]))
