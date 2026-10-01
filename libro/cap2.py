# -*- coding: utf-8 -*-
"""Capítulo 2 — Entradas y salidas digitales."""
from maqueta import (capitulo, lab, sec, codigo, circuito, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import circuitos_cap2 as CIR

PARTES = []
A = PARTES.append

A(capitulo(2, "Entradas y salidas digitales", p(
    "Una señal digital sólo tiene dos estados. Está o no está, conduce o no conduce, "
    "hay presencia o no la hay. Es la más simple de todas las que trata este libro y "
    "por eso es la primera, pero conviene no subestimarla: el final de carrera de una "
    "máquina, el presostato de un compresor, el contacto de una puerta, el "
    "interruptor de nivel de un tanque y el sensor de cinturón de un vehículo son "
    "todos señales digitales, y buena parte de la automatización real se hace con "
    "ellas.",

    "Los cuatro laboratorios de este capítulo recorren el camino completo: primero "
    "gobernar una salida, después coordinar varias, después leer una entrada y "
    "finalmente hacer que una entrada gobierne una salida. Al terminarlo, el lector "
    "tendrá armado un sistema de alarma que funciona, y lo habrá hecho con un solo "
    "tipo de señal.")))

# =================================================================== 2.1
A(lab("2.1", "Gobernar una salida digital"))

A(sec("Objetivo"))
A(p("Encender y apagar un LED externo desde un pin de la placa, y entender por qué "
    "la resistencia en serie no es opcional."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "LED de 5 mm", "de cualquier color"],
         ["1", "Resistencia de 330 Ω", "limita la corriente"],
         ["—", "Cables de conexión", ""]],
        centradas=(0,)))

A(sec("El circuito"))

A(p(
    "El LED tiene una pata larga (<b>ánodo</b>, positiva) y una corta (<b>cátodo</b>, "
    "negativa). La corriente entra por la larga y sale por la corta. La resistencia va "
    "en serie, y puede ir de cualquiera de los dos lados:"))

A(figura(CIR.svg('lab_2_1')[0], ancha=True, epigrafe= "Circuito del laboratorio 2.1. El ánodo va siempre al pin y el cátodo siempre a masa: así value(1) significa encendido.", capitulo=2))

A(aviso("Un detalle que invierte toda la lógica", p(
    "Existe la tentación de conectar el ánodo a <code>3V3</code> y el cátodo al pin, "
    "porque el LED igual enciende. Pero entonces enciende cuando el pin está en "
    "<b>bajo</b>, de modo que <code>led.value(1)</code> lo <b>apaga</b> y "
    "<code>led.value(0)</code> lo <b>enciende</b>. Todo el programa queda con el "
    "significado invertido, y cuando el montaje crece a tres o cuatro luces el error se "
    "vuelve muy difícil de rastrear.",
    "En este libro el ánodo va siempre al pin y el cátodo siempre a masa. Así "
    "<code>value(1)</code> significa encendido, que es lo que cualquiera espera al "
    "leer el programa.")))

A(nota("Por qué 330 Ω", p(
    "Un LED rojo cae alrededor de 2 V cuando conduce. Con los 3,3 V del pin quedan "
    "1,3 V sobre la resistencia, y con 330 Ω la corriente resulta de unos 4 mA: "
    "suficiente para que se vea bien y muy por debajo de lo que el pin puede entregar. "
    "Sin resistencia, la corriente sólo queda limitada por la resistencia interna del "
    "LED y del pin, y se destruyen los dos.")))

A(sec("Razonamiento"))

A(p(
    "El programa es el mismo del laboratorio 1.5, cambiando el número de pin. Vale la "
    "pena detenerse en eso: para el microcontrolador no hay ninguna diferencia entre el "
    "LED soldado a la placa y uno puesto en la protoboard. Lo que cambia es el "
    "circuito, no el algoritmo. Esta separación —el programa de un lado, la etapa de "
    "potencia del otro— es la que permitirá más adelante reemplazar el LED por un relé "
    "sin tocar una sola línea."))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time

led = Pin(23, Pin.OUT)

ENCENDIDO_S = 0.5
APAGADO_S = 0.5

