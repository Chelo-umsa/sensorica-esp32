# -*- coding: utf-8 -*-
"""Capítulo 4 — Señales de pulso."""
from maqueta import (capitulo, lab, sec, codigo, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import circuitos_cap4 as CIR

PARTES = []
A = PARTES.append

A(capitulo(4, "Señales de pulso", p(
    "Hay una familia de sensores que no entrega ni un sí o un no ni una "
    "tensión proporcional: entrega <b>pulsos</b>, y la información está en "
    "cuántos llegan o cada cuánto llegan. Un caudalímetro da un pulso por "
    "cada tanto volumen que pasa; un encoder, uno por cada fracción de "
    "vuelta; un sensor de rueda fónica, uno por cada diente.",

    "La señal es digital —cada pulso es un cambio de nivel como los del "
    "capítulo 2— pero el problema es nuevo, y es de tiempo. Un pulso que se "
    "pierde no se recupera, y el programa tiene que estar mirando en el "
    "instante justo. Los cuatro laboratorios de este capítulo tratan ese "
    "problema, y los tres primeros no necesitan ningún sensor: la placa se "
    "genera los pulsos a sí misma, de modo que se sabe de antemano cuántos "
    "debería haber contado y se puede medir exactamente cuántos se perdió.")))

# =================================================================== 4.1
A(lab("4.1", "Contar sin perder: consulta contra interrupción"))

A(sec("Objetivo"))
A(p("Medir, con números, la diferencia entre revisar un pin cada tanto y "
    "hacer que el pin avise."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["1", "Un cable de conexión. Nada más."]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_4_1")[0], ancha=True, epigrafe=
         "El circuito más corto del libro. GPIO25 genera una señal cuadrada "
         "y GPIO26 la recibe; como la frecuencia es conocida, también se "
         "conoce cuántos pulsos deberían contarse.", capitulo=4))

A(sec("Razonamiento"))

A(p(
    "Hay dos maneras de enterarse de que llegó un pulso.",

    "La <b>consulta</b> es la evidente: en cada vuelta del programa se lee el "
    "pin y se compara con la lectura anterior. Funciona, y es lo que se hizo "
    "en el laboratorio 2.3 con el pulsador. Pero entre dos lecturas el "
    "programa está haciendo otra cosa —calcular, escribir en la consola, "
    "refrescar una pantalla— y si en ese rato la señal sube y vuelve a bajar, "
    "ese pulso <b>no lo contó nadie</b>. No hay error, no hay aviso: "
    "simplemente falta.",

    "La <b>interrupción</b> invierte la relación. Se le dice al "
    "microcontrolador que cuando ese pin baje, ejecute una función "
    "determinada, y él la ejecuta <i>interrumpiendo</i> lo que estuviera "
    "haciendo. No hay manera de perderse un pulso, porque el programa ya no "
    "tiene que estar mirando.",

    "Para un pulsador que se aprieta con el dedo la diferencia no se nota. "
    "Para un caudalímetro a doscientos pulsos por segundo, la consulta pierde "
    "la mayoría."))

A(codigo("""entrada.irq(trigger=Pin.IRQ_FALLING, handler=al_llegar_un_pulso)"""))

A(tabla(
    ["Disparador", "Cuándo se ejecuta"],
    [["<code>Pin.IRQ_FALLING</code>", "Cuando la señal pasa de alto a bajo."],
     ["<code>Pin.IRQ_RISING</code>", "Cuando pasa de bajo a alto."],
     ["<code>Pin.IRQ_RISING | Pin.IRQ_FALLING</code>",
      "En los dos flancos. Cuenta el doble de veces."]]))

A(aviso("Lo que se hace dentro de un manejador, y lo que no", p(
    "Mientras el manejador corre, el programa principal está detenido y "
    "ninguna otra interrupción se atiende. Por eso debe ser <b>lo más corto "
    "posible</b>: sumar uno, anotar un instante, cambiar una bandera. Nada "
    "más.",
    "Dentro de un manejador <b>no</b> van: <code>print</code>, esperas, "
    "cálculos largos, ni nada que reserve memoria —una cadena con "
    "<code>format</code>, por ejemplo—. Reservar memoria dentro de una "
    "interrupción provoca un error que aparece minutos u horas después y es "
    "muy difícil de rastrear. Todo eso se hace en el programa principal, "
    "leyendo lo que el manejador dejó anotado.")))

A(sec("Leer el contador sin perder cuentas"))

A(p(
    "Hay un detalle fino. Si el programa principal hace "
    "<code>pulsos = 0</code> justo después de haber leído el valor, y entre "
    "esas dos instrucciones llega un pulso, ese pulso se pierde: el manejador "
    "lo sumó al valor viejo y el programa lo acaba de borrar.",

    "La solución es apagar las interrupciones durante las dos instrucciones, "
    "que juntas tardan microsegundos:"))

A(codigo("""def tomar_pulsos():
    \"\"\"Lee el contador y lo pone en cero sin perder nada.

    Entre leer y poner en cero podria llegar un pulso, y se
    perderia. Apagar las interrupciones durante esas dos
    instrucciones lo impide; duran microsegundos.
    \"\"\"
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta"""))

A(nota("Por qué se guarda el estado y no se enciende y ya", p(
    "<code>disable_irq()</code> devuelve cómo estaban las interrupciones "
    "antes, y <code>enable_irq()</code> las deja como estaban. Si en lugar de "
    "eso se encendieran sin más, una función llamada desde dentro de otra que "
    "las había apagado las encendería a destiempo. Es una costumbre que "
    "cuesta una variable y evita un problema difícil.")))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import machine
import time

PIN_GENERADOR = 25
PIN_CONTADOR = 26

FRECUENCIA = 200          # pulsos por segundo que se generan
DURACION = 3              # segundos que dura cada medicion
TRABAJO_MS = 5            # lo que el programa tarda en cada vuelta

generador = PWM(Pin(PIN_GENERADOR), freq=FRECUENCIA)
generador.duty(512)       # 50 %: mitad alto, mitad bajo

entrada = Pin(PIN_CONTADOR, Pin.IN)

pulsos = 0


def al_llegar_un_pulso(pin):
    \"\"\"Se ejecuta sola, apenas baja la senal. Solo suma uno.\"\"\"
    global pulsos
    pulsos = pulsos + 1


def tomar_pulsos():
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta


def contar_por_consulta(segundos):
    \"\"\"Revisa el pin una y otra vez, haciendo otra cosa entre medio.

    Ese "otra cosa" es lo que ocurre en cualquier programa real. Si
    en ese rato la senal sube y vuelve a bajar, ese pulso no lo
    cuenta nadie.
    \"\"\"
    cuenta = 0
    anterior = entrada.value()
    limite = time.ticks_add(time.ticks_ms(), segundos * 1000)

    while time.ticks_diff(limite, time.ticks_ms()) > 0:
        actual = entrada.value()
        if anterior == 1 and actual == 0:
            cuenta = cuenta + 1
        anterior = actual
        time.sleep_ms(TRABAJO_MS)      # el programa hace otra cosa

    return cuenta


def contar_por_interrupcion(segundos):
    \"\"\"Deja que el pin avise, perdiendo el mismo tiempo que antes.\"\"\"
    entrada.irq(trigger=Pin.IRQ_FALLING, handler=al_llegar_un_pulso)
    tomar_pulsos()                      # descarta lo acumulado

    limite = time.ticks_add(time.ticks_ms(), segundos * 1000)
    while time.ticks_diff(limite, time.ticks_ms()) > 0:
        time.sleep_ms(TRABAJO_MS)      # exactamente el mismo trabajo

    entrada.irq(handler=None)
    return tomar_pulsos()


def main():
    esperados = FRECUENCIA * DURACION
    print("Se generan {} pulsos por segundo durante {} s.".format(
        FRECUENCIA, DURACION))
    print("Deberian contarse {} pulsos.".format(esperados))
    print("")

    por_consulta = contar_por_consulta(DURACION)
    por_interrupcion = contar_por_interrupcion(DURACION)

    print("  metodo          contados   perdidos")
    for nombre, cuenta in (("consulta", por_consulta),
                           ("interrupcion", por_interrupcion)):
        perdidos = esperados - cuenta
        print("  {:<14}  {:6d}   {:5d}  ({:4.1f} %)".format(
            nombre, cuenta, perdidos, perdidos * 100.0 / esperados))


if __name__ == "__main__":
    main()""", archivo="lab_4_1_consulta_interrupcion.py"))

A(sec("Qué debe observarse"))

A(consola("""Se generan 200 pulsos por segundo durante 3 s.
Deberian contarse 600 pulsos.

  metodo          contados   perdidos
  consulta            120      480  (80.0 %)
  interrupcion        600        0  ( 0.0 %)"""))

A(p(
    "Las cifras exactas dependen de la placa, pero el orden de magnitud es "
    "ése: con el programa ocupado cinco milisegundos por vuelta y pulsos cada "
    "cinco milisegundos, la consulta pierde la mayoría y la interrupción no "
    "pierde ninguno.",

    "Conviene repetir la prueba bajando <code>FRECUENCIA</code> a 10 y "
    "subiéndola a 1000. A diez pulsos por segundo los dos métodos aciertan; "
    "a mil, la consulta es inservible. <b>Ese es el criterio para elegir</b>, "
    "y el ejercicio 1 pide encontrar el punto donde deja de servir."))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, esto decide si un contador de "
    "producción es confiable. Una fotocélula que cuenta piezas en una cinta "
    "rápida, leída por consulta, cuenta de menos y nadie se entera hasta que "
    "los números no cierran con el inventario.",
    "<b>En el área mecánica</b>, la señal del sensor de cigüeñal a 6000 rpm con una "
    "rueda de 60 dientes da 6000 pulsos por segundo. Ahí la consulta no es "
    "una alternativa peor: es imposible.")))

# =================================================================== 4.2
A(lab("4.2", "Frecuencímetro por conteo"))

A(sec("Objetivo"))
A(p("Medir la frecuencia contando cuántos pulsos llegan en un tiempo fijo, y "
    "encontrar el límite del método."))

A(sec("El circuito"))
A(p("El mismo del laboratorio 4.1: un puente entre GPIO25 y GPIO26."))

A(sec("Razonamiento"))

A(p(
    "Si se cuentan los pulsos que llegan en exactamente un segundo, ese "
    "número <b>es</b> la frecuencia en hercios. No hay cálculo. Es el método "
    "que usan casi todos los tacómetros y caudalímetros, y su virtud es que "
    "no se puede equivocar en la aritmética.",

    "Su defecto aparece abajo. La cuenta es siempre un número entero: o "
    "llegaron nueve pulsos o llegaron diez. A 1000 Hz, equivocarse en uno es "
    "un error del 0,1 %; a 10 Hz, el mismo pulso de diferencia es un error "
    "del <b>10 %</b>. El método es exacto arriba y grosero abajo, y el "
    "laboratorio siguiente resuelve justamente eso."))

A(tabla(
    ["Frecuencia", "Pulsos en 1 s", "Error de ±1 pulso"],
    [["10 Hz", "10", "<b>± 10 %</b>"],
     ["50 Hz", "50", "± 2 %"],
     ["200 Hz", "200", "± 0,5 %"],
     ["1000 Hz", "1000", "± 0,1 %"],
     ["5000 Hz", "5000", "± 0,02 %"]],
    centradas=(0, 1, 2)))

A(nota("La ventana y la resolución van de la mano", p(
    "Con una ventana de un segundo, la resolución es de 1 Hz. Con media "
    "ventana, la medición llega el doble de rápido pero la resolución cae a "
    "2 Hz. Con dos segundos, mejora a 0,5 Hz pero hay que esperar el doble.",
    "No hay manera de tener las dos cosas con este método: es la limitación "
    "de fondo, y por eso existe el otro.")))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import machine
import time

PIN_GENERADOR = 25
PIN_CONTADOR = 26

VENTANA_MS = 1000         # duracion de cada medicion
FRECUENCIAS = (10, 50, 200, 1000, 5000)

generador = PWM(Pin(PIN_GENERADOR), freq=FRECUENCIAS[0])
generador.duty(512)

entrada = Pin(PIN_CONTADOR, Pin.IN)

pulsos = 0


def contar(pin):
    global pulsos
    pulsos = pulsos + 1


def tomar_pulsos():
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta


def medir_frecuencia(ventana_ms=VENTANA_MS):
    \"\"\"Cuenta los pulsos de una ventana y los pasa a hercios.\"\"\"
    tomar_pulsos()                      # arranca de cero
    time.sleep_ms(ventana_ms)
    return tomar_pulsos() * 1000.0 / ventana_ms


def main():
    entrada.irq(trigger=Pin.IRQ_FALLING, handler=contar)
    print("Frecuencimetro por conteo, ventana de {} ms".format(
        VENTANA_MS))
    print("")
    print("  generada   medida    error")

    for f in FRECUENCIAS:
        generador.freq(f)
        time.sleep_ms(200)              # deja que se asiente
        medida = medir_frecuencia()
        error = (medida - f) * 100.0 / f
        print("  {:6d} Hz  {:7.1f} Hz  {:+5.1f} %".format(
            f, medida, error))

    resolucion = 1000.0 / VENTANA_MS
    print("")
    print("Con {} ms de ventana no se baja de {:.1f} Hz.".format(
        VENTANA_MS, resolucion))
    print("Por eso el error relativo es grande abajo y chico arriba.")


if __name__ == "__main__":
    main()""", archivo="lab_4_2_frecuencimetro.py"))

