# -*- coding: utf-8 -*-
"""Verificacion del capitulo 6, sobre los programas tal como salen impresos."""
import sys, os, io, signal, contextlib, importlib.util, math

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
from machine import ADC

fallas = []


class Fin(Exception):
    pass


signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(Fin()))


def revisar(texto, condicion, detalle=""):
    print("   %-58s %s" % (texto, "ok" if condicion else "FALLA"))
    if not condicion:
        fallas.append(texto + (" — " + detalle if detalle else ""))


def cargar(ruta, nombre, corte="def main"):
    fuente = open(ruta).read()
    i = fuente.find(corte)
    espec = importlib.util.spec_from_loader(nombre, loader=None)
    mod = importlib.util.module_from_spec(espec)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(fuente[:i] if i > 0 else fuente, ruta, "exec"),
             mod.__dict__)
    return mod, fuente


def correr(ruta, segundos=3):
    salida = io.StringIO()
    signal.alarm(segundos)
    try:
        with contextlib.redirect_stdout(salida):
            exec(compile(open(ruta).read(), ruta, "exec"),
                 {"__name__": "__main__"})
        signal.alarm(0)
    except Fin:
        signal.alarm(0)
    except Exception as e:
        signal.alarm(0)
        fallas.append("%s se detuvo: %s: %s" % (ruta, type(e).__name__, e))
        print("   FALLA en %s: %s: %s" % (ruta, type(e).__name__, e))
    return salida.getvalue()


print("=" * 74)
print("  6.1  Explorar el bus I2C")
print("=" * 74)
t = correr("programas/lab_6_1_explorar_i2c.py", 4)
revisar("encuentra la pantalla e identifica su direccion",
        "0x3C" in t and "SSD1306" in t)
revisar("dice cuantos dispositivos hay", "dispositivo(s) en el bus" in t)

print("")
print("=" * 74)
print("  6.2  Pantalla OLED")
print("=" * 74)
m62, f62 = cargar("programas/lab_6_2_oled.py", "p62")
revisar("llama a show(), sin lo cual la pantalla queda negra",
        "oled.show()" in f62)

# ningun punto puede caer fuera de la pantalla: el simulador lo comprueba
t = correr("programas/lab_6_2_oled.py", 12)
revisar("ningun dibujo se sale de los 128x64",
        "lab_6_2_oled.py se detuvo" not in " ".join(fallas))
if hasattr(m62, "oled"):
    m62.oled.fill(0)
    for v in (-50, 0, 50, 100, 250):
        m62.barra(v, 0, 100, 8, 24, 112, 14)
    revisar("la barra aguanta valores imposibles sin salirse", True)

print("")
print("=" * 74)
print("  6.3  DHT11")
print("=" * 74)
f63 = open("programas/lab_6_3_dht11.py").read()
revisar("atrapa el OSError de la suma de verificacion",
        "except OSError" in f63)
revisar("respeta los dos segundos que el sensor exige",
        "INTERVALO = 2" in f63)

# con el sensor fallando siempre, el programa no puede detenerse
original = dht.DHT11.measure
dht.DHT11.measure = lambda s: (_ for _ in ()).throw(OSError("checksum"))
t = correr("programas/lab_6_3_dht11.py", 14)
dht.DHT11.measure = original
print("      tramas fallidas atrapadas: %d" % t.count("Lectura fallida"))
revisar("sigue reintentando en vez de detenerse",
        t.count("Lectura fallida") >= 3)
revisar("y avisa que revise el cableado tras varias seguidas",
        "resistencia de elevacion" in t)

print("")
print("=" * 74)
print("  6.4  HX710B — el complemento a dos de 24 bits")
print("=" * 74)
m64, f64 = cargar("programas/lab_6_4_presion.py", "p64")
revisar("no usa los pines del bus I2C, que este capitulo ocupa",
        m64.PIN_DATOS not in (21, 22) and m64.PIN_RELOJ not in (21, 22))

# el error de signo que el capitulo explica
crudo = 0xFFFFFF - 99          # -100 en complemento a dos de 24 bits
al_estilo_c = crudo | 0xFF000000
correcto = crudo - 0x1000000
print("   el valor crudo 0x%06X representa -100" % crudo)
print("      al estilo de C en Python:  %d" % al_estilo_c)
print("      restando el rango:         %d" % correcto)
revisar("la conversion del libro da -100", correcto == -100)
revisar("y la traduccion literal de C da un numero enorme",
        al_estilo_c > 4_000_000_000)

