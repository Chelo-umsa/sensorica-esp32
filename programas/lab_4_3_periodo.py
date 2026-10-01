# -*- coding: utf-8 -*-
from machine import Pin, PWM
import time

PIN_GENERADOR = 25
PIN_CONTADOR = 26

MUESTRAS = 16             # periodos que se promedian
FRECUENCIAS = (2, 10, 50, 200, 1000)

generador = PWM(Pin(PIN_GENERADOR), freq=FRECUENCIAS[0])
generador.duty(512)

entrada = Pin(PIN_CONTADOR, Pin.IN)

ultimo_us = 0
periodo_us = 0


def al_llegar_un_pulso(pin):
    """Anota cuanto paso desde el pulso anterior.

    Se usa ticks_diff y no una resta comun porque el contador de
    microsegundos se da vuelta: una resta directa daria, en ese
    momento, un valor negativo enorme.
    """
    global ultimo_us, periodo_us
    ahora = time.ticks_us()
    if ultimo_us != 0:
        periodo_us = time.ticks_diff(ahora, ultimo_us)
    ultimo_us = ahora


def medir_frecuencia(muestras=MUESTRAS, espera_ms=600):
    """Promedia varios periodos. None si no llego ningun pulso."""
    global periodo_us
    suma = 0
    tomadas = 0
    limite = time.ticks_add(time.ticks_ms(), espera_ms)

    while tomadas < muestras and \
            time.ticks_diff(limite, time.ticks_ms()) > 0:
        if periodo_us > 0:
            suma = suma + periodo_us
            periodo_us = 0
            tomadas = tomadas + 1
        time.sleep_ms(1)

    if tomadas == 0:
        return None
    return 1000000.0 / (suma / tomadas)


def main():
    entrada.irq(trigger=Pin.IRQ_FALLING, handler=al_llegar_un_pulso)
    print("Medicion por periodo, promediando {} pulsos".format(
        MUESTRAS))
    print("")
    print("  generada   medida    error")

    for f in FRECUENCIAS:
        generador.freq(f)
        time.sleep_ms(300)
        medida = medir_frecuencia()

        if medida is None:
            print("  {:6d} Hz  sin pulsos".format(f))
        else:
            error = (medida - f) * 100.0 / f
            print("  {:6d} Hz  {:7.1f} Hz  {:+5.1f} %".format(
                f, medida, error))

    print("")
    print("Este metodo mide bien abajo, donde el conteo se equivocaba.")


if __name__ == "__main__":
    main()
