# -*- coding: utf-8 -*-
from machine import Pin
import time
import dht
from ble_uart import BLEUART

PIN_DATOS = 14
NOMBRE = "ESP32-TALLER"      # el que va a aparecer en el telefono
INTERVALO = 2                # segundos entre mediciones

sensor = dht.DHT11(Pin(PIN_DATOS))
enlace = BLEUART(NOMBRE)

print("Bluetooth activo como", NOMBRE)
print("Busque ese nombre en la pestana BLE de la aplicacion.")

fallas = 0

while True:
    # Lo que el telefono haya escrito. Puede venir vacio, asi que
    # se comprueba ANTES de decodificar: .decode() sobre nada
    # levanta una excepcion y corta el programa.
    recibido = enlace.read()
    if recibido:
        print("El telefono dice:", recibido.decode().strip())

    try:
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        fallas = 0
    except OSError:
        fallas = fallas + 1
        print("Lectura fallida ({}).".format(fallas))
        time.sleep(INTERVALO)
        continue

    print("Temperatura: {} C   Humedad: {} %".format(
        temperatura, humedad))

    # Escribir sin nadie conectado no da error, pero tampoco sirve:
    # preguntarlo permite avisar en la consola que el telefono se fue.
    if enlace.conectado():
        enlace.write("T:{}C\n".format(temperatura))
        enlace.write("H:{}%\n".format(humedad))
    else:
        print("   (nadie conectado todavia)")

    time.sleep(INTERVALO)
