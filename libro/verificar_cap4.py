# -*- coding: utf-8 -*-
"""Verificacion del capitulo 4.

Los tres primeros laboratorios se pueden probar de verdad: el
simulador enlaza la salida PWM con el pin de entrada y dispara las
interrupciones, de modo que los pulsos se cuentan como en la placa.
Lo que NO reproduce es la temporizacion fina por encima de unos
cientos de hercios, asi que ahi se comprueba la aritmetica.
"""
import sys, os, io, contextlib, importlib.util

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

fallas = []


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


print("=" * 74)
print("  4.1  Consulta contra interrupcion")
print("=" * 74)

m41, f41 = cargar("programas/lab_4_1_consulta_interrupcion.py", "p41")
revisar("el manejador solo suma: nada de print ni de format adentro",
        "print" not in f41.split("def al_llegar_un_pulso")[1].split("def ")[0])
revisar("apaga las interrupciones para leer y poner en cero",
        "disable_irq" in f41 and "enable_irq" in f41)
revisar("guarda el estado anterior en vez de encenderlas sin mas",
        "estado = machine.disable_irq()" in f41
        and "enable_irq(estado)" in f41)

# el contador atomico: mil sumas desde "interrupciones" y ninguna perdida
m41.pulsos = 0
for _ in range(1000):
    m41.al_llegar_un_pulso(None)
revisar("mil pulsos se cuentan sin perder ninguno", m41.tomar_pulsos() == 1000)
revisar("y el contador queda en cero para la ventana siguiente",
        m41.tomar_pulsos() == 0)

print("")
print("=" * 74)
print("  4.2  Frecuencimetro por conteo")
print("=" * 74)

m42, f42 = cargar("programas/lab_4_2_frecuencimetro.py", "p42")