while True:
    led.value(1)
    print("encendido")
    time.sleep(ENCENDIDO_S)

    led.value(0)
    print("apagado")
    time.sleep(APAGADO_S)""", archivo="lab_2_1_salida_digital.py"))

A(nota("Los tiempos van en constantes", p(
    "Los dos tiempos están en constantes con nombre, escritas en mayúsculas al "
    "principio del programa, en lugar de repetidos como números sueltos dentro de la "
    "repetición. Es una costumbre que este libro sostiene en todos sus programas: "
    "cuando haya que ajustar un tiempo, un umbral o un pin, está en un solo lugar "
    "visible y no hay que buscarlo entre las líneas.")))

A(sec("Qué debe observarse"))
A(p("El LED parpadea una vez por segundo. Si se aumenta <code>ENCENDIDO_S</code> y se "
    "disminuye <code>APAGADO_S</code>, el LED pasa más tiempo encendido sin cambiar la "
    "cantidad de parpadeos por minuto."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El LED no enciende nunca",
      "Está al revés. La pata larga debe mirar hacia el pin. Invertirlo no lo daña: "
      "simplemente no conduce."],
     ["Enciende cuando el programa dice apagado",
      "El ánodo quedó en 3V3 en lugar del pin. Es el caso del recuadro anterior."],
     ["Enciende muy débil",
      "La resistencia es de un valor mucho mayor que 330 Ω. Verificar el código de "
      "colores."],
     ["El LED enciende fijo y no parpadea",
      "El programa no está corriendo: quedó una versión anterior en la placa, o la "
      "ejecución se detuvo con un error que aparece en la consola."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el piloto de señalización de un "
    "tablero. Cambiando la resistencia y el LED por un módulo de relé conectado al "
    "mismo pin, el programa gobierna una lámpara de 220 V sin que se modifique una "
    "sola línea.",
    "<b>En el área mecánica</b>, es una luz testigo del panel de instrumentos. La estructura "
    "encender–esperar–apagar–esperar es exactamente la de un intermitente de giro, y "
    "sólo hay que ajustar los tiempos a los que fija la norma.")))

# =================================================================== 2.2
A(lab("2.2", "Coordinar varias salidas: el semáforo"))

A(sec("Objetivo"))
A(p("Gobernar tres salidas que deben respetar una secuencia, garantizando que en "
    "ningún instante haya dos encendidas a la vez."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["3", "LED de 5 mm: rojo, amarillo y verde"],
         ["3", "Resistencias de 330 Ω"],
         ["—", "Cables de conexión"]],
        centradas=(0,)))

A(sec("El circuito"))
A(p("Los tres LED se conectan igual que el del laboratorio anterior, cada uno a su "
    "pin y con su resistencia:"))

A(figura(CIR.svg('lab_2_2')[0], ancha=True, epigrafe= "Circuito del semáforo. Cada luz tiene su pin y su resistencia; los tres cátodos comparten la línea de masa.", capitulo=2))

A(sec("Razonamiento"))

A(p(
    "La tentación es escribir la secuencia tal como se la describe en voz alta: "
    "«enciendo el verde, espero cinco segundos, apago el verde, enciendo el amarillo…». "
    "Ese orden esconde un defecto. Si el apagado del LED anterior se escribe "
    "<b>después</b> de la espera, durante esos cinco segundos quedan encendidas dos "
    "luces: la nueva y la que venía de la fase anterior. En un semáforo de juguete se "
    "ve raro; en un enclavamiento real es una falla de seguridad.",

    "La corrección no es agregar apagados, sino cambiar de idea sobre qué se está "
    "programando. No hay tres luces que se encienden y se apagan por separado: hay un "
    "<b>estado</b>, y en cada estado hay exactamente una luz encendida. Escrito así, "
    "es imposible que queden dos prendidas, porque cada cambio de estado fija las tres "
    "de una vez.",

    "Ese cambio de enfoque se traduce en una función que recibe cuál debe quedar "
    "encendida y se ocupa de las otras dos. La repetición principal se vuelve la "
    "lectura directa de la secuencia."))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time

rojo = Pin(23, Pin.OUT)
amarillo = Pin(21, Pin.OUT)
verde = Pin(17, Pin.OUT)

SEGUNDOS_ROJO = 5
SEGUNDOS_VERDE = 5
SEGUNDOS_AMARILLO = 2


def encender(cual, segundos, mensaje):
    \"\"\"Deja encendida una sola luz y apaga las otras dos.

    Fijar las tres en la misma instruccion es lo que garantiza que
    en ningun instante haya dos encendidas a la vez.
    \"\"\"
    rojo.value(1 if cual is rojo else 0)
    amarillo.value(1 if cual is amarillo else 0)
    verde.value(1 if cual is verde else 0)
    print(mensaje)
    time.sleep(segundos)


while True:
    encender(rojo, SEGUNDOS_ROJO, "Rojo - alto")
    encender(verde, SEGUNDOS_VERDE, "Verde - avance")
    encender(amarillo, SEGUNDOS_AMARILLO, "Amarillo - precaucion")""",
    archivo="lab_2_2_semaforo.py"))

A(nota("Dónde se lee la secuencia", p(
    "Las tres últimas líneas del programa son la secuencia completa del semáforo, en "
    "orden y en castellano. Cualquiera puede leerlas y decir si el ciclo es correcto, "
    "sin entender nada de lo que hay más arriba. Cuando un programa se deja escribir "
    "así, las modificaciones se vuelven seguras: agregar una fase de intermitente "
    "nocturno es agregar una línea, no reescribir la lógica.")))

