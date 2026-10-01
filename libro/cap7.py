# -*- coding: utf-8 -*-
"""Capítulo 7 — Monitoreo remoto."""
from maqueta import (capitulo, lab, sec, codigo, consola, tabla,
                     aviso, nota, otra_carrera, ejercicios, p, figura)
import circuitos_cap7 as CIR

PARTES = []
A = PARTES.append

A(capitulo(7, "Monitoreo remoto", p(
    "Hasta aquí el dato nacía y moría en la mesa de trabajo. Se medía, se "
    "decidía y se mostraba, pero para verlo había que estar sentado frente a "
    "la placa. Este capítulo lo saca de ahí.",

    "Hay cuatro maneras de hacerlo y no compiten entre sí: resuelven "
    "problemas distintos y cada una tiene su costo. Conviene conocer las "
    "cuatro antes de elegir, porque la tentación es ir directamente a "
    "internet cuando muchas veces alcanza con algo mucho más simple.")))

A(figura(CIR.rutas(),
         "Las cuatro maneras de sacar el dato de la placa. Las dos primeras "
         "no necesitan más que la red del taller o ni siquiera eso; la "
         "última es la única que guarda el histórico.", capitulo=7))

A(p(
    "El orden de los laboratorios sigue ese cuadro, de menos a más "
    "dependencias. Se empieza por lo que funciona con la placa sola y se "
    "termina en el tablero que se mira desde otra ciudad."))

# =================================================================== 7.1
A(lab("7.1", "Conectar a la red sin publicar las claves"))

A(sec("Objetivo"))
A(p("Conectar el ESP32 al WiFi, y establecer de una vez la disciplina que "
    "van a seguir todos los programas del capítulo: que ninguna clave quede "
    "escrita dentro del programa."))

A(sec("Razonamiento"))

A(p(
    "Conectarse es corto: se enciende la interfaz, se le pasan el nombre de "
    "la red y la clave, y se espera. Lo que merece atención es dónde se "
    "guardan esos dos datos.",

    "La manera evidente —escribirlos en el programa— tiene un problema que no "
    "se nota hasta que ya ocurrió. El programa se comparte con los "
    "compañeros, se sube a un repositorio, se imprime en un informe, se pega "
    "en una diapositiva. La clave del WiFi del taller viaja con él a todas "
    "partes, y lo mismo pasa con la clave del servicio de internet del "
    "laboratorio 7.6, que además da acceso a una cuenta.",

    "La solución es separar el <b>programa</b> de la <b>configuración</b>. El "
    "programa se comparte; el archivo de configuración no sale de la placa. "
    "Es una línea más de trabajo y evita un problema que después no tiene "
    "arreglo: una clave publicada hay que cambiarla, no basta con borrar el "
    "archivo."))

A(sec("Los dos archivos"))

A(p("El primero es la plantilla, y es el único de los dos que se comparte. Se "
    "copia con el nombre <code>config.py</code> y ahí se escriben los datos "
    "reales."))

A(codigo("""# config_ejemplo.py — plantilla. Copiela como config.py y
# complete los datos. config.py no se comparte con nadie.

WIFI_SSID = "NOMBRE_DE_SU_RED"
WIFI_CLAVE = "CLAVE_DE_SU_RED"

AIO_USUARIO = "su_usuario"
AIO_CLAVE = "aio_0000000000000000000000000000000000"

# Estos cuatro recien hacen falta en el laboratorio 7.7, pero van
# aqui desde el principio: la plantilla es una sola y asi no hay dos
# versiones dando vueltas.
INFLUX_HOST = "192.168.0.10"
INFLUX_ORG = "taller"
INFLUX_BUCKET = "sensores"
INFLUX_TOKEN = "PEGUE_AQUI_SU_TOKEN\"""",
    archivo="config_ejemplo.py"))

A(p("El segundo es el módulo que van a importar todos los programas del "
    "capítulo. Se escribe una sola vez:"))

A(codigo("""# iot.py — conexion a la red, compartida por todo el capitulo
import time
import network
import config


def conectar_wifi(intentos=20):
    \"\"\"Conecta el ESP32 a la red. Devuelve la direccion IP.\"\"\"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando a la red", config.WIFI_SSID, "...")
        wlan.connect(config.WIFI_SSID, config.WIFI_CLAVE)
        for _ in range(intentos * 2):
            if wlan.isconnected():
                break
            time.sleep(0.5)

    if not wlan.isconnected():
        raise OSError("No se pudo conectar. Revise config.py")

    ip = wlan.ifconfig()[0]
    print("Red conectada. IP:", ip)
    return ip""", archivo="iot.py"))

A(aviso("Si una clave ya se publicó", p(
    "Borrar el archivo no alcanza. Una clave que estuvo publicada hay que "
    "darla por perdida y <b>cambiarla</b>: la del WiFi en el router, la del "
    "servicio de internet regenerándola desde la cuenta. Es incómodo una vez "
    "y barato comparado con la alternativa.")))

A(sec("Qué debe observarse"))
A(consola(""">>> import iot
>>> iot.conectar_wifi()
Conectando a la red TALLER ...
Red conectada. IP: 192.168.0.50
'192.168.0.50'"""))

A(p("Esa dirección es la que va a hacer falta en el laboratorio siguiente. "
    "Conviene anotarla: en muchas redes cambia cada vez que la placa se "
    "reconecta."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["«No se pudo conectar. Revise config.py»",
      "Nombre o clave equivocados. Ojo con las mayúsculas: se distinguen."],
     ["Conecta en casa y no en el taller",
      "La red del taller es de <b>5 GHz</b>. El ESP32 sólo trabaja en 2,4 GHz "
      "y esa red no le aparece siquiera."],
     ["<code>ImportError: no module named 'config'</code>",
      "Falta copiar la plantilla como <code>config.py</code> <b>dentro de la "
      "placa</b>, no en el computador."],
     ["Conecta pero después se cae sola",
      "Señal débil, o la red exige portal de acceso. El ESP32 no puede pasar "
      "un portal con usuario y contraseña de navegador."]]))

# =================================================================== 7.2
A(lab("7.2", "La placa como servidor web"))