A(sec("Qué debe observarse"))
A(p(
    "Las cinco frecuencias se miden con error decreciente. La columna de "
    "error es la lección del laboratorio: en 10 Hz ronda el 10 % y en 5000 Hz "
    "es despreciable. Vale la pena repetirlo con "
    "<code>VENTANA_MS = 100</code> y ver que todos los errores se multiplican "
    "por diez."))

# =================================================================== 4.3
A(lab("4.3", "Medición por período"))

A(sec("Objetivo"))
A(p("Medir bien las frecuencias bajas, que es donde el conteo falla."))

A(sec("El circuito"))
A(p("El mismo puente entre GPIO25 y GPIO26."))

A(sec("Razonamiento"))

A(p(
    "En vez de contar cuántos pulsos entran en un tiempo fijo, se mide "
    "<b>cuánto tarda un pulso</b> y se invierte: si entre dos flancos pasaron "
    "100 000 microsegundos, la frecuencia es 10 Hz.",

    "La ventaja es inmediata. El reloj de microsegundos del ESP32 tiene mucha "
    "más resolución que el conteo de pulsos enteros, de modo que a frecuencias "
    "bajas la medición es muy precisa. Y no hay que esperar una ventana "
    "completa: con un solo período ya hay resultado.",

    "La desventaja es la simétrica. A frecuencias altas los períodos son tan "
    "cortos que el propio tiempo de atención de la interrupción —unos pocos "
    "microsegundos— pesa sobre la medida, y el resultado empieza a bailar. "
    "Por eso se promedian varios períodos."))

