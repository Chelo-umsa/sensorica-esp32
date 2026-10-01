# -*- coding: utf-8 -*-
from machine import Pin, ADC
import math
import time

PIN_ENTRADA = 33

R_FIJA = 100000.0         # ohmios, la resistencia de arriba
R_NOMINAL = 100000.0      # ohmios del termistor a T_NOMINAL
T_NOMINAL = 25.0          # grados centigrados
BETA = 3950.0             # kelvin, constante del material

ALIMENTACION = 3.3
CERO_ABSOLUTO = 273.15
CUENTAS_MAXIMAS = 4095
MUESTRAS = 16

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)
entrada.width(ADC.WIDTH_12BIT)


def leer_tension():
    suma = 0
    for _ in range(MUESTRAS):
        suma = suma + entrada.read()
        time.sleep_ms(2)
    return (suma / MUESTRAS) * ALIMENTACION / CUENTAS_MAXIMAS


def resistencia_del_ntc(tension):
    """Despeja la resistencia. None si el sensor esta desconectado."""
    if tension <= 0 or tension >= ALIMENTACION:
        return None
    return R_FIJA * tension / (ALIMENTACION - tension)


def temperatura(resistencia):
    """Aplica la ecuacion de Beta. Devuelve grados centigrados."""
    t0 = T_NOMINAL + CERO_ABSOLUTO
    inversa = 1.0 / t0 + math.log(resistencia / R_NOMINAL) / BETA
    return 1.0 / inversa - CERO_ABSOLUTO


def main():
    print("Termistor NTC de {:.0f}k, Beta {:.0f}".format(
        R_NOMINAL / 1000, BETA))
    print("")
    print("  tension   resistencia   temperatura")

    while True:
        tension = leer_tension()
        r = resistencia_del_ntc(tension)

        if r is None:
            print("   {:5.3f} V    sensor desconectado".format(tension))
        else:
            print("   {:5.3f} V   {:8.0f} ohm   {:5.1f} C".format(
                tension, r, temperatura(r)))

        time.sleep(1)


if __name__ == "__main__":
    main()
