# -*- coding: utf-8 -*-
"""Anexos del libro."""
from maqueta import (lab, sec, codigo, consola, tabla, aviso, nota, p,
                     esc)

PARTES = []
A = PARTES.append


def anexo(letra, titulo, entrada):
    return ('<div class="cap"><p class="num">ANEXO {}</p>\n'
            '<h1>{}</h1>\n<hr class="linea">\n'
            '<div class="entrada">{}</div>\n').format(letra, esc(titulo),
                                                      entrada)


# =================================================================== A
A(anexo("A", "Crear la cuenta y el tablero en Adafruit IO", p(
    "El laboratorio 7.6 publica en Adafruit IO, y para que publique en algún "
    "lado hay que haber creado antes la cuenta, los <i>feeds</i> y el "
    "tablero. Son cinco minutos de trabajo en el navegador, una sola vez, y "
    "conviene tenerlos hechos antes de la clase.")))

A(lab("A.1", "La cuenta y la clave"))

A(tabla(
    ["Paso", "Qué hacer"],
    [["1", "Entrar en <code>io.adafruit.com</code> y crear una cuenta "
      "gratuita. Sirve cualquier correo."],
     ["2", "Una vez dentro, pulsar la <b>llave amarilla</b> de la barra "
      "superior. Se abre un recuadro con dos datos."],
     ["3", "El primero es el <b>usuario</b> y el segundo la <b>clave</b> "
      "—una cadena larga que empieza con <code>aio_</code>."],
     ["4", "Copiar los dos a <code>config.py</code>, en la placa. No al "
      "programa."]]))

A(codigo("""AIO_USUARIO = "jmarcelo"
AIO_CLAVE = "aio_0000000000000000000000000000000000\"""",
    archivo="config.py"))

A(aviso("Esa clave da acceso a toda la cuenta", p(
    "No es una contraseña de un feed: con ella se puede leer, escribir y "
    "borrar cualquier cosa de la cuenta. Por eso no va dentro del programa, "
    "no se comparte y no se muestra en una diapositiva.",
    "Si se publicó por error, desde la misma llave amarilla se la puede "
    "<b>regenerar</b>, y la anterior deja de servir en el acto. Es la ventaja "
    "de estas claves frente a la del WiFi.")))

A(lab("A.2", "Los feeds"))

A(p(
    "Un <b>feed</b> es donde se guarda una magnitud. Hace falta uno por cada "
    "cosa que se quiera publicar: uno para la temperatura, otro para la "
    "humedad. Si el programa publica en un feed que no existe, el servidor "
    "acepta la conexión y <b>descarta el dato sin avisar</b>, de modo que "
    "crear los feeds primero ahorra un buen rato de desconcierto."))

A(tabla(
    ["Paso", "Qué hacer"],
    [["1", "En el menú superior, entrar en <b>Feeds</b>."],
     ["2", "Pulsar <b>New Feed</b> y ponerle nombre. Para el laboratorio 7.6, "
      "<code>temperatura</code> y <code>humedad</code>; para el 7.9, "
      "<code>foco</code>."],
     ["3", "El nombre tiene que escribirse <b>igual</b> que en el programa, "
      "con las mismas minúsculas y sin acentos."]]))

A(nota("Dos límites de la cuenta gratuita", p(
    "Hay un tope de <b>cinco feeds</b> y otro de <b>treinta datos por "
    "minuto</b>, contando todos los feeds juntos. El segundo es el que "
    "aparece en el recuadro del laboratorio 7.6, con la cuenta que permite "
    "elegir el intervalo. El primero se nota antes: un medidor eléctrico que "
    "publique tensión, corriente, potencia, factor de potencia y energía ya "
    "ocupa los cinco.")))

A(lab("A.3", "El tablero"))

A(p(
    "El tablero —<i>dashboard</i>— es la pantalla donde se ven los datos. Se "
    "arma con bloques, y cada bloque se conecta a uno o más feeds."))

A(tabla(
    ["Paso", "Qué hacer"],
    [["1", "En el menú superior, <b>Dashboards</b> → <b>New Dashboard</b>. "
      "Ponerle nombre y pulsar <i>Create</i>."],
     ["2", "Entrar al tablero recién creado. Arriba a la derecha hay un "
      "engranaje: <b>Dashboard Settings</b> → <b>Create New Block</b>."],
     ["3", "Elegir el tipo de bloque. Para ver la evolución en el tiempo, el "
      "<b>gráfico de líneas</b>; para un valor suelto, el indicador "
      "circular; para <b>mandar</b> una orden en lugar de mirar un dato, el "
      "<b>interruptor</b> (<i>toggle</i>) del laboratorio 7.9."],
     ["4", "En <b>Connect Feeds</b>, marcar los feeds que ese bloque va a "
      "mostrar. Un gráfico de líneas admite varios a la vez, y poner "
      "temperatura y humedad juntas permite compararlas."],
     ["5", "<b>Next step</b>, ajustar el título y los límites del eje, y "
      "crear."]]))

