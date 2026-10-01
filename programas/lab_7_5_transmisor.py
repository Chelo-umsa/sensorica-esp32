# -*- coding: utf-8 -*-
import network
import espnow
from machine import Pin
import time

PAREJA = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # <-- la MAC de la receptora
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

    time.sleep_ms(10)