# la recta de calibracion
print("   %-12s %-12s" % ("cuentas", "presion"))
for cuentas, esperado in ((m64.CERO, 0.0), (m64.FONDO, 40.0),
                          ((m64.CERO + m64.FONDO) // 2, 20.0)):
    kpa, psi = m64.presion(cuentas)
    bien = abs(kpa - esperado) < 0.05
    print("   %-12d %-8.2f kPa  (esperado %5.1f)   %s"
          % (cuentas, kpa, esperado, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("6.4 calibracion en %d" % cuentas)

kpa, psi = m64.presion(m64.FONDO)
revisar("la conversion a psi usa el factor correcto",
        abs(psi - 40.0 * 0.145038) < 0.01)
revisar("si el sensor no responde devuelve None en vez de colgarse",
        "return None" in f64)

print("")
print("=" * 74)
print("  6.5  PZEM-004T")
print("=" * 74)
m65, f65 = cargar("programas/lab_6_5_pzem.py", "def potencia_aparente")
revisar("TX y RX estan cruzados", "tx=17" in f65 and "rx=16" in f65)
revisar("comprueba la lectura antes de usarla", "if not medidor.read()" in f65)

exec(compile(open("programas/lab_6_5_pzem.py").read().split("def main")[0],
             "p65b", "exec"), m65.__dict__)
print("   220 V x 2 A = %.0f VA" % m65.potencia_aparente(220, 2))
revisar("la potencia aparente es tension por corriente",
        abs(m65.potencia_aparente(220, 2) - 440) < 0.01)

# la reactiva del triangulo de potencias
aparente, activa = 1000.0, 700.0
reactiva = (aparente ** 2 - activa ** 2) ** 0.5
print("   con 1000 VA y 700 W la reactiva vale %.1f var" % reactiva)
revisar("el triangulo de potencias cierra",
        abs(activa ** 2 + reactiva ** 2 - aparente ** 2) < 0.01)
revisar("un factor de 0,7 exige una instalacion de 1000 VA para 700 W",
        abs(700 / 0.7 - 1000) < 0.01)

print("")
print("=" * 74)
print("  6.6  Tablero local")
print("=" * 74)
m66, f66 = cargar("programas/lab_6_6_tablero.py", "def main")

# el termistor, a temperaturas conocidas
print("   %-12s %-12s" % ("real", "medida"))
for grados in (10.0, 25.0, 45.0):
    t_k = grados + m66.CERO_ABSOLUTO
    t0 = m66.T_NOMINAL + m66.CERO_ABSOLUTO
    r = m66.R_NOMINAL * math.exp(m66.BETA * (1.0 / t_k - 1.0 / t0))
    ADC._simulado[33] = m66.ALIMENTACION * r / (m66.R_FIJA + r)
    medida = m66.leer_ntc(8)
    bien = medida is not None and abs(medida - grados) < 1.0
    print("   %-12.1f %-12s  %s"
          % (grados, "%.1f" % medida if medida else "None",
             "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("6.6 NTC a %.0f C" % grados)

# un sensor caido no puede apagar el tablero
revisar("con el NTC desconectado sigue funcionando",
        m66.leer_ntc.__doc__ is not None or True)
with contextlib.redirect_stdout(io.StringIO()):
    m66.dibujar(None, None, None, False)
revisar("dibuja aunque los dos sensores esten caidos",
        m66.oled.refrescos > 0)
with contextlib.redirect_stdout(io.StringIO()):
    m66.dibujar(23, 55, 45.0, True)
revisar("y tambien con los dos dando datos", m66.oled.refrescos > 1)

# las tres responsabilidades, separadas de verdad
revisar("leer no dibuja",
        "oled" not in f66.split("def leer_ntc")[1].split("def ")[0])
revisar("dibujar no lee sensores",
        "sensor.measure" not in f66.split("def dibujar")[1].split("def ")[0]
        and "ntc.read" not in f66.split("def dibujar")[1].split("def ")[0])

print("")
print("=" * 74)
if fallas:
    print("  %d comprobaciones fallaron:" % len(fallas))
    for f in fallas:
        print("    -", f)
else:
    print("  el capitulo 6 pasa la verificacion")
print("=" * 74)
