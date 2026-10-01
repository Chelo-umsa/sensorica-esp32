# -*- coding: utf-8 -*-
"""Modulos simulados: permiten ejecutar los programas del libro en una
computadora, sin ESP32, para verificar la logica."""
import sys, time as _t, types, random, math

# ------------------------------------------------------------------ machine
class Pin:
    IN, OUT, PULL_UP, IRQ_FALLING, IRQ_RISING = 0, 1, 2, 4, 8
    def __init__(s, n, modo=None, pull=None):
        s.n, s.modo, s._v, s._h = n, modo, 0, None
    def value(s, v=None):
        if v is None:
            return s._v               # la entrada conserva su estado
        s._v = v
    def on(s):  s._v = 1
    def off(s): s._v = 0
    def irq(s, trigger=None, handler=None): s._h = handler
    def disparar(s, n=1):
        for _ in range(n):
            if s._h: s._h(s)

class PWM:
    def __init__(s, pin, freq=5000): s.pin, s._f, s._d = pin, freq, 0
    def freq(s, f=None):
        if f is None: return s._f
        s._f = f
    def duty(s, d=None):
        if d is None: return s._d
        s._d = d
    def duty_u16(s, d=None):
        if d is None: return s._d
        s._d = d
    def deinit(s):
        # MicroPython real apaga la salida y suelta el pin. Aqui basta
        # con dejar el ciclo de trabajo en cero: lo que los programas
        # comprueban es que el servo o el zumbador queden en reposo.
        s._d = 0
        s._activo = False

class SoftI2C:
    def __init__(s, *a, scl=None, sda=None, freq=400000): pass
    def scan(s): return [0x3C]
I2C = SoftI2C

class UART:
    def __init__(s, n, baudrate=9600, tx=None, rx=None): pass
    def write(s, d): return len(d)
    def read(s, n=None): return b""
    def any(s): return 0

class RTC:
    def datetime(s, v=None):
        t = _t.localtime()
        return (t.tm_year, t.tm_mon, t.tm_mday, t.tm_wday,
                t.tm_hour, t.tm_min, t.tm_sec, 0)

def reset(): raise SystemExit("reset()")
def unique_id(): return b"\xaa\xbb\xcc\xdd"

_machine = types.ModuleType("machine")
for _n in ("Pin","PWM","SoftI2C","I2C","UART","RTC","reset","unique_id"):
    setattr(_machine, _n, globals()[_n])
sys.modules["machine"] = _machine

# ------------------------------------------------------------------ network
STA_IF, AP_IF = 0, 1
class WLAN:
    def __init__(s, modo=0): s._on, s._con = False, False
    def active(s, v=None):
        if v is None: return s._on
        s._on = v
    def connect(s, ssid, clave): s._con = True
    def isconnected(s): return s._con
    def ifconfig(s): return ("192.168.0.50","255.255.255.0","192.168.0.1","8.8.8.8")
_net = types.ModuleType("network")
_net.WLAN, _net.STA_IF, _net.AP_IF = WLAN, STA_IF, AP_IF
sys.modules["network"] = _net

# ------------------------------------------------------------------ umqtt
class MQTTClient:
    def __init__(s, client_id=None, server=None, port=0, user=None,
                 password=None, keepalive=0, ssl=False):
        s.id, s.user, s.cb, s.publicados = client_id, user, None, 0
        s.suscrito, s.entrantes, s.pings = set(), [], 0
    def set_callback(s, cb): s.cb = cb
    def connect(s, clean_session=True): return 0
    def disconnect(s): pass
    def subscribe(s, topico, qos=0):
        s.suscrito.add(topico if isinstance(topico, str) else topico.decode())
        print("   [sim] suscrito a", topico)
    def publish(s, topico, msg, retain=False, qos=0):
        s.publicados += 1
        print("   [sim] -> %s = %s" % (topico if isinstance(topico,str) else topico.decode(),
                                        msg if isinstance(msg,str) else msg.decode()))
    # --- del lado del servidor: lo que el broker le manda a la placa.
    # Sin esto no hay manera de comprobar un programa que se suscribe,
    # que es justo lo que hace el laboratorio 7.9.
    def entregar(s, topico, mensaje):
        """Encola un mensaje como si lo hubiera mandado el servidor."""
        s.entrantes.append((topico.encode() if isinstance(topico, str) else topico,
                            mensaje.encode() if isinstance(mensaje, str) else mensaje))
    def check_msg(s):
        if not s.entrantes:
            return None
        topico, mensaje = s.entrantes.pop(0)
        if s.cb:
            s.cb(topico, mensaje)
        return 1
    def wait_msg(s): return s.check_msg()
    def ping(s): s.pings += 1