A(sec("Objetivo"))
A(p("Que cualquier teléfono de la misma red abra la dirección de la placa y "
    "vea la medición, sin ninguna cuenta ni servicio de por medio."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Sensor DHT11", "el mismo del laboratorio 6.3"],
         ["1", "Teléfono o computadora", "en la <b>misma</b> red que la placa"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_7_2")[0], ancha=True, epigrafe=
         "El montaje es el del laboratorio 6.3, sin recablear. GPIO14 está en "
         "la columna izquierda, así que su cable rodea la placa.", capitulo=7))

A(sec("Razonamiento"))

A(p(
    "Un servidor web es un programa que espera conexiones en un puerto, y "
    "cuando llega una, contesta con un texto. Ese texto es la página. No hay "
    "más misterio: el navegador pide, la placa responde.",

    "La parte que sí tiene miga es <b>dónde se mide</b>. La manera natural de "
    "escribirlo es: llega la visita, leo el sensor, contesto. Y esa manera "
    "está mal por dos razones."))

A(p(
    "La primera es el tiempo. El DHT11 necesita alrededor de dos segundos "
    "entre lecturas, de modo que hay que esperarlo; y durante esa espera el "
    "programa no atiende a nadie más. Con la página refrescándose sola cada "
    "cuatro segundos, la mitad del tiempo el servidor está dormido. Con un "
    "curso entero apuntando a la misma placa, las visitas se hacen cola. "
    "Medido sobre el programa: <b>2,00 s por visita</b> y <b>20 s para diez "
    "visitas seguidas</b>.",

    "La segunda es más grave. El DHT11 entrega de vez en cuando una trama con "
    "error de suma de verificación —es normal, no significa que esté malo—, y "
    "si la lectura está dentro del lazo sin protección, ese error termina el "
    "programa. La página deja de responder hasta que alguien reinicia la "
    "placa.",

    "La corrección es una sola y arregla las dos cosas: <b>medir por reloj</b>, "
    "en el lazo principal, y que la visita reciba el último valor guardado. La "
    "misma idea del laboratorio 2.4, donde la sirena no podía impedir que el "
    "programa siguiera vigilando. Con la medición separada, la respuesta baja "
    "a <b>menos de 10 ms</b> y un sensor que falla deja el último valor bueno "
    "en pantalla en vez de matar el servidor."))

A(sec("Programa"))

A(codigo("""import socket
import time
import network
from machine import Pin
import dht
import config

PIN_DATOS = 14
PUERTO = 80
INTERVALO_MS = 3000       # cada cuanto se toma una medicion nueva

sensor = dht.DHT11(Pin(PIN_DATOS))

# Ultima medicion valida. El servidor entrega esto, no una lectura
# hecha en el momento: medir dentro de la atencion de la peticion
# haria esperar al visitante y bloquearia a los demas.
temperatura = None
humedad = None
medido_en = 0
fallas = 0


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a la red", config.WIFI_SSID, "...")
        wlan.connect(config.WIFI_SSID, config.WIFI_CLAVE)
        for _ in range(40):
            if wlan.isconnected():
                break
            time.sleep(0.5)
    if not wlan.isconnected():
        raise OSError("No se pudo conectar. Revise config.py")
    return wlan.ifconfig()[0]


def medir_si_toca():
    \"\"\"Toma una medicion nueva si paso el intervalo.

    Si el sensor falla se conserva el ultimo valor bueno en lugar
    de detener el servidor.
    \"\"\"
    global temperatura, humedad, medido_en, fallas
    if temperatura is not None and \\
            time.ticks_diff(time.ticks_ms(), medido_en) < INTERVALO_MS:
        return
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        fallas = 0
    except OSError:
        fallas = fallas + 1
    medido_en = time.ticks_ms()


def pagina():
    if temperatura is None:
        valores = "<p>Esperando la primera medicion...</p>"
    else:
        valores = ("<p>Temperatura: {} C</p>\\n"
                   "<p>Humedad: {} %</p>").format(temperatura, humedad)
        if fallas > 0:
            valores += ("\\n<p class='aviso'>{} lecturas "
                        "fallidas</p>").format(fallas)

    return \"\"\"<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="4">
<title>Monitoreo DHT11</title>
<style>
body {{ text-align:center; font-family:Arial, sans-serif; }}
h1 {{ color:navy; }}
p {{ font-size:30px; }}
p.aviso {{ font-size:16px; color:#A81C22; }}
</style>
</head>
<body>
<h1>MONITOREO SENSOR DHT11</h1>
{}
</body>
</html>
\"\"\".format(valores)


def camino_pedido(peticion):
    \"\"\"Extrae el camino de la primera linea: GET /algo HTTP/1.1\"\"\"
    try:
        return peticion.split(" ")[1]
    except IndexError:
        return "/"


def main():
    ip = conectar_wifi()

    servidor = socket.socket()
    # Sin esto, al reiniciar el programa el puerto queda ocupado un
    # rato y la placa responde "address in use".
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(socket.getaddrinfo("0.0.0.0", PUERTO)[0][-1])
    servidor.listen(2)
    servidor.settimeout(1)      # para poder medir entre visita y visita

    print("Servidor listo. Abra http://{}/ en el navegador.".format(ip))

    while True:
        medir_si_toca()

        try:
            cliente, direccion = servidor.accept()
        except OSError:
            continue            # no vino nadie: se vuelve a medir

        try:
            cliente.settimeout(3)
            peticion = cliente.recv(1024).decode()

            if camino_pedido(peticion) == "/favicon.ico":
                # El navegador pide siempre el icono. Se le contesta
                # que no existe en vez de mandarle la pagina entera.
                cliente.sendall(b"HTTP/1.0 404 Not Found\\r\\n\\r\\n")
            else:
                cliente.sendall(b"HTTP/1.0 200 OK\\r\\n"
                                b"Content-Type: text/html\\r\\n\\r\\n")
                cliente.sendall(pagina().encode())
        except OSError as e:
            print("Visita interrumpida:", e)
        finally:
            cliente.close()


if __name__ == "__main__":
    main()""", archivo="lab_7_2_servidor_web.py"))

A(nota("Tres detalles pequeños que evitan tres molestias", p(
    "<code>SO_REUSEADDR</code> evita el <code>Errno 98, address in use</code> "
    "al detener y volver a ejecutar. <code>settimeout(3)</code> en el cliente "
    "impide que un navegador que se conecta y no pide nada deje al servidor "
    "esperando para siempre. Y <code>sendall</code> —en lugar de "
    "<code>send</code>— garantiza que la página salga entera: "
    "<code>send</code> puede mandar sólo una parte.")))

A(sec("Qué debe observarse"))
A(p(
    "Escribiendo la dirección en el teléfono aparece el título y las dos "
    "magnitudes. La página se refresca sola y el número cambia al soplar sobre "
    "el sensor. La respuesta es inmediata: no hay espera perceptible.",

    "<b>La prueba que vale la pena hacer en clase:</b> desconecte la pata de "
    "datos del DHT11 con el servidor andando. La página <b>sigue "
    "respondiendo</b>, muestra el último valor bueno y avisa en rojo cuántas "
    "lecturas fallaron. Vuelva a conectarla y el aviso desaparece solo. Con la "
    "versión que mide dentro de la petición, ese mismo gesto deja la página "
    "muerta."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El navegador no encuentra la dirección",
      "El teléfono está en otra red, o en datos móviles."],
     ["<code>Address already in use</code>",
      "Quedó corriendo una copia anterior. El botón <b>EN</b> reinicia."],
     ["Dice «Esperando la primera medición» y no cambia",
      "El sensor no entregó ninguna trama buena todavía. Revise la "
      "resistencia de elevación en la línea de datos."],
     ["La dirección funcionaba ayer y hoy no",
      "El router le dio otra a la placa. Vuelva a mirar lo que imprime al "
      "arrancar."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el tablero de un equipo "
    "consultable desde el celular dentro de la planta, sin pasar por la red "
    "corporativa ni pedir permisos de informática. Cambiando el DHT11 por el "
    "transmisor de presión del laboratorio 6.4 se obtiene un indicador remoto "
    "de línea.",
    "<b>En el área mecánica</b>, el mismo servidor con el termistor de refrigerante "
    "—laboratorio 3.4— y la escala llevada a 60–110 °C da un tablero que se "
    "mira desde el celular con el motor en marcha, sin tender cables hasta el "
    "banco.")))

# =================================================================== 7.3
A(lab("7.3", "La misma página con indicadores de barra"))

A(sec("Objetivo"))
A(p("Cambiar la presentación sin tocar nada de lo que consigue los datos."))

A(sec("Razonamiento"))

A(p(
    "Es el mismo servidor. Lo único que cambia es la función "
    "<code>pagina()</code>, que en vez de escribir el número dibuja una barra "
    "proporcional. Vale la pena hacerlo notar, porque es la idea que el libro "
    "viene repitiendo desde el capítulo 6: <b>la forma de mostrar los datos no "
    "debería obligar a tocar la parte que los consigue</b>."))

A(codigo("""TEMPERATURA_MIN, TEMPERATURA_MAX = 0, 50
HUMEDAD_MIN, HUMEDAD_MAX = 20, 90


def porcentaje(valor, minimo, maximo):
    \"\"\"Posicion de valor dentro de la escala, de 0 a 100.

    Recorta solo el LARGO DE LA BARRA. El numero que se escribe al
    lado sigue siendo el que entrego el sensor.
    \"\"\"
    recorrido = maximo - minimo
    if recorrido <= 0:
        return 0.0
    proporcion = (valor - minimo) * 100.0 / recorrido
    if proporcion < 0:
        return 0.0
    if proporcion > 100:
        return 100.0
    return proporcion


def barra(etiqueta, valor, unidad, minimo, maximo, color):
    fuera = "" if minimo <= valor <= maximo else " (fuera de escala)"
    return \"\"\"<div class="marco">
  <div class="relleno"
       style="width:{:.1f}%; background-color:{};"></div>
  <div class="cifra">{} {}</div>
</div>
<div class="rotulo">{} ({} a {} {}){}</div>\"\"\".format(
        porcentaje(valor, minimo, maximo), color, valor, unidad,
        etiqueta, minimo, maximo, unidad, fuera)""",
    archivo="lab_7_3_barras.py"))

A(aviso("Un indicador no corrige la medición", p(
    "La hoja de datos del DHT11 declara humedad de 20 a 90 %, y es tentador "
    "recortar la lectura a ese rango antes de mostrarla. Si se hace, una "
    "humedad real de 15 % aparece en pantalla como 20 %, y el instrumento "
    "está mintiendo.",
    "El recorte se aplica <b>sólo al largo de la barra</b>. El número que se "
    "informa es siempre el que entregó el sensor, y si queda fuera de escala "
    "la página lo dice. En instrumentación este criterio no es negociable: un "
    "indicador que ajusta la medición para que entre en su escala es peor que "
    "no tener indicador.")))

A(sec("Qué debe observarse"))
A(p("Dos barras, la de temperatura sobre una escala de 0 a 50 °C y la de "
    "humedad de 20 a 90 %, con la cifra escrita encima. Soplando sobre el "
    "sensor la barra de humedad avanza a la vista."))

# =================================================================== 7.4
A(lab("7.4", "El celular por Bluetooth"))

A(sec("Objetivo"))
A(p("Mandar la medición al teléfono por Bluetooth, sin red, sin router y sin "
    "que el teléfono ni la placa estén conectados a nada."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["1", "Sensor DHT11", "el mismo del laboratorio 7.2"],
         ["1", "Teléfono", "con la aplicación <b>Serial Bluetooth "
          "Terminal</b>, gratuita"]],
        centradas=(0,)))

A(sec("El circuito"))
A(p("El mismo del laboratorio 7.2, sin cambios (figura 7.2)."))