A(nota("El bloque interruptor manda, no informa", p(
    "Los bloques de gráfico e indicador <b>leen</b> un feed. El interruptor lo "
    "<b>escribe</b>: cada vez que se lo mueve, publica un valor, y quien esté suscrito "
    "a ese feed lo recibe. Es lo que usa el laboratorio 7.9 para encender el relé.",
    "Al crearlo pregunta qué valor manda en cada posición. Conviene poner "
    "<code>1</code> y <code>0</code>, que es lo que espera el programa del libro; si "
    "se dejan <code>ON</code> y <code>OFF</code>, hay que cambiar la función "
    "<code>atender()</code> en lugar del bloque.")))

A(p(
    "Desde ese momento, cada vez que la placa publique, el bloque se "
    "actualiza solo. El tablero se puede compartir con un enlace público "
    "desde <i>Dashboard Privacy</i>, que es lo que permite que el resto del "
    "curso vea la medición sin tener cuenta."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El programa conecta pero el feed queda vacío",
      "El feed no existe, o el nombre está escrito distinto. El servidor no "
      "avisa."],
     ["Avisos de <i>throttle</i>",
      "Se pasó de treinta datos por minuto. Subir el intervalo."],
     ["<code>MQTTException: 5</code>",
      "Usuario o clave mal copiados. La clave es la de la llave amarilla, no "
      "la contraseña de ingreso."],
     ["El bloque no muestra nada aunque el feed tenga datos",
      "El rango de tiempo del gráfico es anterior a los datos, o el bloque "
      "quedó conectado a otro feed."]]))

# =================================================================== B
A(anexo("B", "Los módulos que se copian a la placa", p(
    "MicroPython trae lo básico, pero varios laboratorios necesitan módulos "
    "que no vienen incluidos. Son archivos <code>.py</code> que se copian "
    "<b>dentro de la placa</b>, una sola vez, igual que se copia un "
    "programa. Una vez allí quedan disponibles para cualquier programa que "
    "los importe.")))

A(tabla(
    ["Archivo", "Para qué", "Laboratorios"],
    [["<code>config.py</code>", "Guarda las claves fuera del programa. Se "
      "copia de <code>config_ejemplo.py</code> y se completa.",
      "7.1 en adelante"],
     ["<code>iot.py</code>", "Conexión a la red y al servidor. Se escribe "
      "en el 7.1 y se completa en el 7.6; el del repositorio es el completo.",
      "7.1 y 7.6 a 7.9"],
     ["<code>ssd1306.py</code>", "Controlador de la pantalla OLED.",
      "6.1, 6.2, 6.6"],
     ["<code>ble_uart.py</code>", "Puerto serie sobre Bluetooth. Se escribe "
      "en el laboratorio 7.4.", "7.4"],
     ["<code>pzem.py</code>", "Protocolo Modbus del medidor eléctrico.",
      "6.5"],
     ["<code>umqtt/</code>", "Cliente MQTT. Viene con algunas versiones del "
      "firmware; si no, se instala aparte.", "7.6, 7.9"]]))

A(sec("Cómo copiarlos"))

A(p(
    "Con Thonny, la manera más simple es abrir el archivo en el computador, "
    "y después <i>Archivo → Guardar como…</i> eligiendo <b>«dispositivo "
    "MicroPython»</b> en lugar de «este computador». El nombre debe quedar "
    "exactamente igual, incluida la extensión."))

A(p(
    "Para comprobar que están, desde la consola:"))

A(consola(""">>> import os
>>> os.listdir()
['boot.py', 'config.py', 'iot.py', 'ssd1306.py', 'main.py']"""))

A(nota("Dónde conseguirlos", p(
    "<code>config.py</code>, <code>iot.py</code> y <code>ble_uart.py</code> "
    "están escritos completos en este libro. <code>ssd1306.py</code> y "
    "<code>umqtt</code> son parte de la biblioteca oficial de MicroPython. "
    "Todos, junto con los programas de los laboratorios, están también en el "
    "repositorio que acompaña al libro.")))

