# -*- coding: utf-8 -*-
from machine import Pin
import time

led = Pin(2, Pin.OUT)          # el LED que la placa trae soldado

while True:
    led.value(1)               # encender
    print("encendido")
    time.sleep(0.5)

    led.value(0)               # apagar
    print("apagado")
    time.sleep(0.5)