A(tabla(
    ["Método", "Va bien en", "Va mal en"],
    [["<b>Conteo</b> (4.2)", "frecuencias altas",
      "frecuencias bajas: ±1 pulso pesa mucho"],
     ["<b>Período</b> (4.3)", "frecuencias bajas",
      "frecuencias altas: el período se acerca al tiempo de atención"]]))

A(p("Un instrumento serio usa los dos y cambia de método según el rango. El "
    "ejercicio 4 propone escribirlo."))

A(aviso("ticks_diff, siempre", p(
    "El contador de microsegundos no crece indefinidamente: llega a un máximo "
    "y vuelve a cero. Restando dos lecturas con el signo menos, si el vuelco "
    "cae entre ambas, el resultado es un número negativo enorme y la "
    "frecuencia sale disparatada.",
    "Con <code>ticks_us()</code> el vuelco ocurre aproximadamente cada 18 "
    "minutos. Un instrumento que anda bien y de golpe marca un valor absurdo, "
    "más o menos cada cuarto de hora, casi siempre es esto.")))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import time

PIN_GENERADOR = 25
PIN_CONTADOR = 26

MUESTRAS = 16             # periodos que se promedian
FRECUENCIAS = (2, 10, 50, 200, 1000)

generador = PWM(Pin(PIN_GENERADOR), freq=FRECUENCIAS[0])
generador.duty(512)