A(sec("Qué debe observarse"))
A(p("El ciclo dura doce segundos y en todo momento hay exactamente una luz encendida. "
    "Conviene mirar con atención el instante del cambio: no debe haber ningún momento, "
    "por breve que sea, con dos luces prendidas ni con las tres apagadas."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Quedan dos luces encendidas a la vez",
      "El programa en uso todavía apaga <i>después</i> de la espera. Es el defecto que "
      "este laboratorio corrige."],
     ["Una luz no enciende nunca",
      "El LED está invertido, o el pin del programa no es aquel en el que se cableó."],
     ["Las tres encienden juntas y no cambian",
      "Se cablearon los tres ánodos al mismo pin, o los tres pines quedaron unidos en "
      "la misma fila de la protoboard."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, esta estructura es la de una secuencia de "
    "proceso con enclavamiento: tres etapas que deben sucederse y que nunca pueden "
    "coincidir, como el arranque estrella-triángulo de un motor, donde energizar los "
    "dos contactores a la vez provoca un cortocircuito franco. La función "
    "<code>encender()</code> es, literalmente, el enclavamiento.",
    "<b>En el área mecánica</b>, es la secuencia de un tablero al dar contacto: testigos que "
    "se encienden en orden durante la comprobación inicial, y luces de giro que no "
    "pueden estar activas en ambos lados simultáneamente.")))

# =================================================================== 2.3
A(lab("2.3", "Leer una entrada digital: el pulsador"))

