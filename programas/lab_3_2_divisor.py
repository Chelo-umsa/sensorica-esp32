# -*- coding: utf-8 -*-
from machine import Pin, ADC
import time

PIN_ENTRADA = 35

R1 = 10000.0              # ohmios, del cursor al punto medio
R2 = 15000.0              # ohmios, del punto medio a masa
FACTOR = (R1 + R2) / R2   # cuanto hay que multiplicar para
                          # recuperar la tension original

TENSION_MAXIMA = 3.3
CUENTAS_MAXIMAS = 4095

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)
entrada.width(ADC.WIDTH_12BIT)


def leer_entrada():
    """Devuelve la tension en el pin y la tension real de la senal."""
    cuentas = entrada.read()
    en_el_pin = cuentas * TENSION_MAXIMA / CUENTAS_MAXIMAS
    return en_el_pin, en_el_pin * FACTOR


def main():
    print("Divisor de {:.0f}k / {:.0f}k, factor {:.3f}".format(
        R1 / 1000, R2 / 1000, FACTOR))
    print("")
    print("  en el pin    senal real")

    while True:
        en_el_pin, real = leer_entrada()

        aviso = ""
        if en_el_pin > 3.1:
            aviso = "   <-- revise el divisor"

        print("   {:5.3f} V     {:5.3f} V{}".format(
            en_el_pin, real, aviso))
        time.sleep(0.5)


if __name__ == "__main__":
    main()
