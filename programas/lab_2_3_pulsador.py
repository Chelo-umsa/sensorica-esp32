# -*- coding: utf-8 -*-
from machine import Pin
import time

pulsador = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(5, Pin.OUT)

REBOTE_MS = 50

encendido = False
estaba_pulsado = False
ultimo_cambio = time.ticks_ms()

print("Pulse el boton para encender y apagar el LED.")

while True:
    pulsado = not pulsador.value()      # el pulsador une el pin a masa
    ahora = time.ticks_ms()

    hubo_cambio = pulsado != estaba_pulsado
    paso_el_rebote = time.ticks_diff(ahora, ultimo_cambio) > REBOTE_MS

    if hubo_cambio and paso_el_rebote:
        estaba_pulsado = pulsado
        ultimo_cambio = ahora

        # Solo interesa cuando se presiona, no cuando se suelta.
        if pulsado:
            encendido = not encendido
            led.value(1 if encendido else 0)
            print("LED encendido" if encendido else "LED apagado")

    time.sleep_ms(10)
