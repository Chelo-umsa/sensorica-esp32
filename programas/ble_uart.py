# -*- coding: utf-8 -*-
# ble_uart.py — puerto serie sobre Bluetooth LE.
# Se copia a la placa una sola vez, como ssd1306.py.
import bluetooth
from micropython import const

_CONECTADO = const(1)
_DESCONECTADO = const(2)
_ESCRITURA = const(3)

# Identificadores del Nordic UART Service. Son estos y no otros:
# es lo que la aplicacion del telefono busca.
_SERV = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
       bluetooth.FLAG_NOTIFY)
_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
       bluetooth.FLAG_WRITE)


class BLEUART:
    def __init__(self, nombre="ESP32"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._evento)
        ((self._tx, self._rx),) = self._ble.gatts_register_services(
            ((_SERV, (_TX, _RX)),))
        self._centrales = set()
        self._buzon = bytearray()
        # anuncio: banderas + nombre completo
        n = nombre.encode()
        self._anuncio = bytearray((2, 0x01, 0x06, len(n) + 1, 0x09)) + n
        self._anunciar()

    def _anunciar(self):
        self._ble.gap_advertise(100000, adv_data=self._anuncio)

    def _evento(self, evento, datos):
        if evento == _CONECTADO:
            conn, _, _ = datos
            self._centrales.add(conn)
        elif evento == _DESCONECTADO:
            conn, _, _ = datos
            self._centrales.discard(conn)
            # Hay que volver a anunciarse: si no, el telefono no
            # puede reconectarse y parece que la placa se colgo.
            self._anunciar()
        elif evento == _ESCRITURA:
            conn, atributo = datos
            if atributo == self._rx:
                self._buzon += self._ble.gatts_read(self._rx)

    def conectado(self):
        return len(self._centrales) > 0

    def write(self, texto):
        """Manda texto al telefono. Si no hay nadie, no hace nada."""
        datos = texto.encode() if isinstance(texto, str) else texto
        for conn in self._centrales:
            self._ble.gatts_notify(conn, self._tx, datos)

    def read(self):
        """Devuelve lo recibido y vacia el buzon. Puede ser vacio."""
        datos = bytes(self._buzon)
        self._buzon = bytearray()
        return datos