A(aviso("Bluetooth clásico y Bluetooth LE no son lo mismo", p(
    "El ESP32 tiene los dos, pero <b>MicroPython sólo expone el Bluetooth de "
    "baja energía (BLE)</b>. El «puerto serie por Bluetooth» de toda la vida "
    "—el perfil SPP, el que se usa con los módulos HC-05— no está disponible "
    "desde MicroPython.",
    "Esto importa porque la aplicación <i>Serial Bluetooth Terminal</i> "
    "maneja las dos clases y arranca en la de siempre. Si se busca la placa "
    "en la pestaña de <b>Bluetooth Classic</b> no aparece nunca, y no hay "
    "nada mal en el programa: hay que buscarla en la pestaña de "
    "<b>Bluetooth LE</b>. Es el tropiezo número uno de este laboratorio.")))

A(sec("Razonamiento"))

A(p(
    "BLE no es un puerto serie: es una base de datos de características que "
    "el teléfono lee, escribe o se suscribe. Para que se comporte como un "
    "cable serie existe un acuerdo de la industria —el <i>Nordic UART "
    "Service</i>— que define dos características, una para cada sentido. "
    "Cualquier aplicación de terminal lo reconoce, y ése es el motivo por el "
    "que funciona con la aplicación del teléfono sin configurar nada.",

    "Ese acuerdo se implementa una vez, en un módulo que se copia a la placa "
    "y que los programas importan. Lo que el programa del laboratorio hace es "
    "sólo tres cosas: crear el enlace con un nombre, preguntar si hay alguien "
    "conectado y escribir."))

A(sec("El módulo, que se copia a la placa"))

A(codigo("""# ble_uart.py — puerto serie sobre Bluetooth LE.
# Se copia a la placa una sola vez, como ssd1306.py.
import bluetooth
from micropython import const

_CONECTADO = const(1)
_DESCONECTADO = const(2)
_ESCRITURA = const(3)

# Identificadores del Nordic UART Service. Son estos y no otros:
# es lo que la aplicacion del telefono busca.
_SERV = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
       bluetooth.FLAG_NOTIFY)
_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
       bluetooth.FLAG_WRITE)


class BLEUART:
    def __init__(self, nombre="ESP32"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._evento)
        ((self._tx, self._rx),) = self._ble.gatts_register_services(
            ((_SERV, (_TX, _RX)),))
        self._centrales = set()
        self._buzon = bytearray()
        # anuncio: banderas + nombre completo
        n = nombre.encode()
        self._anuncio = bytearray((2, 0x01, 0x06, len(n) + 1, 0x09)) + n
        self._anunciar()

    def _anunciar(self):
        self._ble.gap_advertise(100000, adv_data=self._anuncio)

    def _evento(self, evento, datos):
        if evento == _CONECTADO:
            conn, _, _ = datos
            self._centrales.add(conn)
        elif evento == _DESCONECTADO:
            conn, _, _ = datos
            self._centrales.discard(conn)
            # Hay que volver a anunciarse: si no, el telefono no
            # puede reconectarse y parece que la placa se colgo.
            self._anunciar()
        elif evento == _ESCRITURA:
            conn, atributo = datos
            if atributo == self._rx:
                self._buzon += self._ble.gatts_read(self._rx)

    def conectado(self):
        return len(self._centrales) > 0

    def write(self, texto):
        \"\"\"Manda texto al telefono. Si no hay nadie, no hace nada.\"\"\"
        datos = texto.encode() if isinstance(texto, str) else texto
        for conn in self._centrales:
            self._ble.gatts_notify(conn, self._tx, datos)

    def read(self):
        \"\"\"Devuelve lo recibido y vacia el buzon. Puede ser vacio.\"\"\"
        datos = bytes(self._buzon)
        self._buzon = bytearray()
        return datos""", archivo="ble_uart.py"))

A(aviso("Veinte caracteres por mensaje", p(
    "Una notificación de BLE entra en <b>20 bytes</b> mientras el teléfono no "
    "negocie un tamaño mayor, y MicroPython no lo negocia. Lo que pase de ahí "
    "se pierde sin aviso: el mensaje llega cortado y no hay ningún error.",
    "Por eso los mensajes de este laboratorio son cortos y van de a uno "
    "—<code>T:23.0C</code> son siete caracteres— en lugar de una línea larga "
    "con todo junto. Es una restricción del medio, no del programa, y "
    "conviene tenerla presente al inventar el formato.")))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time
import dht
from ble_uart import BLEUART

PIN_DATOS = 14
NOMBRE = "ESP32-TALLER"      # el que va a aparecer en el telefono
INTERVALO = 2                # segundos entre mediciones

sensor = dht.DHT11(Pin(PIN_DATOS))
enlace = BLEUART(NOMBRE)

print("Bluetooth activo como", NOMBRE)
print("Busque ese nombre en la pestana BLE de la aplicacion.")

fallas = 0

while True:
    # Lo que el telefono haya escrito. Puede venir vacio, asi que
    # se comprueba ANTES de decodificar: .decode() sobre nada
    # levanta una excepcion y corta el programa.
    recibido = enlace.read()
    if recibido:
        print("El telefono dice:", recibido.decode().strip())

    try:
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        fallas = 0
    except OSError:
        fallas = fallas + 1
        print("Lectura fallida ({}).".format(fallas))
        time.sleep(INTERVALO)
        continue

    print("Temperatura: {} C   Humedad: {} %".format(
        temperatura, humedad))

    # Escribir sin nadie conectado no da error, pero tampoco sirve:
    # preguntarlo permite avisar en la consola que el telefono se fue.
    if enlace.conectado():
        enlace.write("T:{}C\\n".format(temperatura))
        enlace.write("H:{}%\\n".format(humedad))
    else:
        print("   (nadie conectado todavia)")

    time.sleep(INTERVALO)""", archivo="lab_7_4_bluetooth.py"))

A(sec("Cómo conectarse desde el teléfono"))

A(tabla(
    ["Paso", "Qué hacer"],
    [["1", "Instalar <b>Serial Bluetooth Terminal</b> y dar permiso de "
      "ubicación: Android lo exige para poder buscar dispositivos BLE."],
     ["2", "Abrir el menú lateral y entrar en <i>Devices</i>."],
     ["3", "Elegir la pestaña <b>Bluetooth LE</b>. No la de Classic."],
     ["4", "Pulsar <i>Scan</i> y esperar a que aparezca "
      "<code>ESP32-TALLER</code>."],
     ["5", "Tocar el nombre. La barra de arriba pasa a <i>Connected</i> y "
      "empiezan a llegar las líneas."]]))

A(sec("Qué debe observarse"))
A(p(
    "En el teléfono aparecen dos líneas cada dos segundos, con la temperatura "
    "y la humedad. Soplando sobre el sensor la humedad sube a la vista. En la "
    "consola de Thonny se ve lo mismo, más el aviso de cuando no hay nadie "
    "conectado.",

    "La aplicación también manda: escribiendo cualquier cosa en el campo de "
    "abajo, el texto aparece en la consola de la placa. Eso abre la puerta al "
    "ejercicio 3, donde el teléfono pasa de mirar a mandar.",

    "<b>La prueba que conviene hacer:</b> cerrar la aplicación con el programa "
    "corriendo. La consola empieza a avisar que no hay nadie. Volver a abrir y "
    "reconectar: sigue funcionando sin reiniciar la placa. Eso es lo que "
    "consigue el <code>_anunciar()</code> del evento de desconexión."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["La placa no aparece en la búsqueda",
      "Se está buscando en la pestaña de <b>Classic</b>. Tiene que ser la de "
      "<b>Bluetooth LE</b>."],
     ["No aparece ni en la pestaña LE",
      "Falta el permiso de ubicación de Android, o el programa se detuvo. "
      "En Thonny debe verse «Bluetooth activo»."],
     ["<code>ImportError: no module named 'ble_uart'</code>",
      "Falta copiar <code>ble_uart.py</code> <b>dentro de la placa</b>."],
     ["Conecta, llega una línea y se corta",
      "El mensaje pasa de veinte caracteres, o el programa se detuvo al "
      "fallar una lectura del sensor."],
     ["Se desconecta y ya no vuelve a aparecer",
      "El programa no se anuncia de nuevo al desconectarse. Es lo que "
      "resuelve el manejador de <code>_DESCONECTADO</code>."],
     ["<code>MemoryError</code> al arrancar",
      "BLE y WiFi encendidos a la vez consumen mucha memoria. Este "
      "laboratorio no necesita WiFi: no lo active."]]))

A(nota("Bluetooth o WiFi, no los dos porque sí", p(
    "El ESP32 puede tener las dos radios activas, pero comparten memoria y "
    "el margen es estrecho. Si un programa no necesita la red —y éste no la "
    "necesita— conviene dejar el WiFi apagado. Un <code>MemoryError</code> "
    "al arrancar suele ser eso y no un programa demasiado grande.")))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, es el diagnóstico en sitio: el "
    "técnico se para frente al tablero, abre la aplicación y lee lo que el "
    "equipo está midiendo, sin acceso a la red de planta ni permisos de "
    "informática. Con el medidor del laboratorio 6.5 se leen tensión y "
    "corriente delante del equipo.",
    "<b>En el área mecánica</b>, es exactamente lo que hace un lector de "
    "diagnóstico con el teléfono. La misma estructura —placa midiendo, "
    "teléfono recibiendo por BLE— con el termistor de refrigerante o el "
    "tacómetro del laboratorio 4.4 da un instrumento que se lee desde la "
    "butaca mientras otro maneja.")))

# =================================================================== 7.5
A(lab("7.5", "De placa a placa, sin red: ESP-NOW"))

A(sec("Objetivo"))
A(p("Que una placa dispare una alarma en otra, sin router, sin claves y sin "
    "internet."))

A(sec("Materiales"))
A(tabla(["Cantidad", "Componente", "Observación"],
        [["2", "Placas ESP32", "una transmisora y otra receptora"],
         ["1", "Pulsador", "en la transmisora"],
         ["1", "Zumbador <b>activo</b>", "en la receptora; aquí sí sirve"]],
        centradas=(0,)))

A(sec("El circuito"))

A(figura(CIR.svg("lab_7_4")[0], ancha=True, epigrafe=
         "Las dos placas, cada una con su componente. Entre ellas no hay "
         "cable ni router: sólo la radio.", capitulo=7))

A(aviso("ESP-NOW usa la radio del WiFi, no la red del WiFi", p(
    "Es la confusión más común. ESP-NOW necesita que la interfaz inalámbrica "
    "esté <b>encendida</b>, porque usa el mismo transmisor de radio, pero "
    "<b>no se conecta a ninguna red</b>. No hay router, no hay clave, no hay "
    "dirección IP. Por eso los programas hacen "
    "<code>wlan.active(True)</code> seguido de "
    "<code>wlan.disconnect()</code>: encienden la radio y se aseguran de no "
    "estar asociados a nada.",
    "La consecuencia práctica es que funciona donde no hay red: en una nave "
    "sin cobertura, entre dos máquinas, en un vehículo. Y que las dos placas "
    "deben compartir el mismo canal de radio, que es automático mientras "
    "ninguna esté conectada a una red.")))

A(sec("Razonamiento"))

A(p(
    "Cada placa tiene una dirección física única —su MAC— y el transmisor "
    "necesita la del receptor para dirigirle el mensaje. Ese es el único paso "
    "de configuración, y hay que hacerlo una vez: se ejecuta un programa corto "
    "en la receptora, se anota lo que imprime y se copia en la transmisora.",

    "Del lado del transmisor, el envío se dispara en el flanco del pulsador y "
    "con el filtro de rebote del laboratorio 2.3: sin él, un solo toque manda "
    "diez mensajes. Del lado del receptor, el zumbador debe sonar dos segundos "
    "<b>sin</b> que el programa deje de escuchar, de modo que en vez de una "
    "espera se anota el instante en que debe callarse. Es, otra vez, la idea "
    "del laboratorio 2.4."))

A(sec("Paso 1: averiguar la dirección de la receptora"))

A(codigo("""import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = wlan.config("mac")
print("MAC de esta placa:")
print("  legible  : " + ":".join("{:02X}".format(b) for b in mac))
print("  para el codigo del transmisor:")
escapada = "".join("\\\\x{:02x}".format(b) for b in mac)
print("    PAREJA = b'" + escapada + "'")""",
    archivo="lab_7_5_mac.py"))

A(consola("""MAC de esta placa:
  legible  : 3C:61:05:0A:1B:2C
  para el codigo del transmisor:
    PAREJA = b'\\x3c\\x61\\x05\\x0a\\x1b\\x2c'"""))

A(p("Esa última línea se copia tal cual en el programa del transmisor."))

A(sec("Paso 2: la placa transmisora"))

A(codigo("""import network
import espnow
from machine import Pin
import time