entrada = Pin(PIN_CONTADOR, Pin.IN)

ultimo_us = 0
periodo_us = 0


def al_llegar_un_pulso(pin):
    \"\"\"Anota cuanto paso desde el pulso anterior.

    Se usa ticks_diff y no una resta comun porque el contador de
    microsegundos se da vuelta: una resta directa daria, en ese
    momento, un valor negativo enorme.
    \"\"\"
    global ultimo_us, periodo_us
    ahora = time.ticks_us()
    if ultimo_us != 0:
        periodo_us = time.ticks_diff(ahora, ultimo_us)
    ultimo_us = ahora


def medir_frecuencia(muestras=MUESTRAS, espera_ms=600):
    \"\"\"Promedia varios periodos. None si no llego ningun pulso.\"\"\"
    global periodo_us
    suma = 0
    tomadas = 0
    limite = time.ticks_add(time.ticks_ms(), espera_ms)

    while tomadas < muestras and \\
            time.ticks_diff(limite, time.ticks_ms()) > 0:
        if periodo_us > 0:
            suma = suma + periodo_us
            periodo_us = 0
            tomadas = tomadas + 1
        time.sleep_ms(1)

    if tomadas == 0:
        return None
    return 1000000.0 / (suma / tomadas)


def main():
    entrada.irq(trigger=Pin.IRQ_FALLING, handler=al_llegar_un_pulso)
    print("Medicion por periodo, promediando {} pulsos".format(
        MUESTRAS))
    print("")
    print("  generada   medida    error")

    for f in FRECUENCIAS:
        generador.freq(f)
        time.sleep_ms(300)
        medida = medir_frecuencia()

        if medida is None:
            print("  {:6d} Hz  sin pulsos".format(f))
        else:
            error = (medida - f) * 100.0 / f
            print("  {:6d} Hz  {:7.1f} Hz  {:+5.1f} %".format(
                f, medida, error))

    print("")
    print("Este metodo mide bien abajo, donde el conteo se equivocaba.")


