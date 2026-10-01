# -*- coding: utf-8 -*-
"""Verificacion del capitulo 7, sobre los programas tal como salen impresos.

Los dos servidores web se prueban de verdad: el modulo socket de
MicroPython y el de Python se usan igual, asi que el servidor se
levanta aqui mismo y se lo visita como lo haria un navegador.
El enlace ESP-NOW se prueba haciendo correr las dos placas.
"""
import sys, os, io, signal, contextlib, importlib.util
import threading, time, urllib.request, urllib.error

# --- la raiz del proyecto es la carpeta que contiene programas/.
# Asi estos archivos funcionan igual estando en la raiz o dentro de
# libro/, y se los puede ejecutar desde donde sea.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = _AQUI if os.path.isdir(os.path.join(_AQUI, "programas")) \
    else os.path.dirname(_AQUI)
os.chdir(_RAIZ)
sys.path.insert(0, _AQUI)
sys.path.insert(0, _RAIZ)
sys.path.insert(0, os.path.join(_RAIZ, "programas"))

# El repositorio no lleva config.py —ahi van las claves de cada uno— y
# estas comprobaciones no se conectan a ninguna red: si falta, se usa
# config_ejemplo.py, que trae los mismos nombres con valores de relleno.
try:
    import config
except ImportError:
    import config_ejemplo as config
    sys.modules["config"] = config
import sim.micropython
import dht

fallas = []


class Fin(Exception):
    pass


signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(Fin()))


def revisar(texto, condicion, detalle=""):
    print("   %-58s %s" % (texto, "ok" if condicion else "FALLA"))
    if not condicion:
        fallas.append(texto + (" — " + detalle if detalle else ""))


def cargar(ruta, nombre, corte="while True:"):
    """Importa el programa como modulo, sin ejecutar su lazo principal."""
    fuente = open(ruta).read()
    i = fuente.find(corte)
    espec = importlib.util.spec_from_loader(nombre, loader=None)
    mod = importlib.util.module_from_spec(espec)
    mod.__dict__["__name__"] = nombre
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(fuente[:i] if i > 0 else fuente, ruta, "exec"),
             mod.__dict__)
    return mod, fuente


def correr_lazo(fuente, entorno, pasos, segundos=20):
    """Ejecuta el while True del programa un numero fijo de vueltas."""
    cuerpo = fuente[fuente.find("while True:"):]
    cuerpo = cuerpo.replace("while True:", "for _paso in range(PASOS):", 1)
    entorno["PASOS"] = pasos
    salida = io.StringIO()
    signal.alarm(segundos)
    try:
        with contextlib.redirect_stdout(salida):
            exec(compile(cuerpo, "lazo", "exec"), entorno)
        signal.alarm(0)
    except Fin:
        signal.alarm(0)
    except Exception as e:
        signal.alarm(0)
        fallas.append("el lazo se detuvo: %s: %s" % (type(e).__name__, e))
    return salida.getvalue()


class RelojFalso:
    """time de MicroPython con el tiempo bajo control."""
    def __init__(s):
        s.t = 0
    def ticks_ms(s):
        return s.t
    def ticks_diff(s, a, b):
        return a - b
    def ticks_add(s, a, b):
        return a + b
    def sleep_ms(s, ms):
        s.t += ms
    def sleep(s, seg):
        s.t += int(seg * 1000)


# ==================================================================
print("=" * 74)
print("  7.2  La placa como servidor web")
print("=" * 74)

RUTA72 = "programas/lab_7_2_servidor_web.py"
m72, _ = cargar(RUTA72, "srv72", "def main")
m72.PUERTO = 8092
hilo = threading.Thread(target=None)


def levantar(modulo, puerto):
    modulo.PUERTO = puerto
    h = threading.Thread(target=modulo.main, daemon=True)
    h.start()
    for _ in range(60):
        try:
            urllib.request.urlopen("http://127.0.0.1:%d/" % puerto,
                                   timeout=2).read()
            return
        except Exception:
            time.sleep(0.1)
    raise RuntimeError("el servidor no llego a escuchar")