PAREJA = b'\\xbb\\xbb\\xbb\\xbb\\xbb\\xbb'   # <-- la MAC de la receptora
MENSAJE = b"alarma"
REBOTE_MS = 200

pulsador = Pin(4, Pin.IN, Pin.PULL_UP)

# La radio debe estar encendida, pero sin conectarse a ninguna red.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()

enlace = espnow.ESPNow()
enlace.active(True)
enlace.add_peer(PAREJA)

print("Transmisor listo. Pulse el boton.")

estaba_pulsado = False
ultimo_cambio = time.ticks_ms()

while True:
    ahora = time.ticks_ms()
    pulsado = not pulsador.value()

    hubo_cambio = pulsado != estaba_pulsado
    paso_el_rebote = time.ticks_diff(ahora, ultimo_cambio) > REBOTE_MS

    if hubo_cambio and paso_el_rebote:
        estaba_pulsado = pulsado
        ultimo_cambio = ahora

        if pulsado:
            # Se saca el aviso fuera del try para no anidar cuatro
            # niveles: a esa profundidad la linea ya no entra impresa.
            try:
                entregado = enlace.send(PAREJA, MENSAJE)
            except OSError as e:
                entregado = None
                print("No se pudo enviar:", e)

            if entregado:
                print("Mensaje entregado.")
            elif entregado is not None:
                print("Sin respuesta. Esta encendida la otra?")

    time.sleep_ms(10)""", archivo="lab_7_5_transmisor.py"))

A(sec("Paso 3: la placa receptora"))

A(codigo("""import network
import espnow
from machine import Pin
import time

MENSAJE = b"alarma"
DURACION_MS = 2000

buzzer = Pin(4, Pin.OUT)
buzzer.off()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()

enlace = espnow.ESPNow()
enlace.active(True)

print("Receptor listo. Esperando mensajes...")

callar_en = 0

