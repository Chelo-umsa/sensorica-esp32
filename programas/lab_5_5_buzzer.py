# -*- coding: utf-8 -*-
from machine import Pin, PWM
import time

buzzer = PWM(Pin(5))
buzzer.duty_u16(0)              # arranca en silencio

MITAD = 32767                   # 50 % de 65535: onda cuadrada simetrica
NOTAS = (("do", 262), ("re", 294), ("mi", 330), ("fa", 349),
         ("sol", 392), ("la", 440), ("si", 494))

try:
    print("Escala")
    buzzer.duty_u16(MITAD)
    for nombre, hz in NOTAS:
        buzzer.freq(hz)
        print("  {:4s} {:3d} Hz".format(nombre, hz))
        time.sleep_ms(400)

    print("Sirena. Interrumpa con Ctrl+C.")
    while True:
        for hz in (400, 800):
            buzzer.freq(hz)
            time.sleep_ms(200)

except KeyboardInterrupt:
    pass

finally:
    # Pase lo que pase, el zumbador queda callado. Sin esto, una
    # interrupcion a mitad de un tono lo deja sonando hasta que
    # alguien reinicie la placa.
    buzzer.duty_u16(0)
    buzzer.deinit()
    print("Silencio.")