A(sec("Objetivo"))
A(p("Leer el estado de un pulsador, filtrar el rebote mecánico del contacto y "
    "conseguir que cada pulsación cambie el estado del LED y lo mantenga."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["1", "Pulsador de cuatro patas para protoboard"],
         ["1", "LED de 5 mm y resistencia de 330 Ω"],
         ["—", "Cables de conexión"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg('lab_2_3')[0], ancha=True, epigrafe= "Circuito del pulsador. Un solo polo en el botón: el pin de un lado y la masa del otro, nunca 3V3 y GND enfrentados.", capitulo=2))

A(aviso("Nunca los dos polos en el pulsador", p(
    "Un montaje que se ve con frecuencia lleva <code>GND</code> a un lado del pulsador "
    "y <code>3V3</code> al otro, con el pin tomando la lectura del medio. Al presionar, "
    "eso une los 3,3 V con masa: es un <b>cortocircuito franco</b> sobre la "
    "alimentación de la placa. Puede que el regulador lo soporte un tiempo, y por eso "
    "el error sobrevive; pero calienta, provoca reinicios y termina dañando la placa.",
    "La conexión correcta usa <b>un solo polo</b>. Una pata al pin, la otra a masa, y "
    "nada más. El nivel en reposo lo provee la resistencia interna de la que se habla "
    "enseguida. Algunos simuladores admiten el otro montaje sin consecuencias, porque "
    "no simulan la corriente; sobre la protoboard sí las hay.")))

A(sec("La resistencia interna de elevación"))

A(p(
    "Con una sola pata a masa, el pin queda sin conexión mientras el pulsador está "
    "suelto. Un pin así no lee ni 0 ni 1: lee ruido, y cambia de valor solo. Hace falta "
    "algo que lo mantenga en un nivel conocido mientras nadie lo toca.",

    "El ESP32 trae ese algo adentro. Declarando el pin con <code>Pin.PULL_UP</code> se "
    "conecta internamente una resistencia hacia los 3,3 V, de modo que:"))

A(tabla(
    ["Estado del pulsador", "Lectura del pin", "Por qué"],
    [["Suelto", "<b>1</b>", "La resistencia interna lo mantiene elevado."],
     ["Presionado", "<b>0</b>", "El pulsador lo une directamente a masa."]],
    centradas=(1,)))

A(p(
    "La lectura queda entonces invertida respecto de la intuición: presionado es cero. "
    "Por eso el programa empieza con <code>pulsado = not pulsador.value()</code>, que "
    "traduce la lectura eléctrica al significado que interesa y permite que el resto "
    "del programa se lea en castellano."))

A(sec("Razonamiento"))

A(p(
    "Un pulsador mecánico no cambia de estado limpiamente. Las láminas del contacto "
    "rebotan durante unos milisegundos, y en ese lapso el pin lee una ráfaga de ceros y "
    "unos. Un programa que actúe ante cada cambio verá diez o quince pulsaciones donde "
    "el dedo hizo una sola. Es el motivo por el cual un LED «no responde» o «responde "
    "al azar»: en realidad responde de más.",

    "El filtro consiste en exigir que entre dos cambios aceptados haya transcurrido un "
    "tiempo mínimo, mayor que la duración del rebote y menor que el intervalo entre dos "
    "pulsaciones humanas. Cincuenta milisegundos cumplen ambas condiciones con holgura.",

    "Hay además una segunda decisión. Interesa el instante en que el pulsador "
    "<b>se presiona</b>, no el que se suelta, porque si no cada pulsación produciría dos "
    "cambios y el LED volvería siempre a su estado original. Y el estado del LED se "
    "guarda en una variable propia: el pulsador no manda sobre la luz, manda sobre el "
    "<b>cambio</b> de la luz. Eso es lo que hace que quede encendida al soltar."))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time

pulsador = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(5, Pin.OUT)

REBOTE_MS = 50

encendido = False
estaba_pulsado = False
ultimo_cambio = time.ticks_ms()

print("Pulse el boton para encender y apagar el LED.")

while True:
    pulsado = not pulsador.value()      # el pulsador une el pin a masa
    ahora = time.ticks_ms()

    hubo_cambio = pulsado != estaba_pulsado
    paso_el_rebote = time.ticks_diff(ahora, ultimo_cambio) > REBOTE_MS

    if hubo_cambio and paso_el_rebote:
        estaba_pulsado = pulsado
        ultimo_cambio = ahora

        # Solo interesa cuando se presiona, no cuando se suelta.
        if pulsado:
            encendido = not encendido
            led.value(1 if encendido else 0)
            print("LED encendido" if encendido else "LED apagado")

    time.sleep_ms(10)""", archivo="lab_2_3_pulsador.py"))

A(sec("Qué debe observarse"))

A(p(
    "Cada pulsación cambia el estado del LED y lo deja así al soltar. La consola "
    "escribe <b>una sola línea</b> por pulsación. Vale la pena hacer la prueba "
    "inversa: poner <code>REBOTE_MS = 0</code> y volver a ejecutar. Aparecerán varias "
    "líneas por cada toque, y a veces el LED quedará en el estado contrario al "
    "esperado. Ese es el rebote, visto de frente."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El LED cambia solo, sin tocar nada",
      "Falta <code>Pin.PULL_UP</code> en la declaración, y el pin está leyendo ruido."],
     ["Hay que mantener presionado para que quede encendido",
      "Se está ejecutando la versión sin memoria de estado, la que copia la lectura "
      "directamente a la salida."],
     ["Una pulsación produce varias líneas en la consola",
      "El tiempo de rebote es demasiado corto para ese pulsador. Subirlo a 80 ms."],
     ["No responde nunca",
      "Las dos patas cableadas pertenecen al mismo contacto interno. Un pulsador de "
      "cuatro patas tiene dos pares unidos de fábrica: hay que tomar una pata de cada "
      "par, es decir, las que están en diagonal."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el pulsador de marcha con "
    "enclavamiento: se presiona un instante y el equipo queda en marcha. La variable "
    "<code>encendido</code> cumple el papel del contacto de retención en un esquema de "
    "mando, y el filtro de rebote hace lo mismo que el tiempo de un temporizador "
    "antiparasitario en un autómata programable.",
    "<b>En el área mecánica</b>, es el botón de arranque por pulsación: se toca una vez y el "
    "sistema queda activo. El mismo filtro es el que impide que la vibración del motor "
    "produzca accionamientos falsos en los mandos del volante.")))

# =================================================================== 2.4
A(lab("2.4", "Una entrada que gobierna una salida: alarma con sensor PIR"))

A(sec("Objetivo"))
A(p("Detectar movimiento con un sensor infrarrojo pasivo y hacer sonar una sirena, "
    "sin que el sonido impida seguir vigilando."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Sensor PIR HC-SR501", "se alimenta con 5 V"],
         ["1", "Buzzer <b>pasivo</b>", "el activo no sirve, ver nota"],
         ["—", "Cables de conexión", ""]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg('lab_2_4')[0], ancha=True, epigrafe= "Circuito de la alarma. El PIR se alimenta con los 5 V de VIN, y el buzzer debe ser pasivo para poder formar la sirena.", capitulo=2))

A(nota("Buzzer pasivo y buzzer activo", p(
    "Un buzzer <b>activo</b> trae su propio oscilador: se lo alimenta y suena, siempre "
    "en la misma nota. Un buzzer <b>pasivo</b> no tiene oscilador y hay que entregarle "
    "la frecuencia desde el pin. Este laboratorio necesita el pasivo, porque la sirena "
    "se construye alternando dos tonos, y eso sólo puede hacerse si el programa "
    "controla la frecuencia. Con un buzzer activo el resultado es un pitido constante.")))

A(aviso("El PIR necesita un minuto", p(
    "Al alimentarlo, el HC-SR501 tarda alrededor de un minuto en estabilizar su "
    "referencia térmica. Durante ese lapso dispara avisos falsos. No es una falla del "
    "montaje ni del programa: hay que alimentarlo, esperar, y recién entonces evaluar "
    "el comportamiento. El sensor trae además dos potenciómetros, de sensibilidad y de "
    "tiempo de retención, que conviene dejar en su posición media al comenzar.")))

A(sec("Razonamiento"))

A(p(
    "La salida del PIR es digital: vale 1 mientras detecta movimiento y 0 el resto del "
    "tiempo. Leerla no tiene ninguna dificultad. El problema de este laboratorio es "
    "otro, y es el primero de una clase que reaparecerá en todo el libro: <b>hacer dos "
    "cosas a la vez</b>.",

    "La sirena exige alternar dos tonos cada doscientos milisegundos. Escrito de la "
    "manera directa, eso son dos esperas dentro de la repetición; y durante esas dos "
    "esperas el programa no está leyendo el sensor. Si el intruso pasa y sale en ese "
    "intervalo, la alarma no se entera. Peor todavía: cuando deja de haber movimiento, "
    "la sirena sigue sonando hasta terminar su espera.",

    "La solución no es acortar las esperas sino sacarlas del programa. En lugar de "
    "«esperar doscientos milisegundos», el programa pregunta en cada vuelta si ya "
    "<b>pasaron</b> doscientos milisegundos desde el último cambio de tono, comparando "
    "el reloj. Así la repetición gira de manera continua, lee el sensor cada vez, y el "
    "tono cambia cuando corresponde.",

    "Es la misma idea que sostiene el filtro de rebote del laboratorio anterior, y la "
    "que permitirá, en el capítulo 7, que un servidor web atienda visitas mientras "
    "sigue midiendo. Conviene retenerla: <b>un programa que espera es un programa que "
    "no vigila</b>."))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import time

buzzer = PWM(Pin(5))
buzzer.duty_u16(0)              # arranca en silencio
pir = Pin(4, Pin.IN)

TONOS = (400, 800)              # Hz, se alternan para formar la sirena
TRAMO_MS = 200
MITAD = 32767                   # media escala de duty_u16

print("Alarma activa. Espere un minuto a que el PIR se estabilice.")

tono = 0
cambio = time.ticks_ms()
sonando = False

while True:
    hay_movimiento = pir.value() == 1
    ahora = time.ticks_ms()

    if hay_movimiento:
        if not sonando:
            print("Movimiento detectado")
            sonando = True
            buzzer.duty_u16(MITAD)

        # se cambia de tono cada tramo, sin detener el programa
        if time.ticks_diff(ahora, cambio) >= TRAMO_MS:
            tono = 1 - tono
            buzzer.freq(TONOS[tono])
            cambio = ahora
    else:
        if sonando:
            print("Sin movimiento")
            sonando = False
            buzzer.duty_u16(0)

    time.sleep_ms(20)""", archivo="lab_2_4_pir_alarma.py"))

