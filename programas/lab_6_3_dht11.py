# -*- coding: utf-8 -*-
from machine import Pin
import time
import dht

PIN_DATOS = 14
INTERVALO = 2             # segundos. El DHT11 no admite menos.
AVISAR_TRAS = 5           # fallas seguidas antes de sospechar del cable

sensor = dht.DHT11(Pin(PIN_DATOS))


def leer():
    """Temperatura y humedad, o None si la trama llego mal.

    La suma de verificacion del DHT11 falla cada tanto y no
    significa que el sensor este malo: hay que pedir otra trama.
    Sin este try, el programa se detiene.
    """
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError:
        return None


def main():
    print("DHT11 en GPIO{}".format(PIN_DATOS))
    print("")
    fallas = 0

    while True:
        lectura = leer()

        if lectura is None:
            fallas = fallas + 1
            print("Lectura fallida ({}).".format(fallas))
            if fallas == AVISAR_TRAS:
                print("Varias seguidas: revise el cable y la")
                print("resistencia de elevacion en la linea.")
        else:
            temperatura, humedad = lectura
            fallas = 0
            print("Temperatura: {} C    Humedad: {} %".format(
                temperatura, humedad))

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
