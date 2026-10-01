# -*- coding: utf-8 -*-
import time
from machine import Pin
import urequests
import dht
import iot
import config

PIN_DATOS = 14
INTERVALO = 10            # aqui no hay limite de datos por minuto

sensor = dht.DHT11(Pin(PIN_DATOS))

URL = "http://{}:8086/api/v2/write?org={}&bucket={}&precision=s".format(
    config.INFLUX_HOST, config.INFLUX_ORG, config.INFLUX_BUCKET)

CABECERAS = {"Authorization": "Token " + config.INFLUX_TOKEN,
             "Content-Type": "text/plain"}


def escribir(temperatura, humedad):
    """Manda una linea a InfluxDB. Devuelve True si la acepto.

    La respuesta se cierra SIEMPRE. En MicroPython una respuesta sin
    cerrar deja el socket tomado, y despues de unas cuantas el
    programa se queda sin ninguno y deja de poder publicar.
    """
    linea = "ambiente temperatura={},humedad={}".format(
        temperatura, humedad)
    respuesta = None
    try:
        respuesta = urequests.post(URL, data=linea, headers=CABECERAS)
        return respuesta.status_code in (200, 204)
    except OSError as e:
        print("No se pudo escribir:", e)
        return False
    finally:
        if respuesta is not None:
            respuesta.close()


def main():
    iot.conectar_wifi()
    print("Escribiendo en", URL)

    while True:
        try:
            sensor.measure()
            temperatura = sensor.temperature()
            humedad = sensor.humidity()
        except OSError:
            print("Lectura fallida. Se reintenta.")
            time.sleep(INTERVALO)
            continue

        if escribir(temperatura, humedad):
            print("{} C   {} %   anotado".format(temperatura, humedad))
        else:
            print("{} C   {} %   NO se pudo anotar".format(
                temperatura, humedad))

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