if __name__ == "__main__":
    main()""", archivo="lab_4_3_periodo.py"))

A(sec("Qué debe observarse"))
A(p(
    "A 2 Hz y a 10 Hz el error es de décimas de por ciento, contra el 10 % "
    "que daba el conteo. A 1000 Hz empieza a notarse ruido. Comparar las dos "
    "tablas —la del 4.2 y la de éste— es el ejercicio más útil del capítulo: "
    "cada método es bueno exactamente donde el otro falla."))

# =================================================================== 4.4
A(lab("4.4", "Tacómetro: del pulso a las revoluciones"))

A(sec("Objetivo"))
A(p("Medir las revoluciones de un motor real, con todo lo que eso trae que "
    "no aparecía con la señal limpia del generador."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Sensor óptico de ranura", "con su comparador, el del disco"],
         ["1", "Disco con marcas", "el de este laboratorio tiene <b>4</b>"],
         ["1", "Módulo L298N", "puente H, para gobernar el motor"],
         ["1", "Motor de corriente continua", "con su fuente"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_4_4")[0], ancha=True, epigrafe=
         "El sensor óptico ve pasar las marcas del disco montado en el eje. "
         "El L298N gobierna el motor y el ESP32 le manda el PWM por ENA.",
         capitulo=4))

A(aviso("Las dos masas tienen que estar unidas", p(
    "El motor se alimenta de su propia fuente por los bornes del L298N, y el "
    "ESP32 del USB. Son dos fuentes distintas, y si sus masas no se unen, las "
    "señales de mando no tienen referencia común: el puente H hace cualquier "
    "cosa o no hace nada.",
    "Unir <b>sólo las masas</b>. No unir los positivos.")))

A(sec("Razonamiento"))

A(p(
    "La cuenta es directa. Si el disco tiene <i>m</i> marcas, cada vuelta "
    "produce <i>m</i> pulsos, de modo que:"))

A(codigo("""RPM = (pulsos / marcas_por_vuelta) * 60000 / ventana_ms"""))

A(p(
    "Con cuatro marcas y una ventana de un segundo, 40 pulsos son 600 RPM. "
    "Si el disco tuviera una sola marca serían 2400. <b>Equivocarse en el "
    "número de marcas multiplica o divide el resultado</b>, y es el error más "
    "común de este laboratorio: el programa no tiene manera de darse cuenta.",

    "Lo que aparece aquí y no aparecía antes es que la señal ya no es limpia. "
    "El comparador del módulo óptico no conmuta de una vez: en cada flanco "
    "puede dar varios cambios en pocos microsegundos. Sin filtro, las "
    "revoluciones salen infladas, a veces al doble.",

    "El filtro es el mismo del pulsador del laboratorio 2.3, con dos "
    "diferencias. Se mide en <b>microsegundos</b>, porque aquí los pulsos "
    "buenos están mucho más cerca; y el umbral hay que elegirlo con cuidado, "
    "porque si se pasa empieza a descartar pulsos legítimos a alta velocidad."))

A(nota("Cómo elegir el tiempo de rebote", p(
    "Tiene que ser mayor que el rebote y menor que el intervalo entre dos "
    "pulsos buenos a la máxima velocidad prevista. Con 4 marcas a 3000 RPM "
    "hay 200 pulsos por segundo, o sea uno cada 5000 µs; un filtro de 1500 µs "
    "deja margen de sobra. Si el motor llegara a 12 000 RPM el intervalo "
    "bajaría a 1250 µs y ese filtro empezaría a comerse pulsos: el tacómetro "
    "marcaría de menos justamente a fondo.")))

A(sec("Programa"))

A(codigo("""from machine import Pin, PWM
import machine
import time

