# -*- coding: utf-8 -*-
import socket
import time
import network
from machine import Pin
import dht
import config

PIN_DATOS = 14
PUERTO = 80
INTERVALO_MS = 3000       # cada cuanto se toma una medicion nueva

sensor = dht.DHT11(Pin(PIN_DATOS))

# Ultima medicion valida. El servidor entrega esto, no una lectura
# hecha en el momento: medir dentro de la atencion de la peticion
# haria esperar al visitante y bloquearia a los demas.
temperatura = None
humedad = None
medido_en = 0
fallas = 0


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a la red", config.WIFI_SSID, "...")
        wlan.connect(config.WIFI_SSID, config.WIFI_CLAVE)
        for _ in range(40):
            if wlan.isconnected():
                break
            time.sleep(0.5)
    if not wlan.isconnected():
        raise OSError("No se pudo conectar. Revise config.py")
    return wlan.ifconfig()[0]


def medir_si_toca():
    """Toma una medicion nueva si paso el intervalo.

    Si el sensor falla se conserva el ultimo valor bueno en lugar
    de detener el servidor.
    """
    global temperatura, humedad, medido_en, fallas
    if temperatura is not None and \
            time.ticks_diff(time.ticks_ms(), medido_en) < INTERVALO_MS:
        return
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        fallas = 0
    except OSError:
        fallas = fallas + 1
    medido_en = time.ticks_ms()


def pagina():
    if temperatura is None:
        valores = "<p>Esperando la primera medicion...</p>"
    else:
        valores = ("<p>Temperatura: {} C</p>\n"
                   "<p>Humedad: {} %</p>").format(temperatura, humedad)
        if fallas > 0:
            valores += ("\n<p class='aviso'>{} lecturas "
                        "fallidas</p>").format(fallas)

    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="4">
<title>Monitoreo DHT11</title>
<style>
body {{ text-align:center; font-family:Arial, sans-serif; }}
h1 {{ color:navy; }}
p {{ font-size:30px; }}
p.aviso {{ font-size:16px; color:#A81C22; }}
</style>
</head>
<body>
<h1>MONITOREO SENSOR DHT11</h1>
{}
</body>
</html>
""".format(valores)


def camino_pedido(peticion):
    """Extrae el camino de la primera linea: GET /algo HTTP/1.1"""
    try:
        return peticion.split(" ")[1]
    except IndexError:
        return "/"


def main():
    ip = conectar_wifi()

    servidor = socket.socket()
    # Sin esto, al reiniciar el programa el puerto queda ocupado un
    # rato y la placa responde "address in use".
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(socket.getaddrinfo("0.0.0.0", PUERTO)[0][-1])
    servidor.listen(2)
    servidor.settimeout(1)      # para poder medir entre visita y visita

    print("Servidor listo. Abra http://{}/ en el navegador.".format(ip))

    while True:
        medir_si_toca()

        try:
            cliente, direccion = servidor.accept()
        except OSError:
            continue            # no vino nadie: se vuelve a medir

        try:
            cliente.settimeout(3)
            peticion = cliente.recv(1024).decode()

            if camino_pedido(peticion) == "/favicon.ico":
                # El navegador pide siempre el icono. Se le contesta
                # que no existe en vez de mandarle la pagina entera.
                cliente.sendall(b"HTTP/1.0 404 Not Found\r\n\r\n")
            else:
                cliente.sendall(b"HTTP/1.0 200 OK\r\n"
                                b"Content-Type: text/html\r\n\r\n")
                cliente.sendall(pagina().encode())
        except OSError as e:
            print("Visita interrumpida:", e)
        finally:
            cliente.close()


if __name__ == "__main__":
    main()
