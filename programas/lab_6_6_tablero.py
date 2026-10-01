# -*- coding: utf-8 -*-
from machine import Pin, SoftI2C, ADC
import math
import time
import dht
import ssd1306

ANCHO, ALTO, CELDA = 128, 64, 8
INTERVALO = 3
TEMPERATURA_ALTA = 30.0        # umbral del aviso en pantalla

# ----------------------------------------------------------- leer
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(ANCHO, ALTO, i2c)

sensor = dht.DHT11(Pin(14))

ntc = ADC(Pin(33))
ntc.atten(ADC.ATTN_11DB)
ntc.width(ADC.WIDTH_12BIT)

R_FIJA = 100000.0
R_NOMINAL = 100000.0
T_NOMINAL = 25.0
BETA = 3950.0
ALIMENTACION = 3.3
CERO_ABSOLUTO = 273.15


def leer_dht():
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except OSError:
        return None


def leer_ntc(muestras=16):
    suma = 0
    for _ in range(muestras):
        suma = suma + ntc.read()
        time.sleep_ms(2)
    tension = (suma / muestras) * ALIMENTACION / 4095

    if tension <= 0 or tension >= ALIMENTACION:
        return None

    resistencia = R_FIJA * tension / (ALIMENTACION - tension)
    t0 = T_NOMINAL + CERO_ABSOLUTO
    inversa = 1.0 / t0 + math.log(resistencia / R_NOMINAL) / BETA
    return 1.0 / inversa - CERO_ABSOLUTO


# -------------------------------------------------------- mostrar
def centrar(texto, fila):
    x = (ANCHO - len(texto) * CELDA) // 2
    oled.text(texto, max(0, x), fila * CELDA, 1)


def barra(valor, minimo, maximo, x, y, ancho, alto):
    oled.rect(x, y, ancho, alto, 1)
    recorrido = maximo - minimo
    if recorrido <= 0:
        return
    proporcion = (valor - minimo) / recorrido
    proporcion = max(0, min(1, proporcion))
    lleno = int((ancho - 2) * proporcion)
    if lleno > 0:
        oled.fill_rect(x + 1, y + 1, lleno, alto - 2, 1)


def dibujar(temperatura, humedad, temperatura_ntc, aviso):
    oled.fill(0)
    centrar("TABLERO", 0)
    oled.hline(0, 10, ANCHO, 1)

    if temperatura is None:
        oled.text("DHT11 sin datos", 0, 2 * CELDA, 1)
    else:
        oled.text("Amb {:4.1f}C {:3d}%".format(temperatura, humedad),
                  0, 2 * CELDA, 1)

    if temperatura_ntc is None:
        oled.text("NTC desconectado", 0, 3 * CELDA, 1)
    else:
        oled.text("NTC {:5.1f} C".format(temperatura_ntc),
                  0, 3 * CELDA, 1)
        barra(temperatura_ntc, 0, 60, 4, 4 * CELDA + 4, 120, 10)

    if aviso:
        centrar("TEMP ALTA", 7)

    oled.show()


def main():
    print("Tablero local en marcha.")

    while True:
        # leer
        lectura = leer_dht()
        temperatura, humedad = lectura if lectura else (None, None)
        temperatura_ntc = leer_ntc()

        # decidir: el umbral se evalua con el sensor que haya
        referencia = temperatura_ntc
        if referencia is None:
            referencia = temperatura
        aviso = (referencia is not None
                 and referencia >= TEMPERATURA_ALTA)

        # mostrar
        dibujar(temperatura, humedad, temperatura_ntc, aviso)

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
