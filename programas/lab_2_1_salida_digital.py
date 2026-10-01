# -*- coding: utf-8 -*-
from machine import Pin
import time

led = Pin(23, Pin.OUT)

ENCENDIDO_S = 0.5
APAGADO_S = 0.5

while True:
    led.value(1)
    print("encendido")
    time.sleep(ENCENDIDO_S)

    led.value(0)
    print("apagado")
    time.sleep(APAGADO_S)