# =================================================================== C
A(anexo("C", "Los pines de cada laboratorio", p(
    "Tabla de consulta rápida. Sirve para armar un laboratorio sin releer su "
    "capítulo y, sobre todo, para ver de un vistazo qué montajes pueden "
    "convivir en la misma placa y cuáles se pisan.")))

A(tabla(
    ["Lab.", "Montaje", "Pines"],
    [["1.5", "LED de la placa", "GPIO2"],
     ["2.1", "LED externo", "GPIO23"],
     ["2.2", "Semáforo", "GPIO23, GPIO21, GPIO17"],
     ["2.3", "Pulsador y LED", "GPIO16, GPIO5"],
     ["2.4", "PIR y zumbador", "GPIO4, GPIO5, VIN"],
     ["2.5", "Módulo de relé y pulsador", "GPIO19, GPIO16"],
     ["3.1", "Potenciómetro", "GPIO34, 3V3"],
     ["3.2", "Divisor de 5 V", "GPIO35, VIN"],
     ["3.3", "LM35", "GPIO32, VIN"],
     ["3.4", "Termistor NTC", "GPIO33, 3V3"],
     ["3.5", "Calibración", "GPIO34, 3V3"],
     ["4.1 – 4.3", "Puente generador-contador", "GPIO25 → GPIO26"],
     ["4.4", "Tacómetro con L298N", "GPIO19, GPIO18, GPIO5, GPIO17, VIN"],
     ["5.2", "Brillo con potenciómetro", "GPIO34, GPIO18, 3V3"],
     ["5.3 – 5.4", "Servomotor", "GPIO4, VIN"],
     ["5.5", "Zumbador pasivo", "GPIO5"],
     ["6.1 – 6.2", "Pantalla OLED (I²C)", "GPIO22 (SCL), GPIO21 (SDA), 3V3"],
     ["6.3", "DHT11", "GPIO14, 3V3"],
     ["6.4", "Presión HX710B", "GPIO16 (OUT), GPIO4 (SCK), 3V3"],
     ["6.5", "Medidor PZEM-004T", "GPIO16 (RX), GPIO17 (TX), 3V3"],
     ["6.6", "Tablero local", "GPIO22, GPIO21, GPIO14, GPIO33, 3V3"],
     ["7.2 – 7.4", "DHT11 con red o Bluetooth", "GPIO14, 3V3"],
     ["7.5", "ESP-NOW", "GPIO4 en cada placa"],
     ["7.8 – 7.9", "Relé gobernado a distancia", "GPIO19"]],
    centradas=(0,)))

A(aviso("Los pines que este libro no usa nunca", p(
    "<b>GPIO 6 a 11</b> están conectados a la memoria del módulo: usarlos "
    "impide arrancar. <b>GPIO 1 y 3</b> son la consola del USB. <b>GPIO 34, "
    "35, 36 y 39</b> sólo pueden ser entrada. Y ningún sensor analógico de "
    "este libro va al ADC2 —GPIO 0, 2, 4, 12 a 15 y 25 a 27—, porque deja de "
    "medir con el WiFi encendido.",
    "El plano completo, con los colores que agrupan estos casos, está en la "
    "figura 1.1, que es el de la placa de <b>30 pines</b>: la que usan todas las "
    "figuras del libro. Si la suya tiene diecinueve agujeros por lado en vez de "
    "quince, es la de 38 y los pines están en otro orden —los nombres de esta tabla "
    "siguen valiendo, la posición en el borde no.")))

A(sec("Qué se pisa con qué"))

A(tabla(
    ["Conflicto", "Dónde aparece"],
    [["El bus I²C ocupa <b>GPIO21 y GPIO22</b>",
      "El semáforo del 2.2 usa GPIO21 y el medidor del 6.5 usa GPIO17: "
      "ninguno de los dos puede convivir con la pantalla sin recablear."],
     ["<b>GPIO5</b> aparece en cuatro laboratorios",
      "2.3, 2.4, 4.4 y 5.5. Al combinar montajes es el primero que hay que "
      "revisar."],
     ["<b>GPIO4</b> es SCK del HX710B y señal del servo",
      "El 6.4 y el 5.3 no pueden estar armados a la vez."],
     ["<b>GPIO16 y GPIO17</b> son el puerto serie del PZEM",
      "El 6.5 se lleva los dos; el 2.3, el 2.5 y el 6.4 también usan GPIO16."],
     ["<b>GPIO19</b> gobierna el relé y también el puente H",
      "El 2.5, el 7.8 y el 7.9 lo usan para el relé; el 4.4 lo usa para ENA del "
      "L298N. No pueden convivir."]]))
