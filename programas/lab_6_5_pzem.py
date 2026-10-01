# -*- coding: utf-8 -*-
from machine import UART
from pzem import PZEM
import time

INTERVALO = 3

uart = UART(1, baudrate=9600, tx=17, rx=16)
medidor = PZEM(uart)

MAGNITUDES = (("Tension", "getVoltage", "{:7.2f} V"),
              ("Corriente", "getCurrent", "{:7.3f} A"),
              ("Potencia activa", "getActivePower", "{:7.2f} W"),
              ("Factor de potencia", "getPowerFactor", "{:7.3f}"))


def potencia_aparente(tension, corriente):
    """Los voltiamperios: lo que la instalacion tiene que soportar."""
    return tension * corriente


def main():
    print("Medidor PZEM-004T")
    print("")

    while True:
        if not medidor.read():
            print("Sin lectura valida. Revise el cableado serie.")
            time.sleep(INTERVALO)
            continue

        valores = []
        for nombre, metodo, formato in MAGNITUDES:
            valor = getattr(medidor, metodo)()
            valores.append(valor)
            print("  {:<20}{}".format(nombre, formato.format(valor)))

        # Lo que el instrumento no da y conviene calcular
        aparente = potencia_aparente(valores[0], valores[1])
        reactiva = (aparente ** 2 - valores[2] ** 2) ** 0.5
        print("  {:<20}{:7.2f} VA".format(
            "Potencia aparente", aparente))
        print("  {:<20}{:7.2f} var".format(
            "Potencia reactiva", reactiva))
        print("")

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
