# -*- coding: utf-8 -*-
from machine import Pin, ADC
import time

PIN_ENTRADA = 32
MILIVOLTIOS_POR_GRADO = 10.0
MUESTRAS = 16             # promedio para atenuar el ruido del conversor

# Con atenuacion de 6 dB el conversor llega a unos 2,0 V, que serian
# 200 C: de sobra, y con el doble de resolucion que usando los 3,3 V.
TENSION_MAXIMA = 2.0
CUENTAS_MAXIMAS = 4095

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_6DB)
entrada.width(ADC.WIDTH_12BIT)


def leer_milivoltios():
    """Promedia varias lecturas y devuelve la salida en milivoltios."""
    suma = 0
    for _ in range(MUESTRAS):
        suma = suma + entrada.read()
        time.sleep_ms(2)
    cuentas = suma / MUESTRAS
    return cuentas * TENSION_MAXIMA * 1000 / CUENTAS_MAXIMAS


def leer_temperatura():
    return leer_milivoltios() / MILIVOLTIOS_POR_GRADO


def main():
    print("Sensor LM35 en GPIO{}".format(PIN_ENTRADA))
    print("")
    print("  salida      temperatura")

    while True:
        mv = leer_milivoltios()
        print("   {:6.1f} mV    {:5.1f} C".format(
            mv, mv / MILIVOLTIOS_POR_GRADO))
        time.sleep(1)


if __name__ == "__main__":
    main()