A(nota("Las dos banderas", p(
    "<code>sonando</code> recuerda si la sirena ya está activa, y sirve para que los "
    "mensajes se escriban <b>una sola vez</b> en cada cambio y no en cada vuelta de la "
    "repetición, que son cincuenta por segundo. Sin esa bandera, la consola queda "
    "inutilizable. <code>tono</code> guarda cuál de los dos suena, y "
    "<code>1 - tono</code> lo alterna entre 0 y 1 sin necesidad de un "
    "<code>if</code>.")))

A(sec("Qué debe observarse"))
A(p(
    "Pasada la estabilización, al mover la mano frente al sensor la sirena arranca de "
    "inmediato y alterna dos tonos. Al retirarse, calla. La consola escribe una sola "
    "línea por evento. La prueba que vale la pena hacer es pasar rápido frente al "
    "sensor y comprobar que igual detecta: el programa nunca deja de mirar."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Dispara sin que haya nadie",
      "No pasó el minuto de estabilización, o el sensor apunta a una fuente de calor: "
      "una ventana con sol, una lámpara incandescente, una salida de aire."],
     ["El buzzer suena con una sola nota",
      "Es un buzzer activo. Con éste no se puede construir la sirena."],
     ["La sirena sigue un rato después de que el movimiento cesó",
      "No es el programa: es el potenciómetro de tiempo de retención del propio "
      "sensor, que mantiene su salida alta. Girarlo hacia el mínimo."],
     ["No detecta nada",
      "Verificar que el PIR esté alimentado con 5 V (<code>VIN</code>) y no con 3V3. "
      "Con 3,3 V el módulo no trabaja de manera confiable."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, el PIR se reemplaza por una barrera "
    "fotoeléctrica o un detector de presencia en zona peligrosa, y el buzzer por una "
    "baliza sonora o el corte de mando de la máquina. El programa no cambia: lo que "
    "cambia es que la salida, en lugar de hacer ruido, abre un contacto de seguridad.",
    "<b>En el área mecánica</b>, es la alarma perimetral del vehículo. La misma estructura "
    "—sensor de presencia, sirena de dos tonos, vigilancia ininterrumpida— se usa con "
    "el sensor de ocupación del asiento o con el de apertura de puertas.")))

