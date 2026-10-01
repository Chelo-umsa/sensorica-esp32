# -*- coding: utf-8 -*-
# iot.py — conexion a la red, compartida por todo el capitulo
import time
import network
from umqtt.robust import MQTTClient
import config

SERVIDOR = "io.adafruit.com"
PUERTO = 1883


def conectar_wifi(intentos=20):
    """Conecta el ESP32 a la red. Devuelve la direccion IP."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando a la red", config.WIFI_SSID, "...")
        wlan.connect(config.WIFI_SSID, config.WIFI_CLAVE)
        for _ in range(intentos * 2):
            if wlan.isconnected():
                break
            time.sleep(0.5)

    if not wlan.isconnected():
        raise OSError("No se pudo conectar. Revise config.py")

    ip = wlan.ifconfig()[0]
    print("Red conectada. IP:", ip)
    return ip


def conectar_adafruit(identificador):
    """Abre la sesion MQTT con Adafruit IO. Devuelve el cliente."""
    cliente = MQTTClient(client_id=identificador,
                         server=SERVIDOR,
                         port=PUERTO,
                         user=config.AIO_USUARIO,
                         password=config.AIO_CLAVE,
                         keepalive=60)
    cliente.connect()
    print("Conectado a Adafruit IO como", config.AIO_USUARIO)
    return cliente


def feed(nombre):
    """Devuelve el topico MQTT que corresponde a un feed."""
    return "{}/feeds/{}".format(config.AIO_USUARIO, nombre)
