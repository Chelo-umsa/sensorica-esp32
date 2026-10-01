# -*- coding: utf-8 -*-
from machine import Pin, PWM, ADC
import time

led = PWM(Pin(18), freq=1000)
led.duty(0)

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)      # rango de entrada de 0 a 3,3 V

DUTY_MAXIMO = 1023            # duty() trabaja con 10 bits

while True:
    cuentas = pot.read()      # 0 a 4095, porque el ADC tiene 12 bits

    # Cuatro mil noventa y seis niveles no entran en mil veinticuatro.
    # Desplazar dos lugares a la derecha divide entre cuatro y ajusta
    # una escala a la otra sin perder el extremo: 4095 >> 2 da 1023.
    brillo = cuentas >> 2

    led.duty(brillo)
    print("Perilla: {:4d}    Brillo: {:4d}  ({:3.0f} %)".format(
        cuentas, brillo, brillo * 100 / DUTY_MAXIMO))
    time.sleep(0.1)
