# -*- coding: utf-8 -*-
import time
import iot
from machine import Pin

PIN_RELE = 19
ACTIVO_EN_BAJO = True         # el puente H/L del modulo, como en el 2.5
FEED = "foco"
PING_MS = 30000                # la mitad del keepalive de iot.py

rele = Pin(PIN_RELE, Pin.OUT)
encendido = False


def mandar(estado):
    global encendido
    encendido = estado
    if ACTIVO_EN_BAJO:
        rele.value(0 if estado else 1)
    else:
        rele.value(1 if estado else 0)
    print("rele", "encendido" if estado else "apagado")


def atender(topico, mensaje):
    """La llama el cliente MQTT cuando llega algo del feed.

    Los dos argumentos vienen en bytes y no en texto. Y el valor que
    manda el bloque interruptor es "1" o "0" segun como se lo haya
    configurado: cualquier otra cosa se ignora en lugar de darla por
    buena, que con una carga de 220 V no es lo mismo.
    """
    orden = mensaje.decode().strip()
    if orden == "1":
        mandar(True)
    elif orden == "0":
        mandar(False)
    else:
        print("orden desconocida, se ignora:", orden)


def main():
    mandar(False)              # apagado antes de escuchar a nadie
    iot.conectar_wifi()

    cliente = iot.conectar_adafruit("esp32-rele")
    cliente.set_callback(atender)
    cliente.subscribe(iot.feed(FEED))

    # Adafruit guarda el ultimo valor de cada feed. Pidiendolo al
    # arrancar, la placa se entera de como quedo el interruptor la
    # vez anterior en lugar de esperar a que alguien lo toque.
    cliente.subscribe(iot.feed(FEED) + "/get")
    cliente.publish(iot.feed(FEED) + "/get", "")

    print("Escuchando el feed", FEED)
    ultimo_ping = time.ticks_ms()

    while True:
        # Sin esta linea la suscripcion no sirve de nada: es aqui
        # donde el cliente mira si llego algo y llama a atender().
        cliente.check_msg()

        # Si no viaja nada durante el keepalive, el servidor da la
        # sesion por muerta y corta. El ping la mantiene viva.
        if time.ticks_diff(time.ticks_ms(), ultimo_ping) > PING_MS:
            cliente.ping()
            ultimo_ping = time.ticks_ms()

        time.sleep_ms(200)


if __name__ == "__main__":
    main()