while True:
    # Espera hasta 50 ms por un mensaje. Si no llega ninguno
    # devuelve None y el programa sigue: nunca queda bloqueado.
    quien, mensaje = enlace.recv(50)

    if mensaje == MENSAJE:
        origen = ":".join("{:02X}".format(b) for b in quien)
        print("Alarma recibida desde", origen)
        buzzer.on()
        callar_en = time.ticks_add(time.ticks_ms(), DURACION_MS)

    elif mensaje is not None:
        print("Mensaje desconocido:", mensaje)

    # El zumbador se calla por reloj, no por espera: mientras suena,
    # el programa sigue atendiendo mensajes.
    if callar_en and time.ticks_diff(time.ticks_ms(), callar_en) >= 0:
        buzzer.off()
        callar_en = 0""", archivo="lab_7_5_receptor.py"))

A(sec("Qué debe observarse"))
A(p(
    "Al pulsar en una placa, la otra suena dos segundos. La consola del "
    "transmisor confirma la entrega y la del receptor informa desde qué "
    "dirección llegó.",

    "Vale la pena hacer dos pruebas. La primera: apagar la receptora y pulsar. "
    "El transmisor avisa «Sin respuesta» — ESP-NOW confirma la entrega, cosa "
    "que el WiFi común no hace. La segunda: alejarse. En interiores el enlace "
    "aguanta bastante más que la red del taller, porque no hay router de por "
    "medio."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["«Sin respuesta» siempre",
      "La MAC copiada no es la de la receptora, o se copió la del formato "
      "legible en lugar de la línea con <code>\\\\x</code>."],
     ["Funcionaba y dejó de funcionar al agregar WiFi",
      "Una de las dos placas se conectó a una red y cambió de canal de radio. "
      "Las dos tienen que estar en el mismo."],
     ["Un toque dispara varias alarmas",
      "El filtro de rebote es corto para ese pulsador. Subir "
      "<code>REBOTE_MS</code>."],
     ["<code>ImportError: no module named 'espnow'</code>",
      "El firmware de MicroPython es anterior a la versión 1.19. Hay que "
      "actualizarlo."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el enlace entre dos tableros "
    "que no tienen red tendida entre ellos: un pulsador de paro de emergencia "
    "remoto, un aviso de nivel entre un tanque y la sala de bombas. La "
    "confirmación de entrega es lo que lo hace utilizable en seguridad: el "
    "transmisor sabe si su mensaje llegó.",
    "<b>En el área mecánica</b>, permite instrumentar un vehículo sin tender cables: "
    "un sensor en la rueda o en el motor manda a una placa en el tablero. Sin "
    "router, que en un vehículo en movimiento no existe.")))

A(ejercicios([
    "En el laboratorio 7.2, haga que la dirección <code>/datos</code> "
    "devuelva sólo las dos cifras separadas por una coma, sin HTML. ¿Para qué "
    "serviría una dirección así?",

    "El intervalo de medición está en <code>INTERVALO_MS</code> y el de "
    "refresco de la página en la etiqueta <code>meta</code>. ¿Qué pasa si el "
    "refresco es más rápido que la medición? ¿Y al revés? Justifique cuál de "
    "los dos conviene que sea mayor.",

    "Dos personas abren la página al mismo tiempo. ¿Ven exactamente la misma "
    "cifra? Explique por qué, mirando dónde se guarda la medición.",

    "En el laboratorio 7.5, haga que el transmisor mande la cuenta de "
    "pulsaciones en lugar de la palabra fija, y que el receptor la muestre.",

    "Agregue una tercera placa al montaje de ESP-NOW, de modo que el mensaje "
    "llegue a las dos receptoras. Ayuda: mire qué acepta "
    "<code>add_peer</code> y qué significa la dirección de difusión "
    "<code>b'\\\\xff' * 6</code>.",

    "Compare las cuatro rutas del cuadro de apertura para este caso: un "
    "sensor de nivel en un tanque a 80 metros del tablero, en un galpón sin "
    "cobertura de WiFi. ¿Cuál elegiría y por qué?",
]))

# =================================================================== 7.6
A(lab("7.6", "Publicar en internet: MQTT y Adafruit IO"))

A(sec("Objetivo"))
A(p("Que la medición salga de la red del taller y quede guardada, de modo "
    "que se pueda mirar desde cualquier parte y consultar el histórico."))

A(sec("El circuito"))
A(p("El mismo del laboratorio 7.2, sin cambios (figura 7.2)."))

A(sec("Razonamiento"))

A(p(
    "El servidor web del laboratorio 7.2 tiene dos límites de fondo. Sólo "
    "alcanza dentro de la misma red —para verlo desde afuera habría que abrir "
    "puertos en el router, que en una empresa nadie va a autorizar—, y no "
    "guarda nada: muestra el valor de ahora y lo de hace una hora se perdió.",

    "<b>MQTT</b> resuelve las dos cosas invirtiendo quién llama a quién. En "
    "vez de esperar visitas, la placa <b>publica</b>: se conecta a un servidor "
    "de internet —el <i>broker</i>— y le manda el dato. Como es la placa la "
    "que sale, el router de la empresa lo permite sin configurar nada. El "
    "broker lo guarda y se lo entrega a quien lo pida.",

    "Cada magnitud va a su propio <b>tópico</b>, que es simplemente un nombre. "
    "En Adafruit IO los tópicos se llaman <i>feeds</i> y se nombran con el "
    "usuario adelante:"))

A(codigo("""su_usuario/feeds/temperatura
su_usuario/feeds/humedad"""))

A(p("Los feeds hay que crearlos primero desde la página de la cuenta. Si se "
    "publica en un feed que no existe, el broker acepta la conexión y "
    "descarta el dato sin avisar."))

A(aviso("El límite que explica los avisos de «throttle»", p(
    "La cuenta gratuita de Adafruit IO admite <b>30 datos por minuto</b>, "
    "contando todos los feeds juntos. Pasado ese número, el servidor empieza "
    "a rechazar publicaciones y manda avisos de <i>throttle</i>; si se insiste, "
    "corta la conexión por un rato.",
    "La cuenta es directa. Con <i>n</i> feeds publicando cada <i>t</i> "
    "segundos:  <code>n × 60 / t ≤ 30</code>. Con dos feeds hacen falta al "
    "menos 4 segundos entre publicaciones; con cuatro feeds —tensión, "
    "corriente, potencia y factor de potencia— hacen falta <b>8</b>, y a 8 "
    "segundos exactos se está justo en el techo, de modo que cualquier "
    "reintento lo pasa. Por eso este libro publica cada <b>15 segundos</b>: "
    "deja margen y para una magnitud física es de sobra.")))

A(nota("umqtt.robust, no umqtt.simple", p(
    "Las dos bibliotecas hacen lo mismo, pero <code>umqtt.robust</code> "
    "reintenta sola cuando la conexión se corta, que en una red inalámbrica "
    "pasa. Con <code>umqtt.simple</code> hay que escribir esa lógica a mano. "
    "Aun así el programa atrapa el error al publicar y vuelve a conectarse: un "
    "equipo que tiene que quedar corriendo semanas no puede detenerse porque "
    "el router se reinició una noche.")))

A(sec("El módulo compartido, ampliado"))

A(p("Al <code>iot.py</code> del laboratorio 7.1 se le agregan dos funciones. "
    "Van abajo del todo, y siguen sin contener ninguna clave: la leen de "
    "<code>config.py</code>. El módulo completo, que es el que hay que "
    "tener copiado en la placa de aquí en adelante, queda así:"))

A(codigo("""# iot.py — conexion a la red, compartida por todo el capitulo
import time
import network
from umqtt.robust import MQTTClient
import config

SERVIDOR = "io.adafruit.com"
PUERTO = 1883


def conectar_wifi(intentos=20):
    \"\"\"Conecta el ESP32 a la red. Devuelve la direccion IP.\"\"\"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando a la red", config.WIFI_SSID, "...")
        wlan.connect(config.WIFI_SSID, config.WIFI_CLAVE)
        for _ in range(intentos * 2):
            if wlan.isconnected():
                break
            time.sleep(0.5)

    if not wlan.isconnected():
        raise OSError("No se pudo conectar. Revise config.py")

    ip = wlan.ifconfig()[0]
    print("Red conectada. IP:", ip)
    return ip


def conectar_adafruit(identificador):
    \"\"\"Abre la sesion MQTT con Adafruit IO. Devuelve el cliente.\"\"\"
    cliente = MQTTClient(client_id=identificador,
                         server=SERVIDOR,
                         port=PUERTO,
                         user=config.AIO_USUARIO,
                         password=config.AIO_CLAVE,
                         keepalive=60)
    cliente.connect()
    print("Conectado a Adafruit IO como", config.AIO_USUARIO)
    return cliente


def feed(nombre):
    \"\"\"Devuelve el topico MQTT que corresponde a un feed.\"\"\"
    return "{}/feeds/{}".format(config.AIO_USUARIO, nombre)""",
    archivo="iot.py"))

A(sec("Programa"))

A(codigo("""from machine import Pin
import time
import dht
import iot

PIN_DATOS = 14
INTERVALO = 15            # segundos. Ver el recuadro del limite.

sensor = dht.DHT11(Pin(PIN_DATOS))
TEMA_TEMP = iot.feed("temperatura")
TEMA_HUM = iot.feed("humedad")


def leer_sensor():
    \"\"\"Temperatura y humedad, o None si la trama falla.\"\"\"
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError:
        return None