# =================================================================== 2.5
A(lab("2.5", "Una carga que no puede colgar del pin: el relé"))

A(sec("Objetivo"))
A(p("Encender y apagar un foco de 220 V desde la placa, con un pulsador, sin que "
    "la red toque en ningún punto al microcontrolador."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Módulo de relé de 1 canal", "con optoacoplador y puente H/L"],
         ["1", "Fuente de continua", "de la tensión de la bobina: 5 V o 12 V"],
         ["1", "Pulsador", ""],
         ["1", "Portalámparas con foco", "de 220 V, el de menor potencia que haya"],
         ["—", "Cables de conexión", "y cable de red del lado de la carga"]],
        centradas=(0,)))

A(aviso("Antes de tocar nada", p(
    "Este es el único laboratorio del libro donde hay tensión de red, y la tensión de "
    "red mata. Cuatro reglas, y ninguna es negociable:",

    "<b>Nada de la red va a la protoboard.</b> La protoboard no aísla, sus contactos "
    "están a dos milímetros y se sueltan solos. El lado de 220 V se cablea con "
    "conductor de instalación y se ajusta a los tornillos de la bornera del módulo, "
    "que para eso están.",

    "<b>Se arma desenchufado y se prueba enchufado una sola vez.</b> Primero se monta "
    "todo el lado de mando y se comprueba que el relé chasquea; recién con el "
    "chasquido andando se cablea el foco y se enchufa. Cualquier cambio posterior, "
    "desenchufando.",

    "<b>El relé corta la fase, no el neutro.</b> Cortando el neutro la lámpara "
    "también se apaga, pero el portalámparas queda con tensión y quien cambie el foco "
    "se entera a la mala.",

    "<b>Los dos lados no se tocan.</b> Ninguna masa del mando va a la red, ningún "
    "conductor de la red se apoya sobre la placa, y las manos no van a la bornera "
    "mientras esté enchufado. Si en el laboratorio hay un interruptor diferencial, "
    "trabaje aguas abajo de él.")))

A(sec("Razonamiento"))

A(p(
    "El capítulo viene repitiendo que una carga mayor que un indicador no se cuelga "
    "del pin. Ahora toca decir con qué se la reemplaza, y la respuesta es un "
    "<b>relé</b>: un interruptor que en lugar de un dedo tiene un electroimán.",

    "Lo que lo vuelve interesante no es que amplifique —de hecho no amplifica nada— "
    "sino que <b>separa</b>. Adentro hay dos circuitos que no se tocan: una bobina, "
    "que se alimenta con unos pocos miliamperios de continua, y un juego de contactos "
    "capaz de cortar diez amperios de alterna. Entre los dos no hay más que aire y un "
    "resorte. Por eso el pin del ESP32 puede gobernar un motor de 220 V sin enterarse "
    "nunca de que existe.",

    "Los módulos que se consiguen armados agregan una segunda separación, esta vez "
    "electrónica: el <b>optoacoplador</b>, un LED y un fototransistor encerrados en el "
    "mismo encapsulado, que se comunican con luz y no con cobre. Es el rectángulo "
    "negro que se ve junto a la entrada. Con él, entre el pin y la red hay dos "
    "barreras en serie.",

    "El módulo trae además dos cosas que hay que mirar antes de conectar nada, y que "
    "son la causa de la mitad de los desconciertos de este laboratorio: la tensión de "
    "la bobina y el puente de disparo."))

A(nota("La bobina no se alimenta de la placa", p(
    "En el encapsulado azul del relé está impresa la tensión de su bobina: "
    "<code>5 VDC</code> o <code>12 VDC</code>. Es lo primero que hay que leer.",

    "Con una bobina de <b>12 V</b> no hay discusión: hace falta una fuente aparte. "
    "El pin <code>VCC</code> del módulo va al positivo de esa fuente y el "
    "<code>GND</code> del módulo va al negativo <b>y también al GND de la placa</b>, "
    "porque el optoacoplador necesita que las dos referencias sean la misma para "
    "reconocer la orden. Es la misma masa común de siempre, y olvidarla es la falla "
    "número uno: el módulo parece muerto.",

    "Con una bobina de <b>5 V</b> se lo puede alimentar del pin <code>VIN</code>, "
    "pero sólo si el módulo es de un canal. Cada bobina consume entre 70 y 90 mA, y "
    "el regulador de la placa no sostiene dos relés y el WiFi a la vez. Un módulo de "
    "dos o cuatro canales lleva fuente propia siempre.")))

