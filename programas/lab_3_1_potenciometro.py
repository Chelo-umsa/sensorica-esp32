# -*- coding: utf-8 -*-
from machine import Pin, ADC
import time

# El ADC1 corresponde a los pines GPIO32 a GPIO39. Ver el recuadro.
PIN_ENTRADA = 34

TENSION_MAXIMA = 3.3      # con atenuacion de 11 dB
CUENTAS_MAXIMAS = 4095    # con resolucion de 12 bits

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)      # rango de entrada de 0 a 3,3 V
entrada.width(ADC.WIDTH_12BIT)    # resolucion de 12 bits


def leer_tension():
    """Devuelve las cuentas crudas y su equivalente en voltios."""
    cuentas = entrada.read()
    return cuentas, cuentas * TENSION_MAXIMA / CUENTAS_MAXIMAS


def main():
    print("Gire la perilla del potenciometro.")
    print("")
    print("  cuentas   tension     barra")

    while True:
        cuentas, tension = leer_tension()

        # una barra de veinticuatro posiciones para ver la variacion
        largo = int(cuentas * 24 / CUENTAS_MAXIMAS)
        barra = "#" * largo + "." * (24 - largo)

        print("   {:5d}    {:5.3f} V    {}".format(
            cuentas, tension, barra))
        time.sleep(0.5)


if __name__ == "__main__":
    main()