def main():
    iot.conectar_wifi()
    cliente = iot.conectar_adafruit("esp32_dht11")
    fallas = 0

    while True:
        lectura = leer_sensor()

        if lectura is None:
            fallas = fallas + 1
            print("Lectura fallida ({}). Se reintenta.".format(fallas))
        else:
            temperatura, humedad = lectura
            fallas = 0
            print("Temperatura: {} C   Humedad: {} %".format(
                temperatura, humedad))
            try:
                cliente.publish(TEMA_TEMP, str(temperatura))
                cliente.publish(TEMA_HUM, str(humedad))
            except Exception as e:
                # La conexion se cayo. Se vuelve a abrir en vez de
                # detener el programa: un equipo que queda corriendo
                # semanas no puede pararse porque se reinicio el router.
                print("No se pudo publicar:", e)
                cliente = iot.conectar_adafruit("esp32_dht11")

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()""", archivo="lab_7_6_mqtt.py"))

A(sec("Qué debe observarse"))
A(p(
    "En el panel de Adafruit IO los dos feeds se van llenando cada quince "
    "segundos, y el gráfico muestra la evolución. Cerrando el navegador y "
    "volviendo al día siguiente, el histórico sigue ahí: eso es lo que el "
    "servidor web no podía hacer.",

    "Vale la pena una prueba: apagar el WiFi del router un minuto y volver a "
    "encenderlo. El programa avisa que no pudo publicar, se reconecta solo y "
    "sigue. En el gráfico queda un hueco, no una interrupción del equipo."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Conecta pero el feed queda vacío",
      "El feed no existe en la cuenta, o el nombre está escrito distinto. Se "
      "descarta el dato sin avisar."],
     ["Avisos de <i>throttle</i> y después se corta",
      "Se pasó de 30 datos por minuto. Subir <code>INTERVALO</code>."],
     ["<code>MQTTException: 5</code>",
      "Usuario o clave equivocados. La clave es la del servicio, no la de la "
      "cuenta de correo."],
     ["Publica un rato y se detiene",
      "Se está usando <code>umqtt.simple</code>, o falta el "
      "<code>try</code> alrededor de <code>publish</code>."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el monitoreo de consumo de un "
    "tablero, con el medidor del laboratorio 6.5 en lugar del DHT11: tensión, "
    "corriente, potencia y factor de potencia publicados a un panel que "
    "gerencia mira desde su oficina. Ahí el límite de 30 datos por minuto deja "
    "de ser un detalle: son cuatro feeds.",
    "<b>En el área mecánica</b>, es la telemetría de un vehículo de flota. La "
    "temperatura del motor y las revoluciones —laboratorio 4.4— publicadas "
    "mientras el vehículo circula, usando el teléfono como punto de acceso.")))

# =================================================================== 7.7
A(lab("7.7", "Un tablero propio: InfluxDB y Grafana"))

A(sec("Objetivo"))
A(p("Guardar el histórico en un servidor del propio taller, sin límite de "
    "datos por minuto y sin depender de ninguna cuenta de internet."))

A(sec("Razonamiento"))

A(p(
    "Adafruit IO resuelve el laboratorio anterior con muy poco trabajo, pero "
    "impone tres condiciones: un tope de datos por minuto, un histórico corto "
    "en la cuenta gratuita, y que los datos del taller vivan en un servidor "
    "ajeno. Para un ensayo de aula está bien; para instrumentar una máquina "
    "durante un semestre, no.",

    "La alternativa es montar el servidor en la propia red. Son dos programas "
    "que corren en cualquier computadora del taller: <b>InfluxDB</b>, que es "
    "una base de datos pensada para valores con fecha y hora, y "
    "<b>Grafana</b>, que dibuja los tableros. Los dos son gratuitos y no "
    "necesitan internet: basta con que la placa y la computadora estén en la "
    "misma red.",

    "Del lado del ESP32 el cambio es menor de lo que parece. En vez de "
    "publicar por MQTT, se manda una petición HTTP con el dato. InfluxDB "
    "acepta un formato de texto muy simple, de una sola línea:"))

A(codigo("""ambiente temperatura=23.4,humedad=55.0
   |         |                  |
   |         |                  +-- otro campo, separado por coma
   |         +-- nombre del campo y su valor
   +-- nombre de la medicion"""))

A(sec("Preparar el servidor"))

A(tabla(
    ["Paso", "Qué hacer"],
    [["1", "Instalar InfluxDB y Grafana en una computadora del taller. Los "
      "dos traen instalador para Windows y para Linux."],
     ["2", "En InfluxDB, crear una organización (por ejemplo <code>taller"
      "</code>), un <i>bucket</i> (<code>sensores</code>) y un <b>token</b> "
      "de escritura. El token va a <code>config.py</code>, no al programa."],
     ["3", "Anotar la dirección de esa computadora en la red. Es la que el "
      "ESP32 va a usar, y conviene fijarla en el router para que no cambie."],
     ["4", "En Grafana, agregar InfluxDB como origen de datos y crear un "
      "panel sobre el bucket <code>sensores</code>."]]))

A(aviso("La dirección no es «localhost»", p(
    "Desde la computadora donde corre InfluxDB, el servidor se ve en "
    "<code>localhost</code>. Desde el ESP32 <b>no</b>: hay que poner la "
    "dirección de esa computadora en la red, la que empieza con "
    "<code>192.168.</code>. Es el tropiezo más frecuente de este laboratorio, "
    "y el síntoma es un error de conexión que no dice nada útil.",
    "El otro tropiezo es el cortafuegos de Windows, que bloquea el puerto "
    "<code>8086</code> hasta que se le autoriza.")))

A(sec("Programa"))

A(codigo("""import time
from machine import Pin
import urequests
import dht
import iot
import config

PIN_DATOS = 14
INTERVALO = 10            # aqui no hay limite de datos por minuto

sensor = dht.DHT11(Pin(PIN_DATOS))

URL = "http://{}:8086/api/v2/write?org={}&bucket={}&precision=s".format(
    config.INFLUX_HOST, config.INFLUX_ORG, config.INFLUX_BUCKET)

CABECERAS = {"Authorization": "Token " + config.INFLUX_TOKEN,
             "Content-Type": "text/plain"}


def escribir(temperatura, humedad):
    \"\"\"Manda una linea a InfluxDB. Devuelve True si la acepto.

    La respuesta se cierra SIEMPRE. En MicroPython una respuesta sin
    cerrar deja el socket tomado, y despues de unas cuantas el
    programa se queda sin ninguno y deja de poder publicar.
    \"\"\"
    linea = "ambiente temperatura={},humedad={}".format(
        temperatura, humedad)
    respuesta = None
    try:
        respuesta = urequests.post(URL, data=linea, headers=CABECERAS)
        return respuesta.status_code in (200, 204)
    except OSError as e:
        print("No se pudo escribir:", e)
        return False
    finally:
        if respuesta is not None:
            respuesta.close()


def main():
    iot.conectar_wifi()
    print("Escribiendo en", URL)

    while True:
        try:
            sensor.measure()
            temperatura = sensor.temperature()
            humedad = sensor.humidity()
        except OSError:
            print("Lectura fallida. Se reintenta.")
            time.sleep(INTERVALO)
            continue

        if escribir(temperatura, humedad):
            print("{} C   {} %   anotado".format(temperatura, humedad))
        else:
            print("{} C   {} %   NO se pudo anotar".format(
                temperatura, humedad))

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()""", archivo="lab_7_7_influx.py"))

A(nota("El finally no es adorno", p(
    "Es la diferencia entre un programa que corre un mes y uno que se detiene "
    "a la media hora. Cada <code>urequests.post</code> abre un socket, y "
    "MicroPython tiene muy pocos: si la respuesta no se cierra —y con un "
    "<code>return</code> de por medio es facilísimo olvidarlo— se agotan. El "
    "<code>finally</code> garantiza el cierre haya salido bien, mal o por "
    "excepción.")))

A(sec("Qué debe observarse"))
A(p(
    "La consola escribe «anotado» cada diez segundos, y el panel de Grafana "
    "dibuja la curva en tiempo real. Dejándolo toda la noche, a la mañana "
    "siguiente está el registro completo: es lo que no daban ni el servidor "
    "web ni la cuenta gratuita."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Error de conexión inmediato",
      "La dirección es <code>localhost</code> en lugar de la de la red, o el "
      "cortafuegos bloquea el puerto 8086."],
     ["Contesta 401",
      "El token es incorrecto, o falta la palabra <code>Token</code> delante "
      "en la cabecera."],
     ["Contesta 400",
      "La línea está mal formada. Los espacios importan: uno solo entre el "
      "nombre de la medición y los campos, y ninguno alrededor del igual."],
     ["Anota un rato y deja de anotar",
      "Falta cerrar la respuesta. Es el caso del recuadro anterior."],
     ["Grafana no muestra nada y no hay error",
      "El rango de tiempo del panel es anterior a los datos. Ponerlo en los "
      "últimos quince minutos."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, éste es el registrador de una planta: "
    "consumo, temperaturas y presiones guardados en un servidor propio, con "
    "los datos dentro de la empresa y sin cuota mensual. Es la base de "
    "cualquier estudio de eficiencia energética, que necesita meses de "
    "registro y no unos minutos.",
    "<b>En el área mecánica</b>, es el banco de pruebas instrumentado: se deja "
    "corriendo un ensayo de varias horas y después se comparan las curvas de "
    "temperatura y revoluciones. Con el límite de una cuenta gratuita ese "
    "ensayo no se puede registrar.")))

# =================================================================== 7.8
A(lab("7.8", "Una página que manda, no que informa"))

A(sec("Objetivo"))
A(p("Encender y apagar desde el navegador el relé del laboratorio 2.5, sin "
    "cuenta, sin servidor y sin salir de la red del taller."))

A(sec("Razonamiento"))

A(p(
    "Los siete laboratorios anteriores mandan datos hacia afuera. Éste va en "
    "sentido contrario, y el cambio de sentido trae problemas propios que la "
    "publicación no tiene.",

    "Cuando un programa informa, un dato perdido cuesta poco: se manda el "
    "siguiente. Cuando un programa obedece, una orden perdida —o peor, una "
    "orden entendida al revés— deja algo encendido que tenía que quedar "
    "apagado. Por eso este laboratorio se arma sobre el relé del 2.5 y hereda "
    "sus reglas: <b>arranca apagado</b>, y la constante del puente H/L sigue "
    "siendo la única línea donde aparece un nivel.",

    "El servidor es el del laboratorio 7.2 con dos diferencias. La página trae "
    "dos botones en lugar de dos números, y el programa mira <b>qué</b> se "
    "pidió antes de contestar. Esa segunda diferencia parece trivial y es la "
    "que se lleva la tarde entera."))

A(aviso("Mirar la petición entera es lo que rompe el botón de apagar", p(
    "La manera natural de escribirlo es preguntar si la petición contiene "
    "<code>/on</code> o <code>/off</code>, y así es como sale la primera vez. "
    "Funciona, y al rato el botón de apagar deja de apagar.",

    "La causa no está en el programa sino en el navegador. Al pulsar ENCENDER, "
    "la página que vuelve queda en la dirección <code>http://ip/on</code>; al "
    "pulsar APAGAR desde ahí, el navegador agrega una cabecera "
    "<code>Referer: http://ip/on</code> para avisar de dónde viene. Esa "
    "cabecera viaja dentro de la misma petición, de modo que buscar "
    "<code>/on</code> en el texto completo la encuentra, se cumple la primera "
    "rama y el relé se enciende otra vez.",

    "El síntoma es de los peores que puede tener un montaje: un foco de 220 V "
    "que no se apaga con el botón de apagar, y que sí se apaga si se abre una "
    "pestaña nueva, porque ahí todavía no hay <code>Referer</code>. La causa "
    "es una sola línea: hay que leer <b>la línea del pedido</b> y no la "
    "petición completa.")))

A(p(
    "Ese es justamente el trabajo de <code>camino_pedido()</code>, que el "
    "laboratorio 7.2 ya usaba para descartar el pedido del icono. Una petición "
    "empieza siempre así:"))

A(consola("""GET /off HTTP/1.1
Host: 192.168.0.42
Referer: http://192.168.0.42/on
Connection: keep-alive"""))

A(p(
    "La primera línea es el pedido; el resto son cabeceras que el navegador "
    "agrega por su cuenta y sobre las que el programa no tiene ningún control. "
    "Quedarse con la primera línea y partirla por espacios da "
    "<code>/off</code> y nada más."))

A(sec("El circuito"))
A(p(
    "El del laboratorio 2.5, sin un solo cambio: el módulo de relé en "
    "<code>GPIO19</code>, con su fuente y su masa común. El pulsador puede "
    "quedar puesto —no molesta— pero este programa no lo lee."))

A(sec("Programa"))

A(codigo(r'''import socket
import iot
from machine import Pin

PUERTO = 80
PIN_RELE = 19
ACTIVO_EN_BAJO = True         # el puente H/L del modulo, como en el 2.5

rele = Pin(PIN_RELE, Pin.OUT)
encendido = False


def mandar(estado):
    """Traduce el estado al nivel que pide este modulo."""
    global encendido
    encendido = estado
    if ACTIVO_EN_BAJO:
        rele.value(0 if estado else 1)
    else:
        rele.value(1 if estado else 0)


def camino_pedido(peticion):
    """El camino de la PRIMERA linea: GET /algo HTTP/1.1

    Buscar "/on" en la peticion entera parece lo mismo y no lo es: el
    navegador agrega una cabecera Referer con la direccion anterior, y
    ahi aparece el "/on" de la visita previa. El boton de apagar deja
    de apagar.
    """
    try:
        return peticion.split("\r\n")[0].split(" ")[1]
    except IndexError:
        return "/"


def pagina():
    estado = "ENCENDIDO" if encendido else "APAGADO"
    color = "#1B7A3D" if encendido else "#8A8F98"
    return PLANTILLA.format(color=color, estado=estado)


PLANTILLA = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Control del rele</title>
<style>
 body {{ font-family: sans-serif; text-align: center; margin-top: 8vh }}
 .estado {{ font-size: 2em; color: {color}; margin-bottom: 0.6em; }}
 a {{ text-decoration: none; }}
 button {{ font-size: 1.8em; padding: 0.6em 1.4em; margin: 0.4em;
           border: none; border-radius: 12px; color: white; }}
 .on {{ background: #1B7A3D; }}  .off {{ background: #9B2C2C; }}
</style></head><body>
<h2>Control del rele</h2>
<p class="estado">{estado}</p>
<a href="/on"><button class="on">ENCENDER</button></a>
<a href="/off"><button class="off">APAGAR</button></a>
</body></html>
"""


