# -*- coding: utf-8 -*-
from machine import Pin, PWM
import time

buzzer = PWM(Pin(5))
buzzer.duty_u16(0)              # arranca en silencio
pir = Pin(4, Pin.IN)

TONOS = (400, 800)              # Hz, se alternan para formar la sirena
TRAMO_MS = 200
MITAD = 32767                   # media escala de duty_u16

print("Alarma activa. Espere un minuto a que el PIR se estabilice.")

tono = 0
cambio = time.ticks_ms()
sonando = False

while True:
    hay_movimiento = pir.value() == 1
    ahora = time.ticks_ms()

    if hay_movimiento:
        if not sonando:
            print("Movimiento detectado")
            sonando = True
            buzzer.duty_u16(MITAD)

        # se cambia de tono cada tramo, sin detener el programa
        if time.ticks_diff(ahora, cambio) >= TRAMO_MS:
            tono = 1 - tono
            buzzer.freq(TONOS[tono])
            cambio = ahora
    else:
        if sonando:
            print("Sin movimiento")
            sonando = False
            buzzer.duty_u16(0)

    time.sleep_ms(20)
