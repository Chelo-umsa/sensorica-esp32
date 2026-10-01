# -*- coding: utf-8 -*-
from machine import Pin, PWM
import time

servo = PWM(Pin(4), freq=50)

DUTY_MINIMO = 40
DUTY_MAXIMO = 115                # 2,25 ms. Subirlo a 150 da 2,93 ms:
RECORRIDO = DUTY_MAXIMO - DUTY_MINIMO     # el tope mecanico del servo

PASO = 2                         # grados por escalon
ESPERA_MS = 30                   # cuanto se detiene en cada escalon


def angulo_a_duty(angulo):
    """Recorta el angulo ANTES de convertirlo, de modo que ningun
    programa que use esta funcion pueda mandar al servo al tope."""
    if angulo < 0:
        angulo = 0
    if angulo > 180:
        angulo = 180
    return int(angulo * RECORRIDO / 180 + DUTY_MINIMO)


def barrer(desde, hasta):
    paso = PASO if hasta > desde else -PASO
    for angulo in range(desde, hasta + paso, paso):
        servo.duty(angulo_a_duty(angulo))
        time.sleep_ms(ESPERA_MS)


while True:
    barrer(0, 180)
    barrer(180, 0)
    print("Barrido completo")
