# -*- coding: utf-8 -*-
from machine import Pin
import time
import dht
import iot

PIN_DATOS = 14
INTERVALO = 15            # segundos. Ver el recuadro del limite.

sensor = dht.DHT11(Pin(PIN_DATOS))
TEMA_TEMP = iot.feed("temperatura")
TEMA_HUM = iot.feed("humedad")


def leer_sensor():
    """Temperatura y humedad, o None si la trama falla."""
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError:
        return None


def main():
    iot.conectar_wifi()
    cliente = iot.conectar_adafruit("esp32_dht11")
    fallas = 0

    while True:
        lectura = leer_sensor()

        if lectura is None:
            fallas = fallas + 1
            print("Lectura fallida ({}). Se reintenta.".format(fallas))
        else:
            temperatura, humedad = lectura
            fallas = 0
            print("Temperatura: {} C   Humedad: {} %".format(
                temperatura, humedad))
            try:
                cliente.publish(TEMA_TEMP, str(temperatura))
                cliente.publish(TEMA_HUM, str(humedad))
            except Exception as e:
                # La conexion se cayo. Se vuelve a abrir en vez de
                # detener el programa: un equipo que queda corriendo
                # semanas no puede pararse porque se reinicio el router.
                print("No se pudo publicar:", e)
                cliente = iot.conectar_adafruit("esp32_dht11")

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