def visitar(puerto, camino="/"):
    t0 = time.monotonic()
    try:
        r = urllib.request.urlopen("http://127.0.0.1:%d%s" % (puerto, camino),
                                   timeout=5)
        return r.status, r.read().decode(), time.monotonic() - t0
    except urllib.error.HTTPError as e:
        return e.code, "", time.monotonic() - t0


# se recarga el modulo completo para que main() exista
espec = importlib.util.spec_from_loader("srv72c", loader=None)
m72 = importlib.util.module_from_spec(espec)
m72.__dict__["__name__"] = "srv72c"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(RUTA72).read(), RUTA72, "exec"), m72.__dict__)

levantar(m72, 8092)

codigo, html, tardanza = visitar(8092)
revisar("la pagina responde y trae las dos magnitudes",
        codigo == 200 and "Temperatura:" in html and "Humedad:" in html)
revisar("el HTML esta completo",
        html.lstrip().startswith("<!DOCTYPE html>")
        and html.rstrip().endswith("</html>"))
print("      la visita tardo %.0f ms" % (tardanza * 1000))
revisar("contesta rapido: no espera a medir", tardanza < 0.5,
        "tardo %.2f s" % tardanza)

t0 = time.monotonic()
for _ in range(10):
    visitar(8092)
total = time.monotonic() - t0
print("      diez visitas seguidas: %.2f s  (midiendo dentro de la "
      "peticion serian 20 s)" % total)
revisar("aguanta visitas seguidas sin atascarse", total < 2.0,
        "tardo %.2f s" % total)

codigo, _, _ = visitar(8092, "/favicon.ico")
revisar("el pedido de icono no gasta una pagina entera", codigo == 404)

antes = m72.temperatura
original = dht.DHT11.measure
dht.DHT11.measure = lambda s: (_ for _ in ()).throw(OSError("checksum"))
time.sleep(m72.INTERVALO_MS / 1000.0 + 1.5)
codigo, html, _ = visitar(8092)
revisar("sobrevive a las tramas con error del DHT11", codigo == 200)
revisar("conserva la ultima medicion buena",
        "Temperatura: %s C" % antes in html)
revisar("avisa en la pagina que hay lecturas fallidas",
        "lecturas fallidas" in html)

# Para la prueba de recuperacion el sensor tiene que acertar seguro.
# El simulador falla una lectura de cada siete al azar, igual que el
# DHT11 real, y con el original puesto esta comprobacion salia bien o
# mal segun la suerte: la que fallaba era la prueba, no el programa.
dht.DHT11.measure = lambda s: None
time.sleep(m72.INTERVALO_MS / 1000.0 + 1.5)
codigo, html, _ = visitar(8092)
dht.DHT11.measure = original
revisar("se recupera solo cuando el sensor vuelve",
        codigo == 200 and "lecturas fallidas" not in html)

fuente72 = open(RUTA72).read()
revisar("no hay ninguna clave escrita en el programa",
        "milo2012" not in fuente72 and "WIFI_CLAVE =" not in fuente72)
revisar("reserva el puerto con SO_REUSEADDR", "SO_REUSEADDR" in fuente72)
revisar("cierra siempre el socket del visitante", "finally:" in fuente72)

print("")
print("=" * 74)
print("  7.3  Indicadores de barra")
print("=" * 74)

m73, _ = cargar("programas/lab_7_3_barras.py", "barr73", "def barra")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open("programas/lab_7_3_barras.py").read(), "b73", "exec"),
         m73.__dict__)