_u = types.ModuleType("umqtt"); _u.__path__ = []
_ur = types.ModuleType("umqtt.robust"); _ur.MQTTClient = MQTTClient
_us = types.ModuleType("umqtt.simple"); _us.MQTTClient = MQTTClient
sys.modules["umqtt"], sys.modules["umqtt.robust"], sys.modules["umqtt.simple"] = _u, _ur, _us

# ------------------------------------------------------------------ dht
class DHT11:
    def __init__(s, pin): s._t, s._h = 0, 0
    def measure(s):
        if random.random() < 0.15:
            raise OSError("checksum error")       # falla realista del DHT11
        s._t, s._h = random.randint(18, 30), random.randint(30, 80)
    def temperature(s): return s._t
    def humidity(s): return s._h
DHT22 = DHT11
_d = types.ModuleType("dht"); _d.DHT11, _d.DHT22 = DHT11, DHT22
sys.modules["dht"] = _d

# ------------------------------------------------------------------ ssd1306
class SSD1306_I2C:
    def __init__(s, w, h, i2c, addr=0x3C): s.w, s.h, s.refrescos = w, h, 0
    def fill(s, c): pass
    def pixel(s, x, y, c=None):
        assert 0 <= x < s.w and 0 <= y < s.h, "pixel fuera de pantalla: (%d,%d)" % (x, y)
    def text(s, t, x, y, c=1): pass
    def line(s, x1, y1, x2, y2, c): pass
    def rect(s, x, y, w, h, c): pass
    def fill_rect(s, x, y, w, h, c): pass
    def hline(s, x, y, w, c): pass
    def vline(s, x, y, h, c): pass
    def show(s): s.refrescos += 1
    def contrast(s, v): pass
    def poweroff(s): pass
_s = types.ModuleType("ssd1306"); _s.SSD1306_I2C = SSD1306_I2C
sys.modules["ssd1306"] = _s

# ------------------------------------------------------------------ pzem
class PZEM:
    def __init__(s, uart=None, addr=0xF8): s._n = 0
    def read(s):
        s._n += 1
        return s._n % 7 != 0            # una lectura de cada siete falla
    def getVoltage(s):      return 220.0 + random.uniform(-4, 4)
    def getCurrent(s):      return random.uniform(0.2, 4.0)
    def getActivePower(s):  return random.uniform(50, 800)
    def getPowerFactor(s):  return random.uniform(0.75, 0.99)
    def getActiveEnergy(s): return 12000.0 + s._n * 1.5
    def getFrequency(s):    return 50.0
_p = types.ModuleType("pzem"); _p.PZEM = PZEM
sys.modules["pzem"] = _p

# ------------------------------------------------- time.ticks_* de MicroPython
_t.ticks_ms = lambda: int(_t.monotonic() * 1000)
_t.ticks_us = lambda: int(_t.monotonic() * 1000000)
_t.ticks_diff = lambda a, b: a - b
_t.ticks_add = lambda a, b: a + b
_t.sleep_ms = lambda ms: _t.sleep(ms / 1000)
_t.sleep_us = lambda us: _t.sleep(us / 1000000)

