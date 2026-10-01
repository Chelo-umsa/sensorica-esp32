# -*- coding: utf-8 -*-
import socket
import iot
from machine import Pin

PUERTO = 80
PIN_RELE = 19
ACTIVO_EN_BAJO = True         # el puente H/L del modulo, como en el 2.5

rele = Pin(PIN_RELE, Pin.OUT)
encendido = False


def mandar(estado):
    """Traduce el estado al nivel que pide este modulo."""
    global encendido
    encendido = estado
    if ACTIVO_EN_BAJO:
        rele.value(0 if estado else 1)
    else:
        rele.value(1 if estado else 0)


def camino_pedido(peticion):
    """El camino de la PRIMERA linea: GET /algo HTTP/1.1

    Buscar "/on" en la peticion entera parece lo mismo y no lo es: el
    navegador agrega una cabecera Referer con la direccion anterior, y
    ahi aparece el "/on" de la visita previa. El boton de apagar deja
    de apagar.
    """
    try:
        return peticion.split("\r\n")[0].split(" ")[1]
    except IndexError:
        return "/"


def pagina():
    estado = "ENCENDIDO" if encendido else "APAGADO"
    color = "#1B7A3D" if encendido else "#8A8F98"
    return PLANTILLA.format(color=color, estado=estado)


PLANTILLA = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Control del rele</title>
<style>
 body {{ font-family: sans-serif; text-align: center; margin-top: 8vh }}
 .estado {{ font-size: 2em; color: {color}; margin-bottom: 0.6em; }}
 a {{ text-decoration: none; }}
 button {{ font-size: 1.8em; padding: 0.6em 1.4em; margin: 0.4em;
           border: none; border-radius: 12px; color: white; }}
 .on {{ background: #1B7A3D; }}  .off {{ background: #9B2C2C; }}
</style></head><body>
<h2>Control del rele</h2>
<p class="estado">{estado}</p>
<a href="/on"><button class="on">ENCENDER</button></a>
<a href="/off"><button class="off">APAGAR</button></a>
</body></html>
"""


def main():
    mandar(False)              # apagado antes de abrir la red a nadie
    ip = iot.conectar_wifi()

    servidor = socket.socket()
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(socket.getaddrinfo("0.0.0.0", PUERTO)[0][-1])
    servidor.listen(2)

    print("Abra http://{}/ en el telefono o el navegador.".format(ip))

    while True:
        cliente, direccion = servidor.accept()
        try:
            cliente.settimeout(3)
            peticion = cliente.recv(1024).decode()
            camino = camino_pedido(peticion)

            if camino == "/favicon.ico":
                cliente.sendall(b"HTTP/1.0 404 Not Found\r\n\r\n")
            else:
                if camino == "/on":
                    mandar(True)
                    print("orden desde", direccion[0], "-> encender")
                elif camino == "/off":
                    mandar(False)
                    print("orden desde", direccion[0], "-> apagar")

                cliente.sendall(b"HTTP/1.0 200 OK\r\n"
                                b"Content-Type: text/html\r\n\r\n")
                cliente.sendall(pagina().encode())
        except OSError as e:
            print("Visita interrumpida:", e)
        finally:
            cliente.close()


if __name__ == "__main__":
    main()
