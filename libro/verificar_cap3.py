# -*- coding: utf-8 -*-
"""Verificacion del capitulo 3, sobre los programas tal como salen impresos.

La calibracion no se ha hecho todavia en el banco, asi que lo que se
comprueba aqui es la ARITMETICA: que las conversiones den lo que dicen
las tablas del capitulo, que los rangos se respeten y que las fallas de
cableado se atrapen en vez de detener el programa.
"""
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


print("=" * 74)
print("  3.1  Lectura analogica basica")
print("=" * 74)

m31, f31 = cargar("programas/lab_3_1_potenciometro.py", "p31")
revisar("usa un pin del ADC1, que sirve con el WiFi encendido",
        32 <= m31.PIN_ENTRADA <= 39)
revisar("fija la atenuacion", "ATTN_11DB" in f31)
revisar("fija la resolucion", "WIDTH_12BIT" in f31)

print("   %8s  %10s" % ("cuentas", "tension"))
for tension_real, cuentas_esp in ((0.0, 0), (1.65, 2047), (3.3, 4095)):
    ADC._simulado[m31.PIN_ENTRADA] = tension_real
    cuentas, tension = m31.leer_tension()
    bien = abs(tension - tension_real) < 0.01
    print("   %8d  %8.3f V   (esperado %.3f)   %s"
          % (cuentas, tension, tension_real, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("3.1 conversion en %.2f V" % tension_real)

print("")
print("=" * 74)
print("  3.2  Divisor de tension")
print("=" * 74)

m32, f32 = cargar("programas/lab_3_2_divisor.py", "p32")
print("   R1 = %.0f, R2 = %.0f  ->  factor %.4f"
      % (m32.R1, m32.R2, m32.FACTOR))
revisar("el factor corresponde a las dos resistencias",
        abs(m32.FACTOR - 25.0 / 15.0) < 1e-9)

# la tabla impresa en el libro
print("   %-12s %-12s %-12s" % ("entrada", "en el pin", "reconstruida"))
for entrada_real in (0.0, 2.5, 5.0):
    en_el_pin_teorico = entrada_real * m32.R2 / (m32.R1 + m32.R2)
    ADC._simulado[m32.PIN_ENTRADA] = en_el_pin_teorico
    en_el_pin, real = m32.leer_entrada()
    bien = abs(real - entrada_real) < 0.02
    print("   %-12.2f %-12.2f %-12.2f  %s"
          % (entrada_real, en_el_pin, real, "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("3.2 reconstruccion de %.1f V" % entrada_real)

revisar("con 5 V a la entrada, en el pin quedan 3,0 V, dentro de lo admisible",
        abs(5.0 * m32.R2 / (m32.R1 + m32.R2) - 3.0) < 0.01)
revisar("el divisor presenta menos de 10 kohm al conversor, como pide el ADC",
        (m32.R1 * m32.R2) / (m32.R1 + m32.R2) <= 10000)

print("")
print("=" * 74)
print("  3.3  LM35, sensor lineal")
print("=" * 74)

m33, f33 = cargar("programas/lab_3_3_lm35.py", "p33")
revisar("usa la atenuacion de 6 dB, que duplica la resolucion",
        "ATTN_6DB" in f33)
revisar("y la constante de tension le corresponde", m33.TENSION_MAXIMA == 2.0)

print("   %-14s %-14s" % ("temperatura", "medida"))
for grados in (0.0, 25.0, 60.0, 100.0):
    ADC._simulado[m33.PIN_ENTRADA] = grados * 0.010     # 10 mV por grado
    medida = m33.leer_temperatura()
    bien = abs(medida - grados) < 0.5
    print("   %-14.1f %-14.2f  %s" % (grados, medida,
                                      "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("3.3 a %.0f C" % grados)

# la tabla de resolucion del capitulo
for atenuacion, tope, esperado in (("11 dB", 3.3, 12.4), ("6 dB", 2.0, 20.5)):
    cuentas_por_grado = 4095 / (tope * 1000 / 10.0)
    bien = abs(cuentas_por_grado - esperado) < 0.15
    print("   con %s: %.1f cuentas por grado  (el libro dice %.1f)   %s"
          % (atenuacion, cuentas_por_grado, esperado,
             "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("3.3 tabla de resolucion, %s" % atenuacion)

print("")
print("=" * 74)
print("  3.4  Termistor NTC")
print("=" * 74)

m34, f34 = cargar("programas/lab_3_4_termistor.py", "p34")
revisar("la resistencia fija vale lo mismo que el nominal del termistor",
        m34.R_FIJA == m34.R_NOMINAL)


def tension_del_ntc(grados, m):
    """La tension que entregaria el divisor a esa temperatura."""
    t = grados + m.CERO_ABSOLUTO
    t0 = m.T_NOMINAL + m.CERO_ABSOLUTO
    r = m.R_NOMINAL * math.exp(m.BETA * (1.0 / t - 1.0 / t0))
    return m.ALIMENTACION * r / (m.R_FIJA + r), r


print("   %-12s %-14s %-12s" % ("temperatura", "resistencia", "medida"))
for grados in (0.0, 25.0, 50.0, 80.0):
    tension, r_teorica = tension_del_ntc(grados, m34)
    ADC._simulado[m34.PIN_ENTRADA] = tension
    v = m34.leer_tension()
    r = m34.resistencia_del_ntc(v)
    medida = m34.temperatura(r) if r else None
    bien = medida is not None and abs(medida - grados) < 1.0
    print("   %-12.1f %-14.0f %-12s  %s"
          % (grados, r_teorica,
             "%.1f" % medida if medida is not None else "None",
             "ok" if bien else "FALLA"))
    if not bien:
        fallas.append("3.4 a %.0f C" % grados)

revisar("a 25 C el termistor vale su valor nominal",
        abs(tension_del_ntc(25.0, m34)[1] - m34.R_NOMINAL) < 1)

# las fallas de cableado no pueden detener el programa
revisar("sensor desconectado: devuelve None en vez de dividir por cero",
        m34.resistencia_del_ntc(m34.ALIMENTACION) is None)
revisar("sensor en corto: devuelve None en vez de tomar el logaritmo de cero",
        m34.resistencia_del_ntc(0.0) is None)

# la no linealidad, que es la leccion del laboratorio
r20 = tension_del_ntc(20.0, m34)[1]
r30 = tension_del_ntc(30.0, m34)[1]
r75 = tension_del_ntc(75.0, m34)[1]
r85 = tension_del_ntc(85.0, m34)[1]
print("   entre 20 y 30 C la resistencia cambia %.0f ohm" % (r20 - r30))
print("   entre 75 y 85 C, los mismos 10 grados mueven %.0f ohm" % (r75 - r85))
revisar("el mismo salto de temperatura mueve mucho menos en caliente: "
        "eso es la no linealidad", (r20 - r30) > 10 * (r75 - r85))

print("")
print("=" * 74)
print("  3.5  Calibracion de dos puntos")
print("=" * 74)

m35, f35 = cargar("programas/lab_3_5_calibracion.py", "p35")

# una recta conocida: 0 cuentas -> 0 C, 4000 cuentas -> 100 C
pend, ordenada = m35.recta_de_calibracion(0, 0.0, 4000, 100.0)
print("   dos puntos (0, 0 C) y (4000, 100 C) -> pendiente %.5f, "
      "ordenada %.3f" % (pend, ordenada))
revisar("la recta pasa por los dos puntos",
        abs(m35.aplicar(0, pend, ordenada) - 0.0) < 1e-9
        and abs(m35.aplicar(4000, pend, ordenada) - 100.0) < 1e-9)
revisar("y el punto medio cae donde corresponde",
        abs(m35.aplicar(2000, pend, ordenada) - 50.0) < 1e-9)

# una recta con desvio de cero, que es el caso real
pend2, ord2 = m35.recta_de_calibracion(200, 0.0, 4000, 100.0)
revisar("con desvio de cero, la ordenada deja de ser nula", abs(ord2) > 1)
revisar("y la recta sigue pasando por los dos puntos",
        abs(m35.aplicar(200, pend2, ord2)) < 1e-9
        and abs(m35.aplicar(4000, pend2, ord2) - 100.0) < 1e-9)

# dos puntos iguales: no hay recta posible
try:
    m35.recta_de_calibracion(100, 0.0, 100, 50.0)
    revisar("dos puntos con la misma lectura se rechazan", False,
            "no levanto ninguna excepcion")
except ValueError:
    revisar("dos puntos con la misma lectura se rechazan", True)

# la mediana resiste un pico; el promedio no
import machine
_lecturas = [2000] * 14 + [4095]
_i = [0]


def _falsa(s):
    v = _lecturas[_i[0] % len(_lecturas)]
    _i[0] += 1
    return v


_orig = machine.ADC.read
machine.ADC.read = _falsa
_i[0] = 0
promedio = m35.leer_promedio(15, 0)
_i[0] = 0
mediana = m35.leer_mediana(15, 0)
machine.ADC.read = _orig

print("   catorce lecturas de 2000 y un pico de 4095:")
print("      promedio %.1f      mediana %.1f" % (promedio, mediana))
revisar("la mediana ignora el pico", mediana == 2000)
revisar("el promedio se deja arrastrar", promedio > 2100)

print("")
print("=" * 74)
if fallas:
    print("  %d comprobaciones fallaron:" % len(fallas))
    for f in fallas:
        print("    -", f)
else:
    print("  el capitulo 3 pasa la verificacion de aritmetica")
print("=" * 74)