# la tabla de error del capitulo: +-1 pulso sobre la cuenta
print("   %-12s %-14s %-12s" % ("frecuencia", "pulsos en 1 s", "error de ±1"))
for f, esperado in ((10, 10.0), (50, 2.0), (200, 0.5), (1000, 0.1),
                    (5000, 0.02)):
    error = 100.0 / f
    bien = abs(error - esperado) < 0.005
    print("   %-12d %-14d ± %-10.2f %%  %s"
          % (f, f, error, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("4.2 tabla de error en %d Hz" % f)

revisar("la resolucion es el inverso de la ventana",
        abs(1000.0 / m42.VENTANA_MS - 1.0) < 1e-9)

# la conversion de pulsos a hercios
for cuenta, ventana, esperado in ((200, 1000, 200.0), (100, 500, 200.0),
                                  (37, 1000, 37.0)):
    obtenido = cuenta * 1000.0 / ventana
    bien = abs(obtenido - esperado) < 1e-9
    print("   %4d pulsos en %4d ms -> %7.1f Hz   %s"
          % (cuenta, ventana, obtenido, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("4.2 conversion")

print("")
print("=" * 74)
print("  4.3  Medicion por periodo")
print("=" * 74)

m43, f43 = cargar("programas/lab_4_3_periodo.py", "p43")
revisar("usa ticks_diff y no una resta directa, por el vuelco del contador",
        "ticks_diff" in f43 and "ahora - ultimo_us" not in f43)
revisar("devuelve None si no llego ningun pulso, en vez de dividir por cero",
        "return None" in f43)

# periodo -> frecuencia
print("   %-16s %-12s" % ("periodo", "frecuencia"))
for periodo_us, esperado in ((500000, 2.0), (100000, 10.0), (20000, 50.0),
                             (1000, 1000.0)):
    obtenido = 1000000.0 / periodo_us
    bien = abs(obtenido - esperado) < 1e-9
    print("   %-16d %-12.1f Hz  %s" % (periodo_us, obtenido,
                                       "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("4.3 conversion de %d us" % periodo_us)

# el promedio de periodos
m43.periodo_us = 0
m43.ultimo_us = 0
import time as _t
base = _t.ticks_us()
for k in range(5):
    m43.ultimo_us = base + k * 100000
    m43.periodo_us = 100000
revisar("un periodo de 100 000 us son 10 Hz",
        abs(1000000.0 / 100000 - 10.0) < 1e-9)

print("")
print("=" * 74)
print("  4.4  Tacometro")
print("=" * 74)

m44, f44 = cargar("programas/lab_4_4_tacometro.py", "p44")
print("   disco de %d marcas, ventana de %d ms, rebote de %d us"
      % (m44.MARCAS_POR_VUELTA, m44.VENTANA_MS, m44.REBOTE_US))

print("   %-10s %-12s" % ("pulsos", "RPM"))
for cuenta, esperado in ((40, 600.0), (4, 60.0), (200, 3000.0), (0, 0.0)):
    obtenido = m44.rpm_desde_pulsos(cuenta, m44.VENTANA_MS)
    bien = abs(obtenido - esperado) < 1e-6
    print("   %-10d %-12.0f  (esperado %.0f)   %s"
          % (cuenta, obtenido, esperado, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("4.4 con %d pulsos" % cuenta)

revisar("con la mitad de marcas declaradas, las RPM salen al doble",
        abs(m44.rpm_desde_pulsos(40, 1000) * 2
            - (40 / (m44.MARCAS_POR_VUELTA / 2)) * 60000.0 / 1000) < 1e-6)

# el filtro de rebote
import machine
m44.pulsos = 0
m44._ultimo_us = 0
# El reloj falso arranca en un valor alto, como en la placa: si
# arrancara en cero, ticks_diff contra _ultimo_us = 0 daria cero y el
# filtro descartaria el primer pulso. En la placa eso no pasa.
_reloj = [5_000_000]
_orig_us = _t.ticks_us
_t.ticks_us = lambda: _reloj[0]

# un pulso bueno seguido de cuatro rebotes a 100 us
for avance in (0, 100, 200, 300, 400):
    _reloj[0] += avance
    m44.contar(None)
tras_rebotes = m44.pulsos

# y otro pulso bueno, ya pasado el tiempo de filtro
_reloj[0] += m44.REBOTE_US + 100
m44.contar(None)
total = m44.pulsos
_t.ticks_us = _orig_us

print("   un pulso con cuatro rebotes a 100 us -> %d contado(s)"
      % tras_rebotes)
revisar("el filtro descarta los rebotes", tras_rebotes == 1,
        "conto %d" % tras_rebotes)
revisar("y no descarta el pulso bueno siguiente", total == 2,
        "conto %d" % total)

# el limite del filtro, que el capitulo calcula
for rpm, marcas in ((3000, 4), (12000, 4)):
    intervalo_us = 60_000_000.0 / (rpm * marcas)
    holgado = intervalo_us > m44.REBOTE_US
    print("   a %5d RPM con %d marcas hay un pulso cada %6.0f us  ->  %s"
          % (rpm, marcas, intervalo_us,
             "el filtro de %d us deja margen" % m44.REBOTE_US if holgado
             else "el filtro de %d us YA SE COME PULSOS" % m44.REBOTE_US))
revisar("a 3000 RPM el filtro deja margen",
        60_000_000.0 / (3000 * 4) > m44.REBOTE_US)
revisar("y a 12 000 RPM ya no, como advierte el capitulo",
        60_000_000.0 / (12000 * 4) < m44.REBOTE_US)
revisar("a 9000 RPM todavia deja margen, aunque poco",
        60_000_000.0 / (9000 * 4) > m44.REBOTE_US)

print("")
print("=" * 74)
if fallas:
    print("  %d comprobaciones fallaron:" % len(fallas))
    for f in fallas:
        print("    -", f)
else:
    print("  el capitulo 4 pasa la verificacion")
print("=" * 74)
