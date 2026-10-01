# -*- coding: utf-8 -*-
from machine import Pin
import time

# El puente del modulo decide con que nivel dispara. En L —lo mas
# comun— el rele se activa con un 0. Cambiando esta linea el programa
# sirve para los dos, y no hay que tocar nada mas.
ACTIVO_EN_BAJO = True

REBOTE_MS = 50

rele = Pin(19, Pin.OUT)
boton = Pin(16, Pin.IN, Pin.PULL_UP)

estado = False
ultimo_cambio = time.ticks_ms()


def mandar(encendido):
    """Traduce 'encendido' al nivel que pide este modulo."""
    if ACTIVO_EN_BAJO:
        rele.value(0 if encendido else 1)
    else:
        rele.value(1 if encendido else 0)


mandar(False)          # apagado antes que nada, pase lo que pase

print("Mantenga presionado para encender. Ctrl+C para salir.")

while True:
    # Con PULL_UP el pulsador en reposo lee 1 y presionado lee 0.
    presionado = not boton.value()
    ahora = time.ticks_ms()

    hubo_cambio = presionado != estado
    paso_el_rebote = time.ticks_diff(ahora, ultimo_cambio) > REBOTE_MS

    if hubo_cambio and paso_el_rebote:
        estado = presionado
        ultimo_cambio = ahora
        mandar(estado)
        print("foco encendido" if estado else "foco apagado")

    time.sleep_ms(10)
