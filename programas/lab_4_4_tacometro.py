# -*- coding: utf-8 -*-
from machine import Pin, PWM
import machine
import time

PIN_SENSOR = 17
MARCAS_POR_VUELTA = 4     # las que tenga SU disco. Ver el razonamiento.

ENA = PWM(Pin(19), freq=1000)
IN1 = Pin(18, Pin.OUT)
IN2 = Pin(5, Pin.OUT)
IN1.on()
IN2.off()                 # sentido de giro fijo
ENA.duty(0)

sensor = Pin(PIN_SENSOR, Pin.IN)

VENTANA_MS = 1000
REBOTE_US = 1500          # descarta los rebotes del comparador

pulsos = 0
_ultimo_us = 0


def contar(pin):
    """Suma un pulso, descartando los rebotes del comparador."""
    global pulsos, _ultimo_us
    ahora = time.ticks_us()
    if time.ticks_diff(ahora, _ultimo_us) > REBOTE_US:
        pulsos = pulsos + 1
        _ultimo_us = ahora


def tomar_pulsos():
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta


def rpm_desde_pulsos(cuenta, ventana_ms):
    """Pasa una cuenta de pulsos a revoluciones por minuto."""
    vueltas = cuenta / MARCAS_POR_VUELTA
    return vueltas * 60000.0 / ventana_ms


def main():
    sensor.irq(trigger=Pin.IRQ_FALLING, handler=contar)
    print("Tacometro. Disco de {} marcas.".format(MARCAS_POR_VUELTA))
    print("")
    print("  velocidad   pulsos      RPM")

    for porcentaje in (40, 60, 80, 100, 0):
        ENA.duty(int(porcentaje * 1023 / 100))
        time.sleep_ms(600)              # deja que el motor se acomode
        tomar_pulsos()                  # descarta lo del transitorio

        time.sleep_ms(VENTANA_MS)
        cuenta = tomar_pulsos()

        print("   {:3d} %      {:4d}    {:7.0f}".format(
            porcentaje, cuenta, rpm_desde_pulsos(cuenta, VENTANA_MS)))

    ENA.duty(0)
    sensor.irq(handler=None)
    print("")
    print("Motor detenido.")


if __name__ == "__main__":
    main()