for valor, minimo, maximo, esperado in ((25, 0, 50, 50.0), (-5, 0, 50, 0.0),
                                        (60, 0, 50, 100.0), (55, 20, 90, 50.0)):
    obtenido = m73.porcentaje(valor, minimo, maximo)
    bien = abs(obtenido - esperado) < 0.01
    print("   %4s en escala %2d a %-3d -> %6.1f %%  (esperado %5.1f)   %s"
          % (valor, minimo, maximo, obtenido, esperado,
             "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("7.3 porcentaje(%s)" % valor)

trozo = m73.barra("HUMEDAD", 15, "%", 20, 90, "#00CED1")
revisar("una humedad de 15 % se informa como 15, no como 20",
        ">15 %<" in trozo and ">20 %<" not in trozo)
revisar("y ademas se avisa que quedo fuera de escala",
        "fuera de escala" in trozo)

print("")
print("=" * 74)
print("  7.4  ESP-NOW — una pulsacion, una alarma")
print("=" * 74)

import espnow
espnow.ESPNow._buzon.clear()

RUTA_TX = "programas/lab_7_5_transmisor.py"
RUTA_RX = "programas/lab_7_5_receptor.py"

fuente_tx = open(RUTA_TX).read()
fuente_rx = open(RUTA_RX).read()

revisar("el transmisor enciende la radio pero no se conecta a ninguna red",
        "wlan.active(True)" in fuente_tx and "wlan.disconnect()" in fuente_tx)
revisar("el receptor hace lo mismo",
        "wlan.active(True)" in fuente_rx and "wlan.disconnect()" in fuente_rx)
revisar("el receptor no se queda bloqueado esperando",
        "recv(50)" in fuente_rx)
revisar("el zumbador se calla por reloj y no con una espera",
        "ticks_add" in fuente_rx and "time.sleep(" not in fuente_rx)

# ---- el transmisor, con un pulsador que rebota
REBOTES = 2


class PulsadorFalso:
    def __init__(s):
        s.guion = []
    def pulsar(s):
        for i in range(REBOTES):
            s.guion.append(i % 2)
        s.guion += [0] * 30
        for i in range(REBOTES):
            s.guion.append(i % 2)
        s.guion += [1] * 30
    def value(s):
        return s.guion.pop(0) if s.guion else 1


mtx, _ = cargar(RUTA_TX, "tx74")
falso = PulsadorFalso()
for _ in range(3):
    falso.pulsar()

entorno = dict(mtx.__dict__)
reloj = RelojFalso()
entorno["pulsador"] = falso
entorno["time"] = reloj
entorno["ultimo_cambio"] = reloj.ticks_ms()
salida_tx = correr_lazo(fuente_tx, entorno, len(falso.guion))

enviados = len(espnow.ESPNow._buzon)
print("      tres pulsaciones con %d rebotes cada una -> %d mensajes"
      % (REBOTES, enviados))
revisar("una pulsacion manda un solo mensaje", enviados == 3,
        "mando %d" % enviados)
revisar("confirma la entrega", salida_tx.count("Mensaje entregado.") == 3)

# ---- el receptor recoge lo que quedo en el aire
mrx, _ = cargar(RUTA_RX, "rx74")
entorno = dict(mrx.__dict__)
reloj = RelojFalso()
entorno["time"] = reloj
entorno["callar_en"] = 0
salida_rx = correr_lazo(fuente_rx, entorno, 10)

revisar("el receptor recibe las tres alarmas",
        salida_rx.count("Alarma recibida") == 3,
        "recibio %d" % salida_rx.count("Alarma recibida"))
revisar("y no confunde el mensaje con otra cosa",
        "Mensaje desconocido" not in salida_rx)

# el zumbador debe apagarse al cumplirse la duracion
buzzer = entorno["buzzer"]
revisar("el zumbador quedo sonando mientras corria la duracion",
        buzzer.value() == 1)
reloj.t += mrx.DURACION_MS + 10
espnow.ESPNow._buzon.clear()
correr_lazo(fuente_rx, entorno, 3)
revisar("y se calla solo al cumplirse los %d ms" % mrx.DURACION_MS,
        buzzer.value() == 0)


# ==================================================================
print("")
print("=" * 74)
print("  7.5  MQTT y Adafruit IO")
print("=" * 74)

fuente75 = open("programas/lab_7_6_mqtt.py").read()
revisar("usa umqtt.robust y no umqtt.simple",
        "umqtt.simple" not in open("programas/iot.py").read())
revisar("atrapa el fallo al publicar y vuelve a conectarse",
        "except Exception" in fuente75 and
        fuente75.count("conectar_adafruit") >= 2)
revisar("no hay ninguna clave escrita en el programa",
        "aio_" not in fuente75 and "AIO_CLAVE =" not in fuente75)

# el limite de la cuenta gratuita: n feeds cada t segundos
m75, _ = cargar("programas/lab_7_6_mqtt.py", "mqtt75", "def leer_sensor")
FEEDS, TOPE = 2, 30
por_minuto = FEEDS * 60.0 / m75.INTERVALO
print("   %d feeds cada %d s -> %.1f datos por minuto  (tope %d)"
      % (FEEDS, m75.INTERVALO, por_minuto, TOPE))
revisar("el intervalo deja margen bajo el tope de la cuenta gratuita",
        por_minuto <= TOPE * 0.6,
        "%.1f de %d" % (por_minuto, TOPE))

minimo = FEEDS * 60.0 / TOPE
print("   con %d feeds el minimo teorico es %.1f s; con 4 feeds, %.1f s"
      % (FEEDS, minimo, 4 * 60.0 / TOPE))
revisar("la cuenta del recuadro es correcta: 4 feeds -> 8 s justo en el techo",
        abs(4 * 60.0 / TOPE - 8.0) < 0.01)

print("")
print("=" * 74)
print("  7.6  InfluxDB y Grafana")
print("=" * 74)

import urequests
registro = urequests._registro
registro.enviadas.clear()
registro.fallar = False

m76, fuente76 = cargar("programas/lab_7_7_influx.py", "influx76", "def main")

revisar("la direccion sale de config y no esta escrita en el programa",
        "192.168" not in fuente76 and "config.INFLUX_HOST" in fuente76)
revisar("cierra la respuesta en un finally", "finally:" in fuente76)

ok = m76.escribir(23.4, 55.0)
revisar("una escritura normal se acepta", ok)
url, datos, cabeceras, resp = registro.enviadas[-1]
print("   linea enviada: %r" % datos)
revisar("la linea sigue el formato de InfluxDB",
        datos == "ambiente temperatura=23.4,humedad=55.0")
revisar("la cabecera lleva el token con la palabra Token delante",
        cabeceras["Authorization"].startswith("Token "))
revisar("la respuesta quedo cerrada", resp.cerrada)

# la prueba que importa: aunque falle, no se puede quedar un socket tomado
registro.fallar = True
ok = m76.escribir(1, 2)
registro.fallar = False
revisar("un fallo de red devuelve False sin detener el programa", ok is False)

for _ in range(20):
    m76.escribir(20.0, 50.0)
abiertas = [r for (_u, _d, _c, r) in registro.enviadas if not r.cerrada]
print("   %d escrituras, %d respuestas sin cerrar" % (len(registro.enviadas),
                                                      len(abiertas)))
revisar("ninguna respuesta queda sin cerrar tras veinte escrituras",
        not abiertas, "%d abiertas" % len(abiertas))


# ==================================================================
print("")
print("=" * 74)
print("  7.4  El celular por Bluetooth")
print("=" * 74)

import bluetooth

# el modulo que el estudiante copia a la placa
espec = importlib.util.spec_from_loader("bleu", loader=None)
mble = importlib.util.module_from_spec(espec)
exec(compile(open("programas/ble_uart.py").read(), "ble_uart.py", "exec"),
     mble.__dict__)
sys.modules["ble_uart"] = mble

enlace = mble.BLEUART("ESP32-TALLER")
radio = enlace._ble

revisar("se anuncia al arrancar", len(radio.anuncios) == 1)
nombre_en_anuncio = b"ESP32-TALLER" in radio.anuncios[0]
revisar("el anuncio lleva el nombre que vera el telefono", nombre_en_anuncio)
revisar("sin nadie conectado, conectado() es falso", not enlace.conectado())

enlace.write("no deberia salir")
revisar("escribir sin nadie conectado no manda nada y no falla",
        len(radio.notificado) == 0)

radio._conectar(1)
revisar("al conectarse el telefono, conectado() es verdadero",
        enlace.conectado())
enlace.write("T:23.0C\n")
revisar("ahora si notifica", len(radio.notificado) == 1)

largo = len(radio.notificado[-1][2])
print("   el mensaje 'T:23.0C' ocupa %d bytes  (el tope de BLE son 20)" % largo)
revisar("el formato del libro entra en una notificacion", largo <= 20)

# lo que el telefono escribe
radio._enviar(enlace._rx, b"hola\n")
recibido = enlace.read()
revisar("lo que escribe el telefono llega a read()", recibido == b"hola\n")
revisar("y el buzon queda vacio despues de leerlo", enlace.read() == b"")

anuncios_antes = len(radio.anuncios)
radio._desconectar(1)
revisar("al desconectarse, conectado() vuelve a ser falso",
        not enlace.conectado())
revisar("y la placa se vuelve a anunciar, para poder reconectarse",
        len(radio.anuncios) == anuncios_antes + 1)

# ---- el programa del laboratorio
fuente74 = open("programas/lab_7_4_bluetooth.py").read()
revisar("comprueba que haya alguien antes de escribir",
        "enlace.conectado()" in fuente74)
revisar("comprueba que llego algo antes de decodificar",
        "if recibido:" in fuente74)
revisar("atrapa la trama fallida del DHT11",
        "except OSError" in fuente74)
revisar("no enciende el WiFi, que aqui solo gastaria memoria",
        "network" not in fuente74)

mlab, _ = cargar("programas/lab_7_4_bluetooth.py", "ble74")
radio2 = mlab.enlace._ble
radio2.notificado.clear()
radio2._conectar(1)
# El sensor tiene que acertar en las tres vueltas: el simulador falla
# una de cada siete al azar y el programa SALTA la vuelta fallida, que
# es lo correcto. Sin fijarlo, la prueba daba 4 o 6 mensajes segun la
# suerte, y la que fallaba era la prueba.
_medir = dht.DHT11.measure
dht.DHT11.measure = lambda s: None
salida = correr_lazo(fuente74, dict(mlab.__dict__, enlace=mlab.enlace,
                                    time=RelojFalso()), 3)
dht.DHT11.measure = _medir
mensajes = [m for (_c, _h, m) in radio2.notificado]
print("   tres vueltas del lazo -> %d mensajes" % len(mensajes))
revisar("manda temperatura y humedad por separado", len(mensajes) == 6)
revisar("ninguno pasa de 20 bytes",
        all(len(m) <= 20 for m in mensajes),
        "el mayor mide %d" % max(len(m) for m in mensajes))

# ==================================================================
print("=" * 74)
print("  7.8  Una pagina que manda, no que informa")
print("=" * 74)

RUTA78 = "programas/lab_7_8_pagina_que_manda.py"

espec = importlib.util.spec_from_loader("srv78", loader=None)
m78 = importlib.util.module_from_spec(espec)
m78.__dict__["__name__"] = "srv78"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(RUTA78).read(), RUTA78, "exec"), m78.__dict__)


