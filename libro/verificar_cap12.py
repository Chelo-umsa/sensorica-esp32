# -*- coding: utf-8 -*-
"""Verificacion de los capitulos 1 y 2.

Se ejecutan los programas TAL COMO SALEN IMPRESOS: los archivos de
la carpeta programas/ los escribe el propio generador del libro a
partir de los bloques de codigo del capitulo, de modo que lo que se
prueba aqui es exactamente lo que va a leer el estudiante.
"""
import sys, os, io, signal, contextlib, importlib.util

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
from machine import Pin

fallas = []


class Fin(Exception):
    pass


signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(Fin()))


def revisar(texto, condicion, detalle=""):
    print("   %-58s %s" % (texto, "ok" if condicion else "FALLA"))
    if not condicion:
        fallas.append(texto + (" — " + detalle if detalle else ""))


def correr(ruta, segundos=2):
    """Ejecuta un programa del libro unos segundos y devuelve su salida."""
    salida = io.StringIO()
    signal.alarm(segundos)
    try:
        with contextlib.redirect_stdout(salida):
            exec(compile(open(ruta).read(), ruta, "exec"), {"__name__": "__main__"})
        signal.alarm(0)
    except Fin:
        signal.alarm(0)
    except Exception as e:
        signal.alarm(0)
        fallas.append("%s se detuvo: %s: %s" % (ruta, type(e).__name__, e))
        print("   FALLA en %s: %s: %s" % (ruta, type(e).__name__, e))
    return salida.getvalue()


def cargar(ruta, nombre):
    """Importa el programa como modulo, sin ejecutar su lazo principal."""
    fuente = open(ruta).read()
    corte = fuente.find("while True:")
    espec = importlib.util.spec_from_loader(nombre, loader=None)
    mod = importlib.util.module_from_spec(espec)
    mod.__dict__["__name__"] = nombre
    exec(compile(fuente[:corte], ruta, "exec"), mod.__dict__)
    return mod


print("=" * 74)
print("  1.5  El primer programa")
print("=" * 74)
t = correr("programas/lab_1_5_parpadeo.py", 2)
revisar("alterna encendido y apagado",
        t.count("encendido") >= 2 and t.count("apagado") >= 2)
revisar("usa el GPIO2, que es el LED de la placa", "Pin(2" in
        open("programas/lab_1_5_parpadeo.py").read())

print("")
print("=" * 74)
print("  2.1  Gobernar una salida digital")
print("=" * 74)
t = correr("programas/lab_2_1_salida_digital.py", 2)
revisar("el LED conmuta", t.count("encendido") >= 2 and t.count("apagado") >= 2)

print("")
print("=" * 74)
print("  2.2  Semaforo — nunca dos luces a la vez")
print("=" * 74)
m = cargar("programas/lab_2_2_semaforo.py", "sem22")
luces = (m.rojo, m.amarillo, m.verde)
nombres = ("rojo", "amarillo", "verde")

