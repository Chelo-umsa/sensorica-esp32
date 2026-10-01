# -*- coding: utf-8 -*-
from machine import Pin
import time

rojo = Pin(23, Pin.OUT)
amarillo = Pin(21, Pin.OUT)
verde = Pin(17, Pin.OUT)

SEGUNDOS_ROJO = 5
SEGUNDOS_VERDE = 5
SEGUNDOS_AMARILLO = 2


def encender(cual, segundos, mensaje):
    """Deja encendida una sola luz y apaga las otras dos.

    Fijar las tres en la misma instruccion es lo que garantiza que
    en ningun instante haya dos encendidas a la vez.
    """
    rojo.value(1 if cual is rojo else 0)
    amarillo.value(1 if cual is amarillo else 0)
    verde.value(1 if cual is verde else 0)
    print(mensaje)
    time.sleep(segundos)


while True:
    encender(rojo, SEGUNDOS_ROJO, "Rojo - alto")
    encender(verde, SEGUNDOS_VERDE, "Verde - avance")
    encender(amarillo, SEGUNDOS_AMARILLO, "Amarillo - precaucion")
