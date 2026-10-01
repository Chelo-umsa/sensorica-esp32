# -*- coding: utf-8 -*-
from machine import Pin, PWM
import time

servo = PWM(Pin(4), freq=50)     # 50 Hz: un ciclo cada 20 ms

DUTY_MINIMO = 40                 # unos 0,78 ms, extremo de 0 grados
DUTY_MAXIMO = 115                # unos 2,25 ms, extremo de 180 grados
RECORRIDO = DUTY_MAXIMO - DUTY_MINIMO


def angulo_a_duty(angulo):
    """Convierte un angulo de 0 a 180 grados en ciclo de trabajo.

    Los dos extremos se recortan a proposito. Pedir 200 grados no
    consigue mas recorrido: manda al servo contra su tope, donde
    zumba, se calienta y termina rompiendo el engranaje de salida.
    """
    if angulo < 0:
        angulo = 0
    if angulo > 180:
        angulo = 180
    return int(angulo * RECORRIDO / 180 + DUTY_MINIMO)


for angulo in (0, 45, 90, 135, 180, 90):
    servo.duty(angulo_a_duty(angulo))
    print("{:3d} grados  ->  duty {:3d}".format(
        angulo, angulo_a_duty(angulo)))
    time.sleep(1)

servo.deinit()                   # suelta el pin y deja de mandar pulsos
