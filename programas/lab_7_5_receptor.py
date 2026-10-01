# -*- coding: utf-8 -*-
import network
import espnow
from machine import Pin
import time

MENSAJE = b"alarma"
DURACION_MS = 2000

buzzer = Pin(4, Pin.OUT)
buzzer.off()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()

enlace = espnow.ESPNow()
enlace.active(True)

print("Receptor listo. Esperando mensajes...")

callar_en = 0

while True:
    # Espera hasta 50 ms por un mensaje. Si no llega ninguno
    # devuelve None y el programa sigue: nunca queda bloqueado.
    quien, mensaje = enlace.recv(50)

    if mensaje == MENSAJE:
        origen = ":".join("{:02X}".format(b) for b in quien)
        print("Alarma recibida desde", origen)
        buzzer.on()
        callar_en = time.ticks_add(time.ticks_ms(), DURACION_MS)

    elif mensaje is not None:
        print("Mensaje desconocido:", mensaje)

    # El zumbador se calla por reloj, no por espera: mientras suena,
    # el programa sigue atendiendo mensajes.
    if callar_en and time.ticks_diff(time.ticks_ms(), callar_en) >= 0:
        buzzer.off()
        callar_en = 0