def pedir(puerto, camino, referer=None):
    """Una visita, opcionalmente con la cabecera que manda el navegador."""
    pedido = urllib.request.Request("http://127.0.0.1:%d%s" % (puerto, camino))
    if referer:
        pedido.add_header("Referer", "http://127.0.0.1:%d%s" % (puerto, referer))
    try:
        r = urllib.request.urlopen(pedido, timeout=5)
        return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, ""


levantar(m78, 8098)

revisar("el rele arranca apagado", m78.encendido is False)
revisar("y el pin arranca en el nivel de reposo del modulo",
        m78.rele.value() == 1)

codigo, html = pedir(8098, "/")
revisar("la pagina responde y muestra el estado",
        codigo == 200 and "APAGADO" in html)

pedir(8098, "/on")
revisar("ENCENDER enciende el rele", m78.encendido is True)
revisar("y el pin baja, porque el modulo es activo en bajo",
        m78.rele.value() == 0)

codigo, html = pedir(8098, "/")
revisar("la pagina refleja el estado nuevo", "ENCENDIDO" in html)

# La prueba que motiva el laboratorio. Al pulsar APAGAR despues de
# ENCENDER, el navegador manda Referer con la direccion anterior, que
# contiene "/on". Un programa que busca "/on" en la peticion entera
# vuelve a encender.
pedir(8098, "/off", referer="/on")
revisar("APAGAR apaga aunque el Referer traiga /on",
        m78.encendido is False,
        "el programa esta mirando la peticion entera")

