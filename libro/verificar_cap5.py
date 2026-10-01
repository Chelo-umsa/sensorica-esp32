# -*- coding: utf-8 -*-
"""Verificacion del capitulo 5, sobre los programas tal como salen impresos."""
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
from machine import ADC

fallas = []


class Fin(Exception):
    pass


signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(Fin()))


def revisar(texto, condicion, detalle=""):
    print("   %-58s %s" % (texto, "ok" if condicion else "FALLA"))
    if not condicion:
        fallas.append(texto + (" — " + detalle if detalle else ""))


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


def cargar(ruta, nombre, corte="while True:"):
    fuente = open(ruta).read()
    i = fuente.find(corte)
    espec = importlib.util.spec_from_loader(nombre, loader=None)
    mod = importlib.util.module_from_spec(espec)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(fuente[:i] if i > 0 else fuente, ruta, "exec"),
             mod.__dict__)
    return mod


print("=" * 74)
print("  5.2  Brillo gobernado por el potenciometro")
print("=" * 74)

# la escala: el ADC da 12 bits y duty() acepta 10
for cuentas, esperado in ((0, 0), (2048, 512), (4095, 1023)):
    obtenido = cuentas >> 2
    bien = obtenido == esperado
    print("   %4d cuentas -> duty %4d  (esperado %4d)   %s"
          % (cuentas, obtenido, esperado, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("5.2 escala en %d" % cuentas)

revisar("el extremo alto llega justo al maximo de duty(), sin pasarse",
        (4095 >> 2) == 1023)

ADC._simulado[34] = 1.65
t = correr("programas/lab_5_2_brillo.py", 2)
revisar("el programa corre y muestra las dos escalas",
        "Perilla" in t and "Brillo" in t)

fuente = open("programas/lab_5_2_brillo.py").read()
revisar("fija la atenuacion del conversor", "ATTN_11DB" in fuente)
revisar("usa una pata del ADC1, que sirve con el WiFi encendido",
        "ADC(Pin(34))" in fuente)
revisar("no mezcla duty() con duty_u16()",
        not ("duty_u16" in fuente and ".duty(" in fuente))

print("")
print("=" * 74)
print("  5.3  Servomotor — la posicion va en el ancho del pulso")
print("=" * 74)

m = cargar("programas/lab_5_3_servo.py", "servo53", "for angulo in (")

# la tabla impresa en el libro tiene que corresponderse con el programa
print("   %-8s %-8s %-10s" % ("angulo", "duty", "pulso"))
for angulo, duty_esperado in ((0, 40), (90, 77), (180, 115)):
    duty = m.angulo_a_duty(angulo)
    ancho = duty / 1023 * 20
    bien = duty == duty_esperado
    print("   %5d°   %4d     %5.2f ms   %s"
          % (angulo, duty, ancho, "ok" if bien else "FALLA (esperado %d)" % duty_esperado))
    if not bien:
        fallas.append("5.3 angulo %d" % angulo)

revisar("el centro cae cerca de 1,5 ms, como pide la norma",
        abs(m.angulo_a_duty(90) / 1023 * 20 - 1.5) < 0.06)

# el recorte: ningun angulo puede sacar al servo de su rango
extremos = [m.angulo_a_duty(a) for a in (-90, -1, 0, 180, 181, 400)]
revisar("ningun angulo, ni absurdo, pasa de DUTY_MAXIMO",
        max(extremos) <= m.DUTY_MAXIMO, "maximo obtenido %d" % max(extremos))
revisar("ni queda por debajo de DUTY_MINIMO",
        min(extremos) >= m.DUTY_MINIMO, "minimo obtenido %d" % min(extremos))

revisar("150 de ciclo de trabajo daria 2,93 ms, fuera del rango del SG90",
        abs(150 / 1023 * 20 - 2.93) < 0.01)

t = correr("programas/lab_5_3_servo.py", 12)
revisar("recorre las cinco posiciones y vuelve al centro",
        t.count("grados") >= 6)
revisar("suelta el pin al terminar",
        "deinit" in open("programas/lab_5_3_servo.py").read())

print("")
print("=" * 74)
print("  5.4  Barrido — el error que corrige este laboratorio")
print("=" * 74)

m4 = cargar("programas/lab_5_4_barrido.py", "barr54")
revisar("el tope superior quedo en 115, no en 150", m4.DUTY_MAXIMO == 115,
        "vale %d" % m4.DUTY_MAXIMO)

# se recorre el barrido entero anotando cada duty que llegaria al servo
vistos = []
_pwm = m4.servo
_original = _pwm.duty
_pwm.duty = lambda v, _o=_original: (vistos.append(v), _o(v))[1]
with contextlib.redirect_stdout(io.StringIO()):
    m4.barrer(0, 180)
    m4.barrer(180, 0)
_pwm.duty = _original

print("   escalones del barrido: %d   duty de %d a %d"
      % (len(vistos), min(vistos), max(vistos)))
revisar("ningun escalon del barrido pasa del tope",
        max(vistos) <= m4.DUTY_MAXIMO)
revisar("el barrido cubre todo el recorrido, de extremo a extremo",
        min(vistos) == m4.DUTY_MINIMO and max(vistos) == m4.DUTY_MAXIMO)
revisar("el recorte esta en el conversor y no en el lazo, para que ninguna "
        "llamada pueda saltearselo",
        "if angulo > 180" in open("programas/lab_5_4_barrido.py").read())

print("")
print("=" * 74)
print("  5.5  Zumbador pasivo")
print("=" * 74)

fuente = open("programas/lab_5_5_buzzer.py").read()
revisar("arranca en silencio", "duty_u16(0)" in fuente.split("try:")[0])
revisar("tiene un bloque finally que lo calla pase lo que pase",
        "finally:" in fuente)

import machine
_freqs, _duties = [], []
_of, _od = machine.PWM.freq, machine.PWM.duty_u16
machine.PWM.freq = lambda s, f=None, _o=_of: (_freqs.append(f), _o(s, f))[1]
machine.PWM.duty_u16 = lambda s, d=None, _o=_od: (
    _duties.append(d) if d is not None else None, _o(s, d))[1]
t = correr("programas/lab_5_5_buzzer.py", 6)
machine.PWM.freq, machine.PWM.duty_u16 = _of, _od

notas = [f for f in _freqs if f]
print("   frecuencias distintas emitidas: %d" % len(set(notas)))
revisar("suena la escala completa de siete notas",
        len({f for f in notas if 250 <= f <= 500}) >= 7,
        "%d notas" % len({f for f in notas if 250 <= f <= 500}))
revisar("el la queda en 440 Hz", 440 in notas)
revisar("despues arranca la sirena de dos tonos",
        800 in notas and 400 in notas)
revisar("el zumbador queda callado al final",
        _duties and _duties[-1] == 0, "ultimo duty %s" % (_duties[-1:] or "ninguno"))

print("")
print("=" * 74)
if fallas:
    print("  %d comprobaciones fallaron:" % len(fallas))
    for f in fallas:
        print("    -", f)
else:
    print("  el capitulo 5 pasa la verificacion")
print("=" * 74)