# ------------------------------------------------------------------ ADC
import random as _r
class ADC:
    ATTN_0DB, ATTN_2_5DB, ATTN_6DB, ATTN_11DB = 0, 1, 2, 3
    WIDTH_9BIT, WIDTH_10BIT, WIDTH_11BIT, WIDTH_12BIT = 9, 10, 11, 12
    _simulado = {}                    # pin -> tension que se quiere simular
    def __init__(s, pin, atten=None):
        s.pin = pin.n if hasattr(pin, "n") else pin
        s._max = 4095
        s._at = ADC.ATTN_11DB if atten is None else atten
        if not (32 <= s.pin <= 39):
            print("   [sim] AVISO: GPIO%d no pertenece al ADC1" % s.pin)
    def atten(s, a): s._at = a
    def width(s, w): s._max = (1 << w) - 1
    # Fondo de escala real de cada atenuacion del ESP32
    FONDO = {0: 1.1, 1: 1.5, 2: 2.0, 3: 3.3}
    def _tension(s):
        v = ADC._simulado.get(s.pin)
        if v is None:
            v = _r.uniform(0.2, 1.0)
        return max(0.0, min(v + _r.uniform(-0.004, 0.004), 3.3))
    def read(s):
        fondo = ADC.FONDO[s._at]
        return min(int(s._tension() / fondo * s._max), s._max)
    def read_u16(s):
        fondo = ADC.FONDO[s._at]
        return min(int(s._tension() / fondo * 65535), 65535)
    def read_uv(s):
        return int(s._tension() * 1_000_000)
_machine.ADC = ADC

# ------------------------------------------------------------------ espnow
class ESPNow:
    _buzon = []                       # mensajes compartidos entre placas simuladas
    def __init__(s): s._on, s.pares = False, []
    def active(s, v=None):
        if v is None: return s._on
        s._on = v
    def add_peer(s, mac, *a, **k): s.pares.append(mac)
    def send(s, mac, msg, sync=True):
        ESPNow._buzon.append((b"\x24\x6f\x28\xaa\xbb\xcc", msg))
        print("   [sim] ESP-NOW ->", msg)
        return True
    def any(s): return len(ESPNow._buzon) > 0
    def recv(s, timeout_ms=None):
        if ESPNow._buzon:
            return ESPNow._buzon.pop(0)
        return (None, None)
    def irecv(s, timeout_ms=None): return s.recv(timeout_ms)
    def irq(s, handler): s._h = handler
_e = types.ModuleType("espnow"); _e.ESPNow = ESPNow
sys.modules["espnow"] = _e
WLAN.config = lambda s, *a, **k: b"\x24\x6f\x28\xaa\xbb\xcc"
WLAN.disconnect = lambda s: None

# ------------------------------------------------- generador de pulsos
# Permite enlazar una salida PWM con un pin de entrada, de modo que los
# programas que cuentan pulsos puedan probarse sin hardware. La
# simulacion reproduce la LOGICA y la ARITMETICA; no reproduce la
# temporizacion real: por encima de unos cientos de hercios un hilo de
# Python no alcanza a seguir el ritmo.
import threading as _th

class _Generador:
    def __init__(s, pwm, pin, tope_hz=400):
        s.pwm, s.pin, s.tope = pwm, pin, tope_hz
        s.vivo = True
        s.emitidos = 0
        _th.Thread(target=s._correr, daemon=True).start()
    def _correr(s):
        while s.vivo:
            f = min(s.pwm.freq() or 1, s.tope)
            if s.pwm.duty() == 0 and s.pwm.duty_u16() == 0:
                _t.sleep(0.01); continue
            medio = 0.5 / f
            s.pin._v = 1
            _t.sleep(medio)
            s.pin._v = 0
            s.emitidos += 1
            if s.pin._h:
                try: s.pin._h(s.pin)
                except Exception: pass
            _t.sleep(medio)
    def parar(s): s.vivo = False


class _Tren:
    """Genera pulsos a una frecuencia que entrega una funcion."""
    def __init__(s, pin, hz):
        s.pin, s.hz, s.vivo, s.emitidos = pin, hz, True, 0
        _th.Thread(target=s._correr, daemon=True).start()
    def _correr(s):
        while s.vivo:
            f = s.hz()
            if f <= 0:
                _t.sleep(0.02); continue
            medio = 0.5 / min(f, 400)
            s.pin._v = 1; _t.sleep(medio)
            s.pin._v = 0; s.emitidos += 1
            if s.pin._h:
                try: s.pin._h(s.pin)
                except Exception: pass
            _t.sleep(medio)
    def parar(s): s.vivo = False


