# -*- coding: utf-8 -*-
from machine import Pin
import time

PIN_DATOS = 16
PIN_RELOJ = 4
INTERVALO = 2

# Calibracion. No son numeros magicos: son los dos puntos de la
# recta del laboratorio 3.5. CERO es lo que entrega el sensor sin
# presion y FONDO lo que entrega a fondo de escala.
CERO = 1037416
FONDO = 8388607
KPA_FONDO = 40.0
KPA_A_PSI = 0.145038

salida = Pin(PIN_DATOS, Pin.IN)
reloj = Pin(PIN_RELOJ, Pin.OUT)
reloj.value(0)


def leer_crudo(espera_ms=200):
    """Los 24 bits del HX710B, o None si el sensor no responde.

    El integrado avisa que tiene un dato listo poniendo su salida
    en cero. Si eso no ocurre dentro del plazo se abandona, en
    lugar de quedar esperando para siempre.
    """
    limite = time.ticks_add(time.ticks_ms(), espera_ms)
    while salida.value() == 1:
        if time.ticks_diff(limite, time.ticks_ms()) <= 0:
            return None
        time.sleep_ms(1)

    dato = 0
    for _ in range(24):
        reloj.value(1)
        dato = (dato << 1) | salida.value()
        reloj.value(0)

    reloj.value(1)          # pulso 25: fija la ganancia de la proxima
    reloj.value(0)

    # Complemento a dos de 24 bits. En Python NO se hace poniendo
    # los bits de arriba: los enteros no tienen tamano y saldria un
    # numero enorme. Se resta el rango completo.
    if dato & 0x800000:
        dato = dato - 0x1000000
    return dato


def presion(crudo):
    """Pasa las cuentas a kPa y a psi, con la recta de calibracion."""
    kpa = (crudo - CERO) * KPA_FONDO / (FONDO - CERO)
    return kpa, kpa * KPA_A_PSI


def main():
    print("HX710B en OUT=GPIO{}  SCK=GPIO{}".format(
        PIN_DATOS, PIN_RELOJ))
    print("Calibracion: {} = 0 kPa, {} = {:.0f} kPa".format(
        CERO, FONDO, KPA_FONDO))
    print("")

    while True:
        crudo = leer_crudo()

        if crudo is None:
            print("El sensor no responde. Revise OUT, SCK y VCC.")
        else:
            kpa, psi = presion(crudo)
            print("{:9d} cuentas   {:7.2f} kPa   {:6.2f} psi".format(
                crudo, kpa, psi))

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