for _ in range(4):
    pedir(8098, "/on", referer="/off")
    pedir(8098, "/off", referer="/on")
revisar("aguanta encender y apagar seguido en la misma pestana",
        m78.encendido is False)

codigo, _ = pedir(8098, "/favicon.ico")
revisar("el pedido de icono no gasta una pagina entera", codigo == 404)

pedir(8098, "/cualquier-cosa", referer="/on")
revisar("una direccion desconocida no cambia el rele",
        m78.encendido is False)

fuente78 = open(RUTA78).read()
revisar("no hay ninguna clave escrita en el programa",
        "WIFI_CLAVE =" not in fuente78 and "milo" not in fuente78.lower())
revisar("lee la linea del pedido y no la peticion entera",
        'split("\\r\\n")[0]' in fuente78)
revisar("cierra siempre el socket del visitante", "finally:" in fuente78)
revisar("el nivel del modulo esta en una sola constante",
        fuente78.count("ACTIVO_EN_BAJO") == 2)

# El mismo error, reproducido, para dejar constancia de que la
# comprobacion de arriba distingue las dos versiones.
def camino_ingenuo(peticion):
    if "/on" in peticion:
        return "/on"
    if "/off" in peticion:
        return "/off"
    return "/"


peticion_real = ("GET /off HTTP/1.1\r\nHost: 192.168.0.42\r\n"
                 "Referer: http://192.168.0.42/on\r\n\r\n")