for objetivo, etiqueta in zip(luces, nombres):
    with contextlib.redirect_stdout(io.StringIO()):
        m.encender(objetivo, 0, "")
    estados = [l.value() for l in luces]
    bien = sum(estados) == 1 and estados[luces.index(objetivo)] == 1
    print("   con %-9s encendida -> rojo=%d amarillo=%d verde=%d   %s"
          % (etiqueta, estados[0], estados[1], estados[2], "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("2.2 estado con %s" % etiqueta)

revisar("la secuencia del ciclo esta completa",
        all(x in open("programas/lab_2_2_semaforo.py").read()
            for x in ("encender(rojo", "encender(verde", "encender(amarillo")))

# la falla historica: apagar despues de la espera
fuente = open("programas/lab_2_2_semaforo.py").read()
revisar("no queda ningun .off() suelto despues de una espera",
        ".off()" not in fuente)

print("")
print("=" * 74)
print("  2.3  Pulsador — una pulsacion, un cambio")
print("=" * 74)
m = cargar("programas/lab_2_3_pulsador.py", "puls23")
revisar("declara la resistencia interna de elevacion",
        "PULL_UP" in open("programas/lab_2_3_pulsador.py").read())
revisar("el pulsador no se cablea contra 3V3",
        "3V3" not in open("programas/lab_2_3_pulsador.py").read())

# Se simulan tres pulsaciones con rebote, ejecutando el lazo a mano.
# El reloj es falso y avanza solo cuando el programa duerme: asi la
# prueba es determinista y no depende de lo cargada que este la
# maquina. Con reloj real el resultado cambiaba de una corrida a otra.
import time as _time


class RelojFalso:
    """time de MicroPython, pero con el tiempo bajo control."""
    def __init__(s):
        s.t = 0
    def ticks_ms(s):
        return s.t
    def ticks_diff(s, a, b):
        return a - b
    def sleep_ms(s, ms):
        s.t += ms
    def sleep(s, seg):
        s.t += int(seg * 1000)
fuente = open("programas/lab_2_3_pulsador.py").read()
cuerpo = fuente[fuente.find("while True:"):]
cuerpo = cuerpo.replace("while True:", "for _paso in range(PASOS):", 1)

entorno = dict(m.__dict__)
entorno["PASOS"] = 0

# Un pulsador real rebota menos de 5 ms. Con el lazo muestreando cada
# 10 ms, eso son una o dos lecturas sucias, no seis: el tren de rebote
# tiene que durar MENOS que el filtro, o no se estaria probando el
# filtro sino su desborde.
REBOTES = 2          # lecturas sucias por toque -> 20 ms, bajo los 50 del filtro


class PulsadorFalso:
    """Reproduce el rebote: al tocar, alterna varias veces antes de asentar."""
    def __init__(s):
        s.guion = []
    def pulsar(s):
        for i in range(REBOTES):
            s.guion.append(i % 2)          # rebote
        s.guion += [0] * 40                # presionado y quieto
        for i in range(REBOTES):
            s.guion.append(i % 2)
        s.guion += [1] * 40                # suelto
    def value(s):
        return s.guion.pop(0) if s.guion else 1


falso = PulsadorFalso()
for _ in range(3):
    falso.pulsar()
reloj = RelojFalso()
entorno["pulsador"] = falso
entorno["PASOS"] = len(falso.guion)
entorno["time"] = reloj
entorno["ultimo_cambio"] = reloj.ticks_ms()

salida = io.StringIO()
signal.alarm(20)
try:
    with contextlib.redirect_stdout(salida):
        exec(compile(cuerpo, "lazo23", "exec"), entorno)
    signal.alarm(0)
except Fin:
    signal.alarm(0)
except Exception as e:
    signal.alarm(0)
    fallas.append("2.3 el lazo se detuvo: %s" % e)

t = salida.getvalue()
cambios = t.count("LED encendido") + t.count("LED apagado")
print("      tres pulsaciones con %d rebotes cada una -> %d cambios" % (REBOTES, cambios))
revisar("el rebote no produce cambios de mas", cambios == 3,
        "hubo %d" % cambios)
revisar("el estado se alterna en el orden correcto",
        t.count("LED encendido") == 2 and t.count("LED apagado") == 1)

print("")
print("=" * 74)
print("  2.4  Alarma PIR — vigila mientras suena")
print("=" * 74)
fuente = open("programas/lab_2_4_pir_alarma.py").read()
revisar("el buzzer arranca en silencio", "duty_u16(0)" in fuente)
revisar("no hay ninguna espera larga dentro del lazo",
        "time.sleep(" not in fuente)
revisar("el tono se cambia comparando el reloj, no esperando",
        "ticks_diff" in fuente)

m = cargar("programas/lab_2_4_pir_alarma.py", "pir24")
cuerpo = fuente[fuente.find("while True:"):]
cuerpo = cuerpo.replace("while True:", "for _paso in range(PASOS):", 1)


class PirFalso:
    def __init__(s, guion):
        s.guion = list(guion)
    def value(s):
        return s.guion.pop(0) if s.guion else 0


# quieto, luego movimiento sostenido, luego quieto otra vez
guion = [0] * 5 + [1] * 60 + [0] * 10
entorno = dict(m.__dict__)
reloj = RelojFalso()
entorno["pir"] = PirFalso(guion)
entorno["PASOS"] = len(guion)
entorno["time"] = reloj
entorno["cambio"] = reloj.ticks_ms()

frecuencias = []
_freq = entorno["buzzer"].freq
entorno["buzzer"].freq = lambda f=None, _o=_freq: (frecuencias.append(f), _o(f))[1]

salida = io.StringIO()
signal.alarm(20)
try:
    with contextlib.redirect_stdout(salida):
        exec(compile(cuerpo, "lazo24", "exec"), entorno)
    signal.alarm(0)
except Fin:
    signal.alarm(0)
except Exception as e:
    signal.alarm(0)
    fallas.append("2.4 el lazo se detuvo: %s" % e)

t = salida.getvalue()
print("      cambios de tono durante la deteccion: %d" % len(frecuencias))
revisar("avisa una sola vez al detectar", t.count("Movimiento detectado") == 1,
        "%d avisos" % t.count("Movimiento detectado"))
revisar("avisa una sola vez al cesar", t.count("Sin movimiento") == 1)
revisar("la sirena alterno los dos tonos",
        set(frecuencias) == set(m.TONOS) if frecuencias else False,
        "tonos usados: %s" % sorted(set(frecuencias)))
revisar("el buzzer quedo en silencio al final",
        entorno["buzzer"].duty_u16() == 0 if hasattr(entorno["buzzer"], "duty_u16") else True)

print("")
print("=" * 74)
print("  2.5  El rele: una carga que no puede colgar del pin")
print("=" * 74)

RUTA25 = "programas/lab_2_5_rele.py"
m25 = cargar(RUTA25, "rele25")
fuente25 = open(RUTA25).read()

# --- la falla segura, que con 220 V en la mesa es lo primero
revisar("el rele queda apagado apenas arranca el programa",
        m25.estado is False and m25.rele.value() == 1)

m25.mandar(True)
revisar("encender baja el pin, porque el modulo es activo en bajo",
        m25.rele.value() == 0)
m25.mandar(False)
revisar("apagar lo devuelve al nivel de reposo", m25.rele.value() == 1)

# --- y el mismo programa con el puente en la otra posicion
m25.ACTIVO_EN_BAJO = False
m25.mandar(True)
revisar("con el puente en H, encender sube el pin", m25.rele.value() == 1)
m25.mandar(False)
revisar("y apagar lo baja", m25.rele.value() == 0)
m25.ACTIVO_EN_BAJO = True
m25.mandar(False)

revisar("el nivel esta en una sola constante y no repartido por el codigo",
        fuente25.count("ACTIVO_EN_BAJO") == 2)
revisar("declara la resistencia interna de elevacion",
        "PULL_UP" in fuente25)
revisar("no hay ningun sleep largo que haga parpadear la carga",
        "sleep(0.5)" not in fuente25 and "sleep_ms(500)" not in fuente25)

# --- el lazo, con el mismo pulsador con rebote del 2.3
cuerpo25 = fuente25[fuente25.find("while True:"):]
cuerpo25 = cuerpo25.replace("while True:", "for _paso in range(PASOS):", 1)

falso25 = PulsadorFalso()
for _ in range(3):
    falso25.pulsar()
reloj25 = RelojFalso()
entorno25 = dict(m25.__dict__)
entorno25["boton"] = falso25
entorno25["PASOS"] = len(falso25.guion)
entorno25["time"] = reloj25
# el programa tomo ultimo_cambio con el reloj real al importarse; con
# el reloj falso arrancando en cero, ticks_diff daria negativo siempre
entorno25["ultimo_cambio"] = reloj25.ticks_ms()

salida25 = io.StringIO()
signal.alarm(20)
try:
    with contextlib.redirect_stdout(salida25):
        exec(compile(cuerpo25, "lazo25", "exec"), entorno25)
    signal.alarm(0)
except Fin:
    signal.alarm(0)
except Exception as e:
    signal.alarm(0)
    fallas.append("2.5 el lazo se detuvo: %s" % e)

t25 = salida25.getvalue()
maniobras = t25.count("foco encendido") + t25.count("foco apagado")
print("      tres pulsaciones con %d rebotes cada una -> %d maniobras"
      % (REBOTES, maniobras))
revisar("el rebote no produce maniobras de mas del rele", maniobras == 6,
        "hubo %d" % maniobras)
revisar("enciende al presionar y no al soltar",
        t25.find("foco encendido") < t25.find("foco apagado"))
revisar("termina apagado", t25.rstrip().endswith("foco apagado"))

# --- la prueba que da nombre al laboratorio: el cable cortado.
# Con PULL_UP, un pulsador desconectado lee 1 para siempre. La version
# que parpadea tiene el parpadeo en esa rama y encendia la carga sola.
class SinCable:
    def value(s):
        return 1


entorno26 = dict(m25.__dict__)
entorno26["boton"] = SinCable()
entorno26["PASOS"] = 200
_reloj26 = RelojFalso()
entorno26["time"] = _reloj26
entorno26["ultimo_cambio"] = _reloj26.ticks_ms()
entorno26["estado"] = False
m25.mandar(False)
salida26 = io.StringIO()
signal.alarm(20)
try:
    with contextlib.redirect_stdout(salida26):
        exec(compile(cuerpo25, "lazo25b", "exec"), entorno26)
    signal.alarm(0)
except Fin:
    signal.alarm(0)
except Exception as e:
    signal.alarm(0)
    fallas.append("2.5 el lazo se detuvo sin pulsador: %s" % e)

revisar("con el cable del pulsador cortado, la carga queda apagada",
        m25.rele.value() == 1 and "foco encendido" not in salida26.getvalue())

print("")
print("=" * 74)
if fallas:
    print("  %d comprobaciones fallaron:" % len(fallas))
    for f in fallas:
        print("    -", f)
else:
    print("  los capitulos 1 y 2 pasan la verificacion")
print("=" * 74)
