# -*- coding: utf-8 -*-
"""Capítulo 1 — El ESP32 y MicroPython."""
from maqueta import (capitulo, lab, sec, codigo, circuito, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import figuras_cap1 as FIG

PARTES = []
A = PARTES.append

A(capitulo(1, "El ESP32 y MicroPython", p(
    "Un sensor, por sí solo, no informa nada. Entrega una tensión, un tren de pulsos "
    "o una trama de bits, y hace falta algo que lo interrogue, interprete lo que "
    "devuelve y lo convierta en una magnitud con unidades. Ese trabajo lo hace el "
    "microcontrolador, y a lo largo de este libro lo hará siempre el mismo: una placa "
    "ESP32 programada en MicroPython.",

    "Este capítulo prepara la mesa de trabajo. No hay todavía ningún sensor conectado: "
    "se trata de conocer la placa, saber qué pin se puede usar y cuál no, dejar "
    "MicroPython instalado y escribir el primer programa. Es el único capítulo del "
    "libro que puede leerse sin tener nada en la mano, y conviene no saltearlo, porque "
    "buena parte de los tropiezos que aparecen más adelante —una lectura que no varía, "
    "una placa que no arranca, un sensor que mide de menos— se explican por algo que "
    "está dicho en estas páginas.")))

# =================================================================== 1.1
A(lab("1.1", "La placa y sus pines"))

A(p(
    "El ESP32 es un microcontrolador de 32 bits con WiFi y Bluetooth integrados. Para "
    "lo que interesa en este libro, sus características relevantes son cuatro: trabaja "
    "a <b>3,3 V</b>, tiene un convertidor analógico-digital de <b>12 bits</b>, maneja "
    "todos los protocolos de comunicación que usan los sensores habituales (I²C, SPI, "
    "UART) y puede conectarse a una red sin hardware adicional. Esa última capacidad es "
    "la que permite que el mismo montaje que mide sobre la mesa termine publicando "
    "en internet, que es el recorrido completo del libro.",

    "Las placas de desarrollo más difundidas son la <b>ESP32 DevKit V1</b> y sus "
    "equivalentes de 30 o 38 pines. Todas exponen el mismo chip, y las diferencias "
    "están en cuántos pines dejan accesibles. Los laboratorios de este libro se "
    "escribieron sobre una DevKit V1 de 30 pines."))

A(nota("Dos alimentaciones que no son intercambiables", p(
    "La placa tiene un pin <code>3V3</code> y un pin <code>VIN</code>. El primero "
    "entrega los 3,3 V con que trabaja el propio microcontrolador; el segundo devuelve "
    "los 5 V que entran por el conector USB. Muchos sensores funcionan con cualquiera "
    "de los dos, pero algunos no: el LM35 del capítulo 3 necesita al menos 4 V y "
    "alimentado con 3,3 V mide de menos sin dar ningún síntoma de falla. Cada "
    "laboratorio indica de cuál de los dos pines debe colgarse el sensor, y esa "
    "indicación no es intercambiable.")))

A(nota("Masa, tierra y ground no son la misma cosa", p(
    "En el taller las tres palabras se usan como sinónimos, y a la hora de conectar "
    "un cable da igual cuál se diga. Este libro dice <b>masa</b> siempre, y conviene "
    "saber por qué, porque llega un momento —en instalaciones, en protecciones— en "
    "que la diferencia deja de ser un capricho de vocabulario.",

    "La <b>masa</b> es el punto de 0 V que todo el montaje toma como referencia. "
    "Medir una tensión es medir una diferencia, de modo que sin una referencia común "
    "no hay nada que medir: por eso el sensor y la placa tienen que compartir ese "
    "cable aunque cada uno tenga su propia fuente, y por eso la mitad de las fallas "
    "de un montaje que «lee cualquier cosa» son una masa que quedó suelta. En la "
    "placa es el pin <code>GND</code>, y hay varios porque hacen falta varios.",

    "La <b>tierra</b> de una instalación es otra cosa. Es el conductor que llega al "
    "electrodo enterrado, y su trabajo no es servir de referencia sino desviar una "
    "corriente de falla para que no pase por una persona. En funcionamiento normal no "
    "conduce nada, y no es donde se conecta un sensor.",

    "Las dos áreas lo muestran bien. En un vehículo la masa es el <b>chasis</b>, "
    "unido al borne negativo de la batería, y no hay ninguna tierra: el auto está "
    "parado sobre cuatro ruedas de caucho. En un tablero industrial conviven las dos "
    "y son bornes distintos, con colores distintos y funciones que no se reemplazan. "
    "De ahí la decisión del libro: <i>tierra</i> queda reservada para la instalación "
    "y <i>masa</i> nombra el 0 V de los montajes.",

    "En los diagramas el pin va rotulado <code>GND</code>, que es lo que dice la "
    "serigrafía de la placa y lo que el estudiante va a leer con el montaje en la "
    "mano.")))

A(sec("Qué pin se puede usar"))

A(figura(FIG.plano_placa(), ancha=True, epigrafe=
         "La placa vista desde arriba, con el conector USB abajo. El rótulo de "
         "color da el número de GPIO, que es el que usa el programa; a su lado, "
         "en gris, lo que dice la serigrafía cuando no coinciden.", capitulo=1))

A(nota("Ésta es la placa de 30 pines, y hay otra de 38", p(
    "Todas las figuras de este libro muestran la <b>DevKit de 30 pines</b>: quince "
    "agujeros por lado. Es la más difundida y la más barata, y es la que se toma como "
    "referencia de aquí en adelante.",

    "En el mercado también se consigue una versión de <b>38 pines</b>, con diecinueve "
    "por lado. Es más larga, saca al conector los pines de la memoria flash —los "
    "GPIO 6 a 11, que igual no se pueden usar— y, sobre todo, <b>lleva los pines en "
    "otro orden</b>. El microcontrolador es el mismo y los programas de este libro "
    "corren idénticos en las dos; lo que no coincide es el dibujo.",

    "De ahí una recomendación que vale para todo el libro: <b>conecte leyendo el "
    "nombre del pin, nunca contando posiciones desde la esquina</b>. Contar funciona "
    "mientras la placa sea la del dibujo, y falla en silencio apenas alguien trae la "
    "otra. Para saber cuál tiene, cuente los agujeros de un lado: quince es ésta, "
    "diecinueve es la de 38.")))

A(p(
    "No todos los pines del ESP32 sirven para todo. Algunas están comprometidas con la "
    "memoria interna, otras sólo leen, y otras se consultan durante el arranque y "
    "cambian el comportamiento de la placa según el nivel que encuentren. Conviene "
    "tener presente esta tabla desde el principio, porque explica una cantidad "
    "desproporcionada de fallas."))

A(tabla(
    ["Pines", "Se pueden usar", "Advertencia"],
    [["<b>GPIO 6 – 11</b>", "<b>No</b>",
      "Están conectados a la memoria flash del propio módulo. Usarlos impide que la "
      "placa arranque. En muchas placas ni siquiera están expuestos."],
     ["<b>GPIO 34, 35, 36, 39</b>", "Sólo como entrada",
      "No tienen resistencias internas de elevación ni de descenso, y no pueden "
      "configurarse como salida. Son excelentes entradas analógicas."],
     ["<b>GPIO 0, 2, 12, 15</b>", "Sí, con cuidado",
      "Se leen durante el arranque. Si tienen algo conectado que fuerce un nivel, la "
      "placa puede quedarse sin arrancar o entrar en modo de carga de firmware."],
     ["<b>GPIO 1, 3</b>", "Sí, con cuidado",
      "Son el puerto serie que usa el USB. Al utilizarlos se pierde la consola de "
      "Thonny."],
     ["Los demás", "Sí", "Entrada o salida, sin restricciones particulares."]],
    centradas=(1,)))

A(aviso("El error de los dos convertidores analógicos", p(
    "El ESP32 tiene dos convertidores. El <b>ADC1</b> ocupa los pines <b>GPIO 32 a "
    "39</b>; el <b>ADC2</b>, los GPIO 0, 2, 4, 12 a 15 y 25 a 27. La diferencia es "
    "decisiva: <b>el ADC2 deja de funcionar cuando el WiFi está encendido</b>, porque "
    "la radio lo usa internamente.",
    "En la práctica esto significa que un montaje que mide bien sobre la mesa deja de "
    "medir en cuanto se le agrega la conexión a la red, y el síntoma es un valor "
    "congelado o un error difícil de interpretar. Por eso, en todo este libro, "
    "<b>cualquier sensor analógico va a un pin del ADC1</b>, esté o no previsto "
    "conectarlo a internet. Es una disciplina barata que evita rehacer el cableado "
    "al llegar al capítulo 7.")))

A(sec("Cuánta corriente puede entregar un pin"))

A(p(
    "Una salida del ESP32 puede entregar unos 12 mA con comodidad, y no debería "
    "pedírsele más de 40 mA en ningún caso. Alcanza de sobra para un LED con su "
    "resistencia, pero no para un relé, un motor ni una tira de LED. Todo lo que "
    "consuma más que un indicador luminoso se maneja con un transistor, un módulo de "
    "relé o un controlador, nunca colgado directamente del pin. Es la diferencia entre "
    "un montaje que dura el semestre y uno que se lleva la placa puesta."))

# =================================================================== 1.2
A(lab("1.2", "Instalar MicroPython y Thonny"))

A(p(
    "MicroPython es una implementación reducida de Python pensada para "
    "microcontroladores. Se graba una sola vez en la placa y a partir de ahí la placa "
    "«habla» Python: se le pueden mandar instrucciones sueltas y ver la respuesta en el "
    "momento, sin compilar ni cargar nada. Esa inmediatez es la razón principal para "
    "elegirlo frente a C en un curso.",

    "El entorno que se usará es <b>Thonny</b>, gratuito y disponible para Windows, "
    "Linux y macOS."))

A(sec("Procedimiento"))

A(p(
    "<b>1. Instalar Thonny.</b> Descargarlo de <code>thonny.org</code> y ejecutar el "
    "instalador. No requiere ninguna opción especial.",

    "<b>2. Descargar el firmware.</b> En <code>micropython.org/download/</code>, "
    "buscar la placa ESP32 genérica y bajar el archivo <code>.bin</code> más reciente.",

    "<b>3. Instalar el controlador del puerto.</b> La placa no se comunica por USB "
    "por su cuenta: lleva un segundo integrado que traduce entre el USB del "
    "computador y el puerto serie del ESP32, y Windows necesita su controlador para "
    "verlo. Es el paso que más veces falla en la primera clase y el que decide todo "
    "lo que viene después; el apartado siguiente explica cuál corresponde.",

    "<b>4. Conectar la placa</b> al computador con un cable USB. Debe ser un cable de "
    "datos: los cables de sólo carga, muy comunes, no establecen comunicación y la "
    "placa no aparece en ningún puerto.",

    "<b>5. Grabar el firmware.</b> En Thonny, ir a <i>Herramientas → Opciones → "
    "Intérprete</i>, elegir <i>MicroPython (ESP32)</i> y el puerto COM correspondiente, "
    "y pulsar <i>Instalar o actualizar firmware</i>. Seleccionar el archivo descargado "
    "y confirmar. El proceso tarda menos de un minuto.",

    "<b>6. Comprobar.</b> De vuelta en la ventana principal, el panel inferior "
    "—la <i>Shell</i>— debe mostrar el indicador de MicroPython:"))

A(consola(""">>> print("hola")
hola
>>> import machine
>>> machine.freq()
160000000"""))

A(p(
    "Si esas tres líneas responden, la placa está lista y no hay que volver a grabar "
    "el firmware nunca más."))

A(sec("Cuál controlador, y por qué no es siempre el mismo"))

A(p(
    "El ESP32 no habla USB. Junto al conector hay un segundo integrado, el "
    "<b>conversor USB-serie</b>, que traduce entre el cable y el puerto serie del "
    "microcontrolador. Ese chip es el que el computador ve, y ése es el que necesita "
    "controlador.",

    "El problema es que no todas las placas llevan el mismo. Dos placas que se ven "
    "iguales, compradas el mismo día, pueden traer conversores de fabricantes "
    "distintos, y el controlador de una no le sirve a la otra. De ahí que en la "
    "primera clase medio curso esté trabajando y la otra mitad no vea ningún puerto, "
    "con el mismo instalador ejecutado.",

    "Hay dos maneras de saber cuál toca. Con la placa en la mano, leer la inscripción "
    "del integrado cuadrado que está al lado del conector USB. Con la placa "
    "conectada, abrir el <b>Administrador de dispositivos</b> de Windows y mirar qué "
    "nombre aparece —o qué dispositivo aparece con un signo de admiración, que es "
    "justamente el que se quedó sin controlador."))

A(tabla(
    ["Dice el integrado", "Windows lo llama", "Controlador que corresponde"],
    [["<code>CP2102</code>, <code>CP2102N</code>",
      "<code>Silicon Labs CP210x USB to UART Bridge</code>",
      "El <i>VCP</i> de <b>Silicon Labs</b>, en su página de <i>CP210x USB to UART "
      "Bridge VCP Drivers</i>."],
     ["<code>CH340</code>, <code>CH340C</code>, <code>CH9102</code>",
      "<code>USB-SERIAL CH340</code> o <code>USB Enhanced SERIAL</code>",
      "El <i>VCP</i> de <b>WCH</b>, que en su sitio figura como <i>CH341SER</i>."]]))

A(p(
    "Los dos son gratuitos y no piden registro. En Linux no hace falta ninguno —el "
    "núcleo ya los trae— y en las versiones recientes de macOS tampoco. Y en Windows "
    "11 al día, el de Silicon Labs suele instalarse solo por Windows Update apenas se "
    "conecta la placa: por eso hay estudiantes a los que nunca les falló, y conviene "
    "saberlo antes de que expliquen que ellos no hicieron nada distinto."))

A(aviso("El controlador va en el computador, no en la placa", p(
    "Instalarlo no le graba nada al ESP32, no le borra el programa y no tiene relación "
    "con el firmware de MicroPython. Es un archivo que se instala en Windows para que "
    "reconozca un chip.",
    "Vale la pena decirlo en voz alta porque el reflejo, cuando una placa no aparece, "
    "es volver a grabarle el firmware. No puede funcionar: para grabar el firmware "
    "hace falta el puerto, que es exactamente lo que falta. Y una placa que no aparece "
    "casi nunca está dañada —lo que falta está del lado del computador.")))

A(sec("Cuando la placa sigue sin aparecer"))

A(tabla(
    ["Síntoma", "Causa habitual"],
    [["No hay ningún puerto COM en la lista",
      "Falta el controlador del conversor USB-serie, o se instaló el del otro "
      "fabricante. Ver el apartado anterior."],
     ["Aparece un dispositivo con signo de admiración",
      "El controlador está, pero no es el de ese chip. Desinstalarlo desde el "
      "Administrador de dispositivos e instalar el que corresponda."],
     ["El controlador está bien y aun así no hay puerto",
      "El cable. Los de sólo carga no llevan las líneas de datos y no hay manera de "
      "distinguirlos por fuera; la prueba es cambiarlo por uno que se sepa bueno."],
     ["El puerto aparece pero la conexión falla",
      "Otro programa lo tiene tomado. Un monitor serie abierto, o una segunda ventana "
      "de Thonny, bloquean el puerto."],
     ["La grabación se interrumpe a la mitad",
      "En algunas placas hay que mantener presionado el botón <b>BOOT</b> mientras "
      "comienza la grabación, y soltarlo cuando la barra empieza a avanzar."],
     ["La placa se reinicia sola todo el tiempo",
      "Alimentación insuficiente. Un puerto USB de bajo consumo, o un cable largo y "
      "delgado, no sostienen los picos de corriente del WiFi."]]))

A(nota("Guardar en la placa o en el computador", p(
    "Thonny distingue dos lugares. Al guardar un programa pregunta si va <i>en este "
    "computador</i> o <i>en el dispositivo MicroPython</i>. Un programa guardado en el "
    "computador se ejecuta en la placa pero desaparece de ella al desconectarla; uno "
    "guardado en la placa queda allí. Y hay un nombre especial: el archivo llamado "
    "<code>main.py</code> dentro de la placa se ejecuta solo cada vez que se la "
    "alimenta, sin computador de por medio. Es lo que convierte un ejercicio de "
    "laboratorio en un equipo que funciona en el tablero.")))

# =================================================================== 1.3
A(lab("1.3", "El simulador Wokwi"))

A(p(
    "<b>Wokwi</b> es un simulador de electrónica que funciona en el navegador, en "
    "<code>wokwi.com</code>. Permite armar un circuito con ESP32, escribir el programa "
    "en MicroPython y verlo funcionar sin tener la placa delante. Para un curso "
    "numeroso resuelve un problema concreto: los estudiantes pueden practicar entre "
    "clases, sin esperar turno de laboratorio y sin riesgo de dañar componentes.",

    "Sus ventajas para este libro son tres. La primera es que no hay nada que "
    "instalar. La segunda es que el hardware virtual no se quema, de modo que el "
    "estudiante puede equivocarse cuantas veces necesite. La tercera, menos evidente, "
    "es que separa los problemas: si el programa funciona en el simulador y no en la "
    "placa, el defecto está en el montaje y no en el código, lo cual acorta "
    "enormemente la búsqueda."))

A(p(
    "Wokwi simula además el WiFi, de modo que los laboratorios de red del capítulo 7 "
    "pueden ensayarse allí antes de armarlos, y dispone de un analizador lógico virtual "
    "con el que se pueden observar las tramas de I²C o UART que en la placa real son "
    "invisibles."))

A(sec("Cómo empezar"))

A(p(
    "En <code>wokwi.com</code> se elige <i>New Project → ESP32 → MicroPython</i>. "
    "Aparecen dos paneles: el diagrama del circuito a la derecha y el editor a la "
    "izquierda. Los componentes se agregan con el botón <b>+</b> y se conectan "
    "arrastrando el ratón de una pata a otra. El botón de arranque pone a correr la "
    "simulación, y <code>Ctrl+C</code> sobre la terminal entra al intérprete "
    "interactivo, igual que en Thonny."))

A(nota("Del simulador a la mesa", p(
    "El circuito que se arma en Wokwi y el que se arma en la protoboard no siempre se "
    "dibujan igual. El simulador resuelve internamente cosas que en el montaje real hay "
    "que poner —una resistencia de elevación, por ejemplo— y admite conexiones que "
    "sobre la mesa conviene hacer de otra manera. Por eso cada laboratorio de este "
    "libro trae su propia sección de circuito, y es <b>esa</b> la que debe seguirse al "
    "cablear sobre protoboard. El simulador sirve para probar la lógica del programa; "
    "el cableado del libro, para que el montaje funcione y dure.")))

# =================================================================== 1.4
A(lab("1.4", "El lenguaje: lo que conviene tener fresco"))

A(p(
    "Este libro no enseña a programar. Da por sabidos los tipos de datos, las "
    "estructuras de decisión y repetición, las listas y las funciones, que son materia "
    "de un primer curso de programación.<sup>1</sup> Lo que sí hace falta es señalar en "
    "qué se aparta MicroPython del Python que se usa sobre un computador, porque son "
    "pocas diferencias pero todas aparecen en los laboratorios."))

A(sec("El módulo machine"))

A(p(
    "Todo el acceso al hardware pasa por el módulo <code>machine</code>. Es la primera "
    "línea de casi todos los programas del libro:"))

A(codigo("""from machine import Pin, ADC, PWM, SoftI2C, UART"""))

A(tabla(
    ["Clase", "Para qué sirve", "Capítulo"],
    [["<code>Pin</code>", "Entradas y salidas digitales", "2"],
     ["<code>ADC</code>", "Leer una tensión continua", "3"],
     ["<code>Pin.irq</code>", "Atender un pulso sin estar esperándolo", "4"],
     ["<code>PWM</code>", "Salidas moduladas: brillo, velocidad, servomotores", "5"],
     ["<code>SoftI2C</code>, <code>UART</code>", "Sensores que hablan por bus", "6"]]))

A(sec("El tiempo se mide distinto"))

A(p(
    "En un computador el tiempo se maneja con <code>time.sleep()</code> y con la hora "
    "del sistema. En un microcontrolador no hay reloj de calendario al encender, y las "
    "esperas se cuentan en milisegundos o microsegundos. MicroPython agrega para eso "
    "una familia de funciones:"))

A(tabla(
    ["Función", "Qué hace"],
    [["<code>time.sleep_ms(n)</code>", "Espera n milisegundos."],
     ["<code>time.sleep_us(n)</code>", "Espera n microsegundos."],
     ["<code>time.ticks_ms()</code>",
      "Devuelve un contador de milisegundos desde que arrancó la placa."],
     ["<code>time.ticks_diff(a, b)</code>",
      "Calcula <code>a − b</code> entre dos lecturas del contador."]]))

A(aviso("Por qué no se restan los contadores directamente", p(
    "El contador de <code>ticks_ms()</code> no crece indefinidamente: llega a un máximo "
    "y vuelve a cero. Si se restan dos lecturas con el signo menos y el vuelco ocurre "
    "entre ambas, el resultado es un número negativo enorme y el programa se comporta "
    "de manera inexplicable. Un equipo que anduvo bien toda la tarde falla una vez por "
    "día, siempre a la misma hora de encendido.",
    "<code>ticks_diff()</code> existe precisamente para eso: hace la resta teniendo en "
    "cuenta el vuelco. En este libro <b>toda</b> diferencia de tiempos se calcula con "
    "<code>ticks_diff()</code>, sin excepción.")))

A(sec("Esperar o preguntar si ya pasó el tiempo"))

A(p(
    "Casi todo este libro se escribe con <code>sleep</code>, que es lo natural y lo "
    "más legible. Pero hay programas que no lo pueden usar, y conviene ver desde "
    "ahora por qué, porque es la única diferencia de estructura que separa a los "
    "programas simples de los que vienen después.",

    "Tomemos un LED que parpadea cada medio segundo. Escrito con esperas es lo más "
    "corto que puede ser:"))

A(codigo("""while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)"""))

A(p(
    "Y escrito preguntando por el reloj hace exactamente lo mismo, con el doble de "
    "líneas:"))

A(codigo("""encendido = False
cambio = time.ticks_ms()

while True:
    if time.ticks_diff(time.ticks_ms(), cambio) >= 500:
        encendido = not encendido
        led.value(1 if encendido else 0)
        cambio = time.ticks_ms()"""))

A(p(
    "Si los dos hacen lo mismo y el segundo es más largo, la pregunta es para qué "
    "sirve. La respuesta está en lo que pasa <b>mientras tanto</b>.",

    "En la primera versión, durante esos dos medios segundos el programa está "
    "detenido. No lee un pulsador, no atiende un sensor, no contesta a nadie: está "
    "esperando y nada más. En la segunda, la repetición gira miles de veces por "
    "segundo y en cada vuelta vuelve a mirar el reloj; el LED cambia cuando "
    "corresponde, y entre cambio y cambio <b>queda sitio para hacer otra cosa</b>.",

    "De ahí la regla que vale para todo el libro, y que es la única que hace falta "
    "recordar:"))

A(nota("Cuándo cada una", p(
    "Se usa <code>sleep</code> cuando el programa <b>no tiene nada más que hacer</b> "
    "mientras espera. Es el caso del primer parpadeo, del semáforo, y de cualquier "
    "programa que mide, muestra y vuelve a medir: ahí la espera no estorba a nadie y "
    "escribirlo con el reloj sólo lo haría más largo.",

    "Se usa <code>ticks_diff</code> cuando <b>sí</b>. Un pulsador que hay que seguir "
    "leyendo mientras el LED hace lo suyo, una sirena que no puede dejar de vigilar "
    "al sensor, un servidor web que tiene que atender visitas sin dejar de medir. En "
    "todos esos casos la espera dejaría ciego al programa justo cuando tiene que "
    "estar mirando.")))

A(p(
    "La cuenta vale la pena hacerla una vez. Una alarma que alterna dos tonos cada "
    "doscientos milisegundos escrita con esperas está <b>detenida cuatro quintas "
    "partes del tiempo</b> si además tiene que leer un sensor cada cincuenta "
    "milisegundos. No es que reaccione lento: es que durante ese rato el movimiento "
    "puede empezar y terminar sin que el programa se entere. Eso es exactamente lo "
    "que ocurre en el laboratorio 2.4, y es donde esta sección deja de ser teoría."))

A(aviso("El error de escribirlo a medias", p(
    "La tentación, al descubrir el problema, es acortar las esperas: cambiar "
    "<code>sleep(0.5)</code> por diez <code>sleep(0.05)</code> con la lectura del "
    "sensor en el medio. Funciona, y es por donde todos pasamos.",
    "Pero el programa queda con la estructura del tiempo metida dentro de la lógica, "
    "y agregar una segunda cosa que atender obliga a rehacerlo entero. Con "
    "<code>ticks_diff</code> cada cosa lleva su propia marca de tiempo y agregar una "
    "más son tres líneas, no una reescritura. Es la diferencia entre un programa de "
    "laboratorio y uno que se puede seguir usando.")))

A(sec("Otras diferencias que se notan"))

A(tabla(
    ["Asunto", "En la placa"],
    [["Memoria",
      "Hay unos pocos cientos de kilobytes. Un programa que acumula lecturas en una "
      "lista sin límite termina agotándola y deteniéndose."],
     ["Números reales",
      "Son de precisión simple, no doble. Alcanza para cualquier medición, pero no "
      "conviene apoyarse en la decimoquinta cifra."],
     ["Biblioteca estándar",
      "Está recortada. Módulos como <code>os</code> o <code>json</code> existen en "
      "versión reducida; muchos otros directamente no están."],
     ["Módulos adicionales",
      "Los controladores de sensores (<code>ssd1306</code>, <code>umqtt</code>) se "
      "copian a la placa como un archivo <code>.py</code> más."]]))

A(nota(None, p(
    "<sup>1</sup> Para el lector que necesite repasar esos fundamentos, el volumen "
    "anterior de esta serie, <i>Algoritmos resueltos con Python</i>, desarrolla el "
    "razonamiento, el diagrama de flujo y el programa de cada construcción del lenguaje "
    "con el mismo método que se usa aquí.")))

# =================================================================== 1.5
A(lab("1.5", "El primer programa"))

A(p(
    "Antes de conectar nada conviene comprobar que la cadena completa funciona: que "
    "Thonny escribe en la placa, que la placa ejecuta y que se puede detener un "
    "programa en marcha. Para eso alcanza con el LED que la propia placa trae soldado, "
    "en el <b>GPIO2</b> de la mayoría de las DevKit V1."))

A(sec("Objetivo"))
A(p("Hacer parpadear el LED incorporado y aprender a interrumpir un programa que no "
    "termina solo."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente"],
        [["1", "Placa ESP32 DevKit V1"], ["1", "Cable USB de datos"]],
        centradas=(0,)))

A(sec("Razonamiento"))

A(p(
    "Encender y apagar alternadamente es una repetición que no termina: mientras la "
    "placa esté alimentada, debe seguir. Dentro de esa repetición hay cuatro pasos —"
    "encender, esperar, apagar, esperar— y las dos esperas son las que hacen visible el "
    "cambio. Sin ellas el LED conmutaría millones de veces por segundo y el ojo vería "
    "un brillo constante.",

    "El pin se declara una sola vez, antes de la repetición, porque configurarlo es "
    "algo que se hace una vez y no en cada vuelta."))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time

led = Pin(2, Pin.OUT)          # el LED que la placa trae soldado

while True:
    led.value(1)               # encender
    print("encendido")
    time.sleep(0.5)

    led.value(0)               # apagar
    print("apagado")
    time.sleep(0.5)""", archivo="lab_1_5_parpadeo.py"))

A(sec("Qué debe observarse"))

A(p(
    "El LED azul de la placa parpadea dos veces por segundo y la consola de Thonny "
    "escribe alternadamente las dos palabras. El programa no se detiene por sí mismo: "
    "se interrumpe con el botón de parada de Thonny o con <code>Ctrl+C</code> sobre la "
    "consola. Conviene practicarlo ahora, porque todos los programas del libro son "
    "repeticiones sin fin y se detienen de la misma manera."))

A(nota("value(1) o on()", p(
    "<code>led.value(1)</code> y <code>led.on()</code> hacen exactamente lo mismo. En "
    "este libro se usa <code>value()</code> de manera sistemática, por una razón "
    "práctica: permite escribir <code>led.value(condicion)</code> y decidir el estado "
    "con una sola línea, en lugar de un <code>if</code> con dos ramas. Se verá "
    "aprovechado desde el laboratorio siguiente.")))

A(sec("Si algo no sale"))

A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El LED no parpadea pero la consola sí escribe",
      "Esa placa tiene el LED en otro pin, o no lo trae. Probar con el GPIO 5, o "
      "seguir directamente al capítulo 2 con un LED externo."],
     ["<code>OSError</code> al ejecutar",
      "El programa quedó guardado en el computador y no en la placa, o el intérprete "
      "seleccionado en Thonny es el del computador y no el de MicroPython."],
     ["El botón de parada no responde",
      "Mantener <code>Ctrl+C</code> presionado sobre la consola. Si tampoco, el botón "
      "<b>EN</b> de la placa reinicia el microcontrolador."]]))

A(otra_carrera(p(
    "Este primer programa es idéntico en las dos aplicaciones, y conviene señalarlo: "
    "una baliza de señalización en una planta y una luz intermitente en un tablero de "
    "vehículo son, para el microcontrolador, el mismo problema. Lo que cambia es la "
    "etapa de potencia que hay después del pin —un relé, un transistor— y los tiempos. "
    "El algoritmo, no.")))

A(ejercicios([
    "Modifique los tiempos para que el LED quede encendido un cuarto de segundo y "
    "apagado un segundo y medio. ¿Cambia en algo la estructura del programa?",

    "Escriba el programa usando una sola espera por vuelta en lugar de dos. "
    "Ayuda: <code>led.value(not led.value())</code>.",

    "Guarde el programa en la placa con el nombre <code>main.py</code>, desconecte el "
    "cable USB y alimente la placa con un cargador de teléfono. Explique qué ocurre y "
    "por qué.",

    "¿Cuántas veces por segundo parpadearía el LED si se quitaran las dos esperas? "
    "Justifique con el dato de frecuencia que devolvió <code>machine.freq()</code>.",

    "Consultando la tabla del apartado 1.1, indique cuáles de los siguientes pines "
    "podrían haberse usado en lugar del GPIO2 y cuáles no: 4, 9, 34, 23, 36.",
]))