def main():
    mandar(False)              # apagado antes de abrir la red a nadie
    ip = iot.conectar_wifi()

    servidor = socket.socket()
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(socket.getaddrinfo("0.0.0.0", PUERTO)[0][-1])
    servidor.listen(2)

    print("Abra http://{}/ en el telefono o el navegador.".format(ip))

    while True:
        cliente, direccion = servidor.accept()
        try:
            cliente.settimeout(3)
            peticion = cliente.recv(1024).decode()
            camino = camino_pedido(peticion)

            if camino == "/favicon.ico":
                cliente.sendall(b"HTTP/1.0 404 Not Found\r\n\r\n")
            else:
                if camino == "/on":
                    mandar(True)
                    print("orden desde", direccion[0], "-> encender")
                elif camino == "/off":
                    mandar(False)
                    print("orden desde", direccion[0], "-> apagar")

                cliente.sendall(b"HTTP/1.0 200 OK\r\n"
                                b"Content-Type: text/html\r\n\r\n")
                cliente.sendall(pagina().encode())
        except OSError as e:
            print("Visita interrumpida:", e)
        finally:
            cliente.close()


if __name__ == "__main__":
    main()''', archivo="lab_7_8_pagina_que_manda.py"))

A(nota("Por qué la página muestra el estado", p(
    "Los dos botones solos no alcanzan. Quien abre la página desde otro "
    "teléfono no sabe si el foco está encendido, y si pulsa ENCENDER sobre "
    "algo que ya lo está no pasa nada visible, lo que invita a pulsar otra "
    "vez, y otra.",
    "Mostrar el estado convierte la página en un <b>reflejo</b> de lo que pasa "
    "en la placa y no sólo en un juego de botones. Es la diferencia entre un "
    "mando y un tablero, y en el laboratorio siguiente se vuelve "
    "indispensable: cuando la orden puede venir de varios lados, cada lado "
    "tiene que poder enterarse de lo que hicieron los demás.")))

A(sec("Qué debe observarse"))
A(p(
    "Al abrir la dirección aparece la página con el estado en APAGADO. "
    "ENCENDER hace chasquear el relé y el estado pasa a ENCENDIDO; APAGAR lo "
    "devuelve. La consola escribe una línea por orden, con la dirección de "
    "quien la mandó.",

    "La prueba que hay que hacer, y que es el motivo del laboratorio: pulsar "
    "ENCENDER y después APAGAR <b>en la misma pestaña</b>, varias veces "
    "seguidas. Con el programa de arriba apaga siempre. Con la versión que "
    "busca en la petición entera, la segunda vez ya no."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["El botón de apagar no apaga, salvo en pestaña nueva",
      "Se está buscando <code>/on</code> en toda la petición y lo encuentra "
      "en la cabecera <code>Referer</code>. Ver el recuadro."],
     ["El relé se enciende solo al arrancar el programa",
      "El módulo es activo en bajo y el pin queda en 0 antes de que el "
      "programa mande nada. Por eso <code>mandar(False)</code> va primero, "
      "incluso antes de conectar la red."],
     ["La página abre pero el relé no responde",
      "El problema es del laboratorio 2.5, no de éste: masa común o tensión "
      "de bobina."],
     ["Desde el teléfono no abre",
      "El teléfono está en otra red, o en datos móviles. Tiene que estar en "
      "la misma red inalámbrica que la placa."],
     ["Anda un rato y deja de responder",
      "La placa perdió la red. Este servidor no reconecta solo; el "
      "laboratorio siguiente sí."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, es el mando local de una "
    "máquina desde el teléfono, sin cablear una botonera: arranque y parada de "
    "una bomba, de un extractor, del alumbrado de un galpón. Y la lección del "
    "<code>Referer</code> vale igual en cualquier interfaz: no decidir sobre "
    "el texto completo de un mensaje, sino sobre el campo que corresponde.",
    "<b>En el área mecánica</b>, es el banco de pruebas gobernado desde el "
    "celular mientras se está debajo del vehículo: activar el "
    "electroventilador, la bomba de combustible o el precalentador sin volver "
    "a la cabina. El relé es el mismo que el vehículo trae de fábrica.")))

# =================================================================== 7.9
A(lab("7.9", "El botón del tablero: suscribirse en lugar de publicar"))

A(sec("Objetivo"))
A(p("Gobernar el mismo relé desde el tablero de Adafruit IO, de modo que la "
    "orden llegue desde cualquier lugar con internet y no sólo desde la red "
    "del taller."))

A(sec("Razonamiento"))

A(p(
    "El laboratorio 7.6 publica: la placa abre la conexión, manda el dato y "
    "sigue con lo suyo. La comunicación la empieza siempre ella.",

    "Recibir una orden no puede funcionar así. La placa no sabe cuándo alguien "
    "va a pulsar el botón del tablero, y preguntar cada segundo «¿hay algo "
    "para mí?» es justamente lo que MQTT vino a evitar. Lo que se hace es al "
    "revés: la placa <b>se suscribe</b> a un feed y le deja al servidor el "
    "trabajo de avisarle. Mientras no pase nada, no viaja nada.",

    "En el programa eso son tres piezas que no aparecían en el 7.6. Una "
    "<b>función de atención</b>, que es la que el cliente llama cuando llega "
    "un mensaje. La <b>suscripción</b>, que declara a qué feed. Y una llamada "
    "a <code>check_msg()</code> dentro de la repetición, que es la que le da "
    "al cliente la oportunidad de revisar si llegó algo y disparar la "
    "atención. Sin esa tercera línea las otras dos no sirven de nada, y es el "
    "olvido más frecuente."))

A(nota("El feed y el bloque del tablero", p(
    "Hace falta un feed nuevo —este libro lo llama <code>foco</code>— y un "
    "bloque de tipo <b>interruptor</b> (<i>toggle</i>) conectado a él. En la "
    "configuración del bloque hay dos casillas con los valores que manda: "
    "convienen <code>1</code> y <code>0</code>, que es lo que el programa "
    "espera.",
    "El anexo A explica cómo se crean los feeds y los bloques. Y conviene "
    "recordar el otro límite de la cuenta gratuita: son <b>cinco feeds</b> en "
    "total, y éste ocupa uno.")))

A(aviso("Un botón en internet enciende algo de verdad", p(
    "Hasta aquí una orden equivocada encendía un LED. Ahora enciende una carga "
    "de 220 V, y el botón está en una página a la que se llega desde cualquier "
    "parte del mundo con el usuario y la clave de la cuenta.",
    "De ahí dos cosas. La clave de Adafruit IO deja de ser una molestia "
    "administrativa y pasa a ser la llave de algo físico: si se publicó alguna "
    "vez, regenérela desde la llave amarilla antes de armar este laboratorio. "
    "Y la carga que se conecte tiene que ser una que no importe que quede "
    "encendida sola: un foco, sí; una estufa o un motor, no.")))

A(sec("Programa"))

A(p(
    "Al <code>iot.py</code> del laboratorio 7.6 no hay que agregarle nada: "
    "<code>conectar_adafruit()</code> y <code>feed()</code> ya alcanzan."))

A(codigo(r'''import time
import iot
from machine import Pin