PIN_SENSOR = 17
MARCAS_POR_VUELTA = 4     # las que tenga SU disco. Ver el razonamiento.

ENA = PWM(Pin(19), freq=1000)
IN1 = Pin(18, Pin.OUT)
IN2 = Pin(5, Pin.OUT)
IN1.on()
IN2.off()                 # sentido de giro fijo
ENA.duty(0)

sensor = Pin(PIN_SENSOR, Pin.IN)

VENTANA_MS = 1000
REBOTE_US = 1500          # descarta los rebotes del comparador

pulsos = 0
_ultimo_us = 0


def contar(pin):
    \"\"\"Suma un pulso, descartando los rebotes del comparador.\"\"\"
    global pulsos, _ultimo_us
    ahora = time.ticks_us()
    if time.ticks_diff(ahora, _ultimo_us) > REBOTE_US:
        pulsos = pulsos + 1
        _ultimo_us = ahora


def tomar_pulsos():
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta


def rpm_desde_pulsos(cuenta, ventana_ms):
    \"\"\"Pasa una cuenta de pulsos a revoluciones por minuto.\"\"\"
    vueltas = cuenta / MARCAS_POR_VUELTA
    return vueltas * 60000.0 / ventana_ms


def main():
    sensor.irq(trigger=Pin.IRQ_FALLING, handler=contar)
    print("Tacometro. Disco de {} marcas.".format(MARCAS_POR_VUELTA))
    print("")
    print("  velocidad   pulsos      RPM")

    for porcentaje in (40, 60, 80, 100, 0):
        ENA.duty(int(porcentaje * 1023 / 100))
        time.sleep_ms(600)              # deja que el motor se acomode
        tomar_pulsos()                  # descarta lo del transitorio

        time.sleep_ms(VENTANA_MS)
        cuenta = tomar_pulsos()

        print("   {:3d} %      {:4d}    {:7.0f}".format(
            porcentaje, cuenta, rpm_desde_pulsos(cuenta, VENTANA_MS)))

    ENA.duty(0)
    sensor.irq(handler=None)
    print("")
    print("Motor detenido.")