revisar("la version ingenua, en cambio, lee /on donde dice /off",
        camino_ingenuo(peticion_real) == "/on"
        and m78.camino_pedido(peticion_real) == "/off")

print("")
print("=" * 74)
print("  7.9  El boton del tablero: suscribirse en lugar de publicar")
print("=" * 74)

RUTA79 = "programas/lab_7_9_boton_adafruit.py"
m79, fuente79 = cargar(RUTA79, "ada79", "def main")

revisar("el rele arranca apagado",
        (m79.mandar(False), m79.encendido is False)[1])

# --- la funcion de atencion, con lo que manda de verdad el servidor
m79.atender(b"u/feeds/foco", b"1")
revisar("una orden 1 enciende", m79.encendido is True)
m79.atender(b"u/feeds/foco", b"0")
revisar("una orden 0 apaga", m79.encendido is False)

m79.atender(b"u/feeds/foco", b"1")
m79.atender(b"u/feeds/foco", b"ON")
revisar("una orden desconocida se ignora en vez de darse por buena",
        m79.encendido is True)
m79.atender(b"u/feeds/foco", b"0")

m79.atender(b"u/feeds/foco", b" 1 \n")
revisar("tolera los espacios y el salto de linea del feed",
        m79.encendido is True)
m79.atender(b"u/feeds/foco", b"0")

# --- el lazo completo, con el servidor entregando mensajes
cliente = MQTTClient79 = None
with contextlib.redirect_stdout(io.StringIO()):
    entorno = dict(m79.__dict__)
    cliente = entorno["iot"].conectar_adafruit("prueba")
    cliente.set_callback(m79.atender)
    cliente.subscribe(entorno["iot"].feed(m79.FEED))

revisar("se suscribe al feed y no solo publica en el",
        "u/feeds/foco" in cliente.suscrito or
        any(t.endswith("/feeds/foco") for t in cliente.suscrito))

cliente.entregar("x/feeds/foco", "1")
cliente.check_msg()
revisar("check_msg() es lo que hace llegar la orden", m79.encendido is True)
cliente.entregar("x/feeds/foco", "0")
cliente.check_msg()
revisar("y la siguiente tambien", m79.encendido is False)

revisar("pide el ultimo valor guardado para arrancar sincronizado",
        '"/get"' in fuente79 or "'/get'" in fuente79)
revisar("manda ping para que el servidor no corte la sesion",
        ".ping()" in fuente79)
revisar("el ping va a la mitad del keepalive",
        m79.PING_MS * 2 <= 60000 and m79.PING_MS >= 20000,
        "PING_MS = %d" % m79.PING_MS)
revisar("no hay ninguna clave escrita en el programa",
        "AIO_CLAVE =" not in fuente79 and "aio_" not in fuente79)
revisar("el nivel del modulo esta en una sola constante",
        fuente79.count("ACTIVO_EN_BAJO") == 2)

print("")
print("=" * 74)
if fallas:
    print("  %d comprobaciones fallaron:" % len(fallas))
    for f in fallas:
        print("    -", f)
else:
    print("  el capitulo 7 completo pasa la verificacion")
print("=" * 74)
