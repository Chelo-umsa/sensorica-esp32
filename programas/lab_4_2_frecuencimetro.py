# -*- coding: utf-8 -*-
from machine import Pin, PWM
import machine
import time

PIN_GENERADOR = 25
PIN_CONTADOR = 26

VENTANA_MS = 1000         # duracion de cada medicion
FRECUENCIAS = (10, 50, 200, 1000, 5000)

generador = PWM(Pin(PIN_GENERADOR), freq=FRECUENCIAS[0])
generador.duty(512)

entrada = Pin(PIN_CONTADOR, Pin.IN)

pulsos = 0


def contar(pin):
    global pulsos
    pulsos = pulsos + 1


def tomar_pulsos():
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta


def medir_frecuencia(ventana_ms=VENTANA_MS):
    """Cuenta los pulsos de una ventana y los pasa a hercios."""
    tomar_pulsos()                      # arranca de cero
    time.sleep_ms(ventana_ms)
    return tomar_pulsos() * 1000.0 / ventana_ms


def main():
    entrada.irq(trigger=Pin.IRQ_FALLING, handler=contar)
    print("Frecuencimetro por conteo, ventana de {} ms".format(
        VENTANA_MS))
    print("")
    print("  generada   medida    error")

    for f in FRECUENCIAS:
        generador.freq(f)
        time.sleep_ms(200)              # deja que se asiente
        medida = medir_frecuencia()
        error = (medida - f) * 100.0 / f
        print("  {:6d} Hz  {:7.1f} Hz  {:+5.1f} %".format(
            f, medida, error))

    resolucion = 1000.0 / VENTANA_MS
    print("")
    print("Con {} ms de ventana no se baja de {:.1f} Hz.".format(
        VENTANA_MS, resolucion))
    print("Por eso el error relativo es grande abajo y chico arriba.")


if __name__ == "__main__":
    main()