def enlazar(pwm, pin, tope_hz=400):
    """Conecta una salida PWM a una entrada, como haria un cable."""
    return _Generador(pwm, pin, tope_hz)


def tren_de_pulsos(pin, hz):
    """Hace llegar pulsos a un pin a la frecuencia que indique hz()."""
    return _Tren(pin, hz)


# ------------------------------------------------------------ urequests
class _Respuesta:
    def __init__(s, texto="ok", codigo=204):
        s.text, s.status_code, s.cerrada = texto, codigo, False
    def close(s):
        s.cerrada = True


class _Peticiones:
    """Registra cada POST para poder comprobarlo, y avisa si el
    programa se olvida de cerrar la respuesta: en MicroPython eso
    agota los sockets y el programa termina fallando."""
    enviadas = []
    sin_cerrar = 0
    fallar = False

    @staticmethod
    def post(url, data=None, headers=None, **k):
        if _Peticiones.fallar:
            raise OSError("host no alcanzable")
        r = _Respuesta()
        _Peticiones.enviadas.append((url, data, headers, r))
        return r


_u = types.ModuleType("urequests")
_u.post = _Peticiones.post
_u.get = _Peticiones.post
_u._registro = _Peticiones
sys.modules["urequests"] = _u


# ------------------------------------------------------------ bluetooth
class _UUID:
    def __init__(s, v): s.v = v
    def __eq__(s, o): return isinstance(o, _UUID) and s.v == o.v
    def __hash__(s): return hash(s.v)
    def __repr__(s): return "UUID(%r)" % s.v


class _BLE:
    """BLE de MicroPython, lo justo para los laboratorios.

    Reproduce el registro del servicio, el anuncio, la conexion de un
    central y la notificacion. Guarda lo notificado para poder
    comprobarlo, y cuenta cuantas veces se anuncio.
    """
    def __init__(s):
        s._on = False
        s.anuncios = []
        s.notificado = []
        s._irq = None
        s._valores = {}
        s._siguiente = 10

    def active(s, v=None):
        if v is None: return s._on
        s._on = v

    def irq(s, manejador): s._irq = manejador

    def gatts_register_services(s, servicios):
        salida = []
        for _uuid, caracteristicas in servicios:
            handles = []
            for _c in caracteristicas:
                handles.append(s._siguiente); s._siguiente += 1
            salida.append(tuple(handles))
        return tuple(salida)

    def gap_advertise(s, intervalo, adv_data=None, **k):
        s.anuncios.append(bytes(adv_data) if adv_data else b"")

    def gatts_notify(s, conn, handle, datos):
        s.notificado.append((conn, handle, bytes(datos)))

    def gatts_read(s, handle): return s._valores.get(handle, b"")

    def gatts_write(s, handle, datos): s._valores[handle] = bytes(datos)

    # --- ayudas para las pruebas, no existen en la placa real
    def _conectar(s, conn=1): s._irq and s._irq(1, (conn, 0, 0))
    def _desconectar(s, conn=1): s._irq and s._irq(2, (conn, 0, 0))
    def _enviar(s, handle, datos):
        s._valores[handle] = datos
        s._irq and s._irq(3, (1, handle))


_b = types.ModuleType("bluetooth")
_b.BLE = _BLE
_b.UUID = _UUID
_b.FLAG_READ, _b.FLAG_WRITE, _b.FLAG_NOTIFY = 0x02, 0x08, 0x10
sys.modules["bluetooth"] = _b

_mp = types.ModuleType("micropython")
_mp.const = lambda v: v
sys.modules["micropython"] = _mp


# ------------------------------------------ disable_irq / enable_irq
# En la placa apagan y encienden las interrupciones. Aqui no hay
# interrupciones de verdad, pero los programas las llaman y tienen que
# existir: disable_irq devuelve el estado anterior, que enable_irq
# vuelve a poner.
_estado_irq = [True]


def _disable_irq():
    anterior = _estado_irq[0]
    _estado_irq[0] = False
    return anterior


def _enable_irq(estado=True):
    _estado_irq[0] = estado


_machine.disable_irq = _disable_irq
_machine.enable_irq = _enable_irq