A(nota("El puente H/L, o por qué hay programas que funcionan al revés", p(
    "Al costado de la entrada hay un puente de tres patas rotulado <code>H</code> y "
    "<code>L</code>. Decide con qué nivel dispara el relé: en <code>H</code> se activa "
    "con un <b>1</b> en la entrada, y en <code>L</code> con un <b>0</b>.",

    "De ahí salen los programas de relé que circulan y que parecen contradecirse: uno "
    "escribe <code>relay.value(1)</code> para encender y otro escribe "
    "<code>relay.value(0)</code>. Los dos están bien; lo que cambia es el puente.",

    "Los módulos chinos más comunes vienen de fábrica en <b>L</b>, activo en bajo. "
    "Este libro los usa así, y el programa lo dice en una constante en lugar de "
    "repartir unos y ceros por el código. Si su módulo no tiene puente, mire el LED "
    "del canal: si enciende con la entrada al aire, es activo en bajo.")))

A(sec("El circuito"))

A(figura(CIR.svg('lab_2_5')[0], ancha=True, epigrafe=
    "El lado de mando. Lo único que sale de la placa es la orden: la bobina se "
    "alimenta de su propia fuente, y las tres masas —la de la placa, la del módulo y "
    "la de la fuente— tienen que ser la misma.", capitulo=2))

A(figura(CIR.svg('lab_2_6')[0], ancha=True, epigrafe=
    "El lado de la carga, que es un circuito aparte. La fase entra por COM y sale por "
    "NA, que sólo conduce con el relé activado; el neutro va directo al foco. NC "
    "queda sin usar: es el contacto que conduce con el relé en reposo.", capitulo=2))

A(nota("NA y NC", p(
    "La bornera tiene tres tornillos. <b>COM</b> es el común, el que siempre está "
    "conectado al circuito. <b>NA</b> —normalmente abierto— conduce sólo cuando el "
    "relé está activado, y es el que se usa para encender algo. <b>NC</b> "
    "—normalmente cerrado— hace lo contrario: conduce en reposo y corta al activarse.",
    "La elección no es un detalle de cableado sino de seguridad. Si lo que se gobierna "
    "tiene que <b>quedar apagado</b> cuando el sistema falla o se queda sin "
    "alimentación, va en NA. Si tiene que quedar encendido —una luz de emergencia, un "
    "freno que se suelta— va en NC.")))

A(sec("Programa"))

A(p(
    "El programa es el del pulsador del laboratorio 2.3 con tres cambios. El primero "
    "es la constante que absorbe el puente H/L, para no tener que recordar en cada "
    "línea si el módulo es activo en alto o en bajo. El segundo es el orden de los "
    "estados: <b>el relé arranca apagado y se enciende al presionar</b>, nunca al "
    "revés. El tercero es que aquí el relé sigue al pulsador mientras está "
    "presionado, en lugar de alternar en cada toque.",

    "El filtro de rebote del 2.3 queda igual, y con un relé importa más que con un "
    "LED: cada rebote que se cuela es una maniobra mecánica de más, y las maniobras "
    "de un relé están contadas."))

A(codigo(r'''from machine import Pin
import time

# El puente del modulo decide con que nivel dispara. En L —lo mas
# comun— el rele se activa con un 0. Cambiando esta linea el programa
# sirve para los dos, y no hay que tocar nada mas.
ACTIVO_EN_BAJO = True

REBOTE_MS = 50

rele = Pin(19, Pin.OUT)
boton = Pin(16, Pin.IN, Pin.PULL_UP)

estado = False
ultimo_cambio = time.ticks_ms()


def mandar(encendido):
    """Traduce 'encendido' al nivel que pide este modulo."""
    if ACTIVO_EN_BAJO:
        rele.value(0 if encendido else 1)
    else:
        rele.value(1 if encendido else 0)


mandar(False)          # apagado antes que nada, pase lo que pase

print("Mantenga presionado para encender. Ctrl+C para salir.")

while True:
    # Con PULL_UP el pulsador en reposo lee 1 y presionado lee 0.
    presionado = not boton.value()
    ahora = time.ticks_ms()

    hubo_cambio = presionado != estado
    paso_el_rebote = time.ticks_diff(ahora, ultimo_cambio) > REBOTE_MS

    if hubo_cambio and paso_el_rebote:
        estado = presionado
        ultimo_cambio = ahora
        mandar(estado)
        print("foco encendido" if estado else "foco apagado")

    time.sleep_ms(10)''',
    archivo="lab_2_5_rele.py"))

A(aviso("Por qué el relé no parpadea", p(
    "La versión que aparece primero cuando uno arma este laboratorio es otra: el "
    "pulsador hace parpadear el foco, con dos <code>sleep(0.5)</code>. Funciona, y en "
    "clase se ve bien. Pero hay dos razones para no dejarla.",

    "La primera es mecánica. Medio segundo encendido y medio apagado son dos maniobras "
    "por segundo: <b>7200 por hora</b>. Un relé de estos aguanta del orden de cien mil "
    "maniobras con carga, de modo que el parpadeo se lo come en unas dos semanas de "
    "clase. Y cada cierre sobre un foco incandescente frío es una corriente de "
    "irrupción de unas diez veces la nominal, justo sobre los contactos.",

    "La segunda es de criterio. Escrito con el pulsador en la rama que apaga, el foco "
    "<b>parpadea cuando el pulsador no está</b> —o cuando se corta su cable, que con "
    "<code>PULL_UP</code> es exactamente lo mismo que soltarlo. La falla segura está "
    "al revés: si algo se desconecta, la carga tiene que quedar apagada. Por eso el "
    "programa de arriba enciende al presionar y no al soltar.")))