if __name__ == "__main__":
    main()""", archivo="lab_4_4_tacometro.py"))

A(sec("Qué debe observarse"))
A(p(
    "Las revoluciones crecen con el porcentaje, pero <b>no en proporción</b>: "
    "por debajo de cierto valor el motor ni arranca, y arriba la curva se "
    "aplana. Un motor de corriente continua no es lineal contra el ciclo de "
    "trabajo, y conviene verlo antes de suponer lo contrario.",

    "Conviene comprobar la cifra con un tacómetro óptico de mano, o "
    "marcando el eje y contando a ojo a baja velocidad. Si el resultado sale "
    "justo al doble o a la mitad, el número de marcas está mal."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Las RPM salen al doble",
      "El disco tiene el doble de marcas de las declaradas, o el disparador "
      "está en los dos flancos."],
     ["Salen infladas y erráticas",
      "Falta el filtro de rebote, o <code>REBOTE_US</code> es demasiado "
      "corto."],
     ["Marca de menos a alta velocidad",
      "<code>REBOTE_US</code> es demasiado largo y descarta pulsos buenos."],
     ["Cuenta con el motor detenido",
      "Ruido eléctrico del motor acoplado al cable del sensor. Separarlo del "
      "cableado de potencia, y unir las masas en un solo punto."],
     ["El motor no arranca",
      "Las masas no están unidas, o el ciclo de trabajo es menor que el "
      "mínimo que ese motor necesita para vencer su propio rozamiento."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el control de velocidad de "
    "una bomba o una cinta con realimentación: se mide la velocidad real y se "
    "corrige el mando hasta alcanzar la consigna. Con el encoder de un motor "
    "cambian las marcas por vuelta —suelen ser cientos— y nada más.",
    "<b>En el área mecánica</b>, es el sensor de régimen del motor. La rueda fónica "
    "del cigüeñal tiene típicamente 60 dientes menos 2, y esos dos que faltan "
    "son los que marcan la posición. El algoritmo de conteo es éste; lo que "
    "se agrega es detectar el hueco.")))

A(ejercicios([
    "En el laboratorio 4.1, encuentre bajando la frecuencia el punto en que "
    "la consulta deja de perder pulsos. Relacione ese valor con "
    "<code>TRABAJO_MS</code>.",

    "Cambie el disparador del 4.1 a los dos flancos. ¿Cuántos pulsos cuenta "
    "ahora? ¿Qué habría que cambiar para que la frecuencia siga saliendo "
    "bien?",

    "Con la tabla del 4.2 y la del 4.3, dibuje el error de los dos métodos "
    "contra la frecuencia. ¿En qué valor se cruzan las dos curvas?",

    "Escriba una función que elija sola el método: período por debajo de la "
    "frecuencia de cruce y conteo por encima.",

    "Un caudalímetro da 450 pulsos por litro. Escriba el programa que muestre "
    "el caudal en litros por minuto y el total acumulado.",

    "En el 4.4, calcule qué valor de <code>REBOTE_US</code> empezaría a "
    "comerse pulsos si el motor llegara a 9000 RPM con el disco de 4 marcas.",

    "El tacómetro con ventana de un segundo tarda un segundo en enterarse de "
    "un cambio. ¿Cómo lo haría más rápido sin perder resolución? Ayuda: mire "
    "el laboratorio 4.3.",
]))