PIN_RELE = 19
ACTIVO_EN_BAJO = True         # el puente H/L del modulo, como en el 2.5
FEED = "foco"
PING_MS = 30000                # la mitad del keepalive de iot.py

rele = Pin(PIN_RELE, Pin.OUT)
encendido = False


def mandar(estado):
    global encendido
    encendido = estado
    if ACTIVO_EN_BAJO:
        rele.value(0 if estado else 1)
    else:
        rele.value(1 if estado else 0)
    print("rele", "encendido" if estado else "apagado")


def atender(topico, mensaje):
    """La llama el cliente MQTT cuando llega algo del feed.

    Los dos argumentos vienen en bytes y no en texto. Y el valor que
    manda el bloque interruptor es "1" o "0" segun como se lo haya
    configurado: cualquier otra cosa se ignora en lugar de darla por
    buena, que con una carga de 220 V no es lo mismo.
    """
    orden = mensaje.decode().strip()
    if orden == "1":
        mandar(True)
    elif orden == "0":
        mandar(False)
    else:
        print("orden desconocida, se ignora:", orden)


def main():
    mandar(False)              # apagado antes de escuchar a nadie
    iot.conectar_wifi()

    cliente = iot.conectar_adafruit("esp32-rele")
    cliente.set_callback(atender)
    cliente.subscribe(iot.feed(FEED))

    # Adafruit guarda el ultimo valor de cada feed. Pidiendolo al
    # arrancar, la placa se entera de como quedo el interruptor la
    # vez anterior en lugar de esperar a que alguien lo toque.
    cliente.subscribe(iot.feed(FEED) + "/get")
    cliente.publish(iot.feed(FEED) + "/get", "")

    print("Escuchando el feed", FEED)
    ultimo_ping = time.ticks_ms()

    while True:
        # Sin esta linea la suscripcion no sirve de nada: es aqui
        # donde el cliente mira si llego algo y llama a atender().
        cliente.check_msg()

        # Si no viaja nada durante el keepalive, el servidor da la
        # sesion por muerta y corta. El ping la mantiene viva.
        if time.ticks_diff(time.ticks_ms(), ultimo_ping) > PING_MS:
            cliente.ping()
            ultimo_ping = time.ticks_ms()

        time.sleep_ms(200)


if __name__ == "__main__":
    main()''', archivo="lab_7_9_boton_adafruit.py"))

A(nota("Por qué hace falta el ping", p(
    "Publicar mantiene viva la conexión sin que uno se entere: cada dato que "
    "sale es tráfico. Un programa que sólo escucha no manda nada, y al cabo "
    "del <code>keepalive</code> —sesenta segundos, en el módulo del "
    "laboratorio 7.6— el servidor da la sesión por perdida y la cierra. La "
    "placa se queda escuchando un feed al que ya no está suscrita, sin ningún "
    "aviso.",
    "El <code>ping()</code> cada treinta segundos es lo que lo evita: la mitad "
    "del <i>keepalive</i>, que es la regla habitual. Es la falla más "
    "desconcertante de este laboratorio, porque el programa funciona el primer "
    "minuto y después deja de obedecer sin escribir un solo error.")))

A(sec("Qué debe observarse"))
A(p(
    "Al arrancar, la consola escribe el estado que tenía el interruptor la vez "
    "anterior: eso es el mensaje retenido llegando. Desde ahí, cada vez que se "
    "mueve el interruptor del tablero el relé chasquea en menos de un segundo, "
    "esté el tablero abierto en la computadora del taller o en el teléfono con "
    "datos móviles.",

    "La prueba que muestra de qué se trata el laboratorio: dejar el tablero "
    "abierto en dos dispositivos a la vez. Al mover el interruptor en uno, el "
    "otro se actualiza solo. Ninguno de los dos habla con la placa: los tres "
    "hablan con el feed."))

A(sec("Si algo no sale"))
A(tabla(
    ["Síntoma", "Causa habitual"],
    [["Conecta pero el relé nunca se mueve",
      "Falta <code>check_msg()</code> dentro de la repetición, o la "
      "suscripción usa un nombre de feed distinto del que tiene el bloque."],
     ["Obedece un minuto y después no",
      "Falta el <code>ping()</code>. Ver la nota."],
     ["<code>MQTTException: 5</code>",
      "Usuario o clave mal copiados en <code>config.py</code>. La clave es la "
      "de la llave amarilla, no la contraseña de ingreso."],
     ["El bloque manda ON y OFF en lugar de 1 y 0",
      "Es la configuración del bloque interruptor. Cambiar los dos valores "
      "allí, o aceptar <code>ON</code> y <code>OFF</code> en "
      "<code>atender()</code>."],
     ["Al arrancar no recupera el estado anterior",
      "Falta la suscripción al tópico terminado en <code>/get</code>, o la "
      "publicación vacía que la dispara."]]))

A(otra_carrera(p(
    "<b>En el área eléctrica y electrónica</b>, es el telemando de una "
    "instalación sin ir hasta ella: el riego de un invernadero, la bomba de un "
    "tanque elevado, el alumbrado de un playón. Y con el 7.6 publicando la "
    "medición y éste recibiendo la orden, el lazo se cierra: la misma cuenta "
    "muestra el nivel del tanque y enciende la bomba.",
    "<b>En el área mecánica</b>, es el precalentador o el bloqueo remoto de la "
    "bomba de combustible, que es como funciona un corte antirrobo comercial. "
    "Conviene mirarlo con ojo crítico: lo que en este laboratorio es un foco, "
    "ahí es un vehículo, y la clave de la cuenta es todo lo que separa al "
    "dueño de cualquier otro.")))

A(ejercicios([
    "Calcule cada cuántos segundos puede publicar un equipo con seis feeds en "
    "una cuenta gratuita de Adafruit IO. ¿Y con diez?",

    "Modifique el laboratorio 7.6 para que publique sólo cuando la medición "
    "cambió respecto de la anterior. ¿Cuántos datos por minuto ahorra en un "
    "ambiente estable? ¿Qué se pierde?",

    "En el laboratorio 7.7, agregue una etiqueta a la línea de InfluxDB "
    "—<code>ambiente,lugar=taller temperatura=23.4</code>— y úsela en Grafana "
    "para distinguir dos placas en el mismo panel.",

    "Escriba una tabla comparando las cuatro rutas del capítulo según: alcance, "
    "histórico, dependencias, costo y qué pasa si se cae internet.",

    "Un ensayo de motor de seis horas registrando cuatro magnitudes cada "
    "segundo. ¿Cuántos datos son? ¿Cuál de las cuatro rutas lo soporta?",

    "Tome el tablero local del laboratorio 6.6 y agréguele la publicación de "
    "este capítulo. Debería ser una cuarta responsabilidad junto a leer, "
    "decidir y mostrar, sin tocar las otras tres. Si tuvo que tocarlas, "
    "¿dónde estaba mal separado el programa original?",

    "Escriba la versión equivocada del laboratorio 7.8 —la que busca "
    "<code>/on</code> en la petición entera— y compruebe el error con el "
    "navegador. Después abra una pestaña nueva y pulse APAGAR. Explique por "
    "qué ahí sí funciona.",

    "Al laboratorio 7.8 agréguele una dirección <code>/estado</code> que "
    "devuelva sólo <code>1</code> o <code>0</code>, sin HTML. ¿Qué podría "
    "hacer otra placa con esa dirección?",

    "Junte los laboratorios 7.6 y 7.9 en un solo programa: que publique la "
    "temperatura y además obedezca al interruptor. Cuide que la publicación "
    "no deje de atender los mensajes que llegan, y diga en qué parte del "
    "programa estaba el riesgo.",

    "El laboratorio 7.9 hace <code>ping()</code> cada 30 s con un "
    "<i>keepalive</i> de 60. ¿Qué pasaría con 90 s? ¿Y con 1 s? Justifique "
    "los dos extremos.",
]))