A(sec("Qué debe observarse"))
A(p(
    "Con el foco todavía sin cablear, al presionar el pulsador se oye el chasquido del "
    "relé y se enciende el LED del canal en el módulo. Ese chasquido es toda la "
    "comprobación del lado de mando: si está, el resto es cableado.",

    "Con el foco conectado, enciende al presionar y apaga al soltar, sin retardo "
    "apreciable. Y la prueba que vale la pena hacer es desconectar el cable del "
    "pulsador con el montaje andando: el foco tiene que quedar <b>apagado</b>."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El relé no chasquea y su LED no enciende",
      "Falta la masa común. El <code>GND</code> del módulo tiene que ir al "
      "<code>GND</code> de la placa <b>y</b> al negativo de la fuente de la bobina."],
     ["El LED del canal enciende pero el relé no chasquea",
      "La bobina no tiene su tensión. Leer qué dice el encapsulado: un relé de 12 V "
      "alimentado con 5 V hace exactamente esto."],
     ["Funciona al revés: apaga al presionar",
      "El puente H/L está en la otra posición. Cambiar "
      "<code>ACTIVO_EN_BAJO</code> en lugar de recablear."],
     ["El relé chasquea pero el foco no enciende",
      "El foco está en NC en lugar de NA, o la fase no llega a COM. Desenchufar "
      "antes de revisar."],
     ["La placa se reinicia cada vez que el relé conmuta",
      "La bobina se está alimentando de la placa y el pico de corriente hunde la "
      "tensión. Fuente aparte."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, es el mando de cualquier arranque: el "
    "relé excita la bobina de un contactor y el contactor mueve el motor. La cadena "
    "pin → relé → contactor → motor es la que separa la lógica de la potencia en "
    "todo tablero, y el programa es el mismo con el pulsador reemplazado por un "
    "sensor de nivel o un térmico.",
    "<b>En el área mecánica</b>, es el relé del vehículo, que está en todos lados: "
    "luces, bomba de combustible, electroventilador, bocina. La llave del tablero no "
    "lleva los treinta amperios del motor del ventilador, lleva la corriente de una "
    "bobina; el relé hace el resto. Cambiar el pulsador por la señal de un sensor de "
    "temperatura es el electroventilador completo.")))

A(ejercicios([
    "En el laboratorio 2.2, agregue una cuarta fase de intermitente nocturno en la que "
    "el amarillo destelle cinco veces antes de reanudar el ciclo. ¿Cuántas líneas hubo "
    "que tocar?",

    "Modifique el semáforo para que un pulsador de peatón, leído como en el "
    "laboratorio 2.3, adelante la fase roja. Tenga en cuenta que el programa no debe "
    "quedarse esperando el pulsador.",

    "En el laboratorio 2.3, haga que una pulsación breve encienda el LED y una "
    "sostenida de más de un segundo lo apague. Ayuda: hace falta recordar el instante "
    "en que se presionó.",

    "En el laboratorio 2.4, cuente cuántas detecciones ocurrieron desde que arrancó el "
    "programa y muéstrelo en la consola en cada evento.",

    "Reescriba el laboratorio 2.4 usando <code>time.sleep(0.2)</code> para alternar los "
    "tonos. Mida cuánto tarda en reaccionar a un movimiento breve y compare con la "
    "versión del libro. Explique la diferencia.",

    "Los tres LED del semáforo consumen unos 4 mA cada uno. Si se quisiera reemplazar "
    "cada uno por una lámpara de 220 V, ¿qué habría que agregar entre el pin y la "
    "lámpara? ¿Cambiaría el programa?",

    "En el laboratorio 2.5, haga que el pulsador funcione como interruptor: una "
    "pulsación enciende y la siguiente apaga, en lugar de encender mientras se "
    "mantiene. Ayuda: hay que detectar el <i>flanco</i>, no el nivel.",

    "Un módulo de relé de cuatro canales con bobinas de 5 V consume unos 80 mA por "
    "canal. ¿Puede alimentarse de <code>VIN</code>? Justifique con el dato del "
    "regulador de la placa, y diga qué pasaría con los cuatro activados.",

    "Explique por qué el laboratorio 2.5 pone el foco en NA y no en NC. ¿En qué caso "
    "elegiría NC, y qué tendría que cambiar en el programa?",
]))
