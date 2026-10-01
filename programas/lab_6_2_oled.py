# -*- coding: utf-8 -*-
from machine import Pin, SoftI2C
import ssd1306
import time

ANCHO, ALTO, CELDA = 128, 64, 8

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(ANCHO, ALTO, i2c)


def centrar(texto, fila):
    """Escribe centrado en una fila, contando en celdas de 8x8."""
    x = (ANCHO - len(texto) * CELDA) // 2
    oled.text(texto, max(0, x), fila * CELDA, 1)


def barra(valor, minimo, maximo, x, y, ancho, alto):
    """Barra de progreso. Recorta el valor para no salirse."""
    oled.rect(x, y, ancho, alto, 1)
    recorrido = maximo - minimo
    if recorrido <= 0:
        return
    proporcion = (valor - minimo) / recorrido
    if proporcion < 0:
        proporcion = 0
    if proporcion > 1:
        proporcion = 1
    lleno = int((ancho - 2) * proporcion)
    if lleno > 0:
        oled.fill_rect(x + 1, y + 1, lleno, alto - 2, 1)


def main():
    # --- texto centrado
    oled.fill(0)
    centrar("SENSORICA", 2)
    centrar("ESP32", 4)
    oled.show()          # sin esta linea la pantalla queda negra
    time.sleep(2)

    # --- una barra que se llena
    for valor in range(0, 101, 5):
        oled.fill(0)
        centrar("CARGA", 0)
        oled.text("{:3d} %".format(valor), 48, 2 * CELDA, 1)
        barra(valor, 0, 100, 8, 4 * CELDA, 112, 14)
        oled.show()
        time.sleep_ms(80)

    # --- lo que no entra, se recorta solo
    oled.fill(0)
    centrar("RECORTE", 0)
    barra(150, 0, 100, 8, 3 * CELDA, 112, 14)   # 150 sobre 100
    barra(-20, 0, 100, 8, 5 * CELDA, 112, 14)   # -20 sobre 100
    oled.show()


if __name__ == "__main__":
    main()
