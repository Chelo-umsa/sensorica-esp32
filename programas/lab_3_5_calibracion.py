# -*- coding: utf-8 -*-
from machine import Pin, ADC
import time

PIN_ENTRADA = 34

entrada = ADC(Pin(PIN_ENTRADA))
entrada.atten(ADC.ATTN_11DB)
entrada.width(ADC.WIDTH_12BIT)


# ------------------------------------------------------- filtrado
def leer_promedio(muestras=32, espera_ms=2):
    """Promedia varias lecturas. Atenua el ruido de fondo."""
    suma = 0
    for _ in range(muestras):
        suma = suma + entrada.read()
        time.sleep_ms(espera_ms)
    return suma / muestras


def leer_mediana(muestras=15, espera_ms=2):
    """Valor central de varias lecturas ordenadas.

    A diferencia del promedio, no se deja arrastrar por una lectura
    disparatada. Conviene cuando hay motores o contactores cerca.
    """
    valores = []
    for _ in range(muestras):
        valores.append(entrada.read())
        time.sleep_ms(espera_ms)
    valores.sort()
    return valores[len(valores) // 2]


# ---------------------------------------------------- calibracion
def recta_de_calibracion(crudo1, real1, crudo2, real2):
    """Pendiente y ordenada de la recta que une los dos puntos."""
    if crudo2 == crudo1:
        raise ValueError("los dos puntos dan la misma lectura")
    pendiente = (real2 - real1) / (crudo2 - crudo1)
    ordenada = real1 - pendiente * crudo1
    return pendiente, ordenada


def aplicar(crudo, pendiente, ordenada):
    return pendiente * crudo + ordenada


def calibrar(unidad="C"):
    """Guia la toma de los dos puntos y devuelve la recta."""
    print("Punto 1: lleve el sensor a la primera condicion conocida.")
    input("   Pulse Enter cuando este estable... ")
    crudo1 = leer_promedio()
    real1 = float(input("   Valor real, en {}: ".format(unidad)))

    print("Punto 2: lleve el sensor a la segunda condicion.")
    input("   Pulse Enter cuando este estable... ")
    crudo2 = leer_promedio()
    real2 = float(input("   Valor real, en {}: ".format(unidad)))

    pendiente, ordenada = recta_de_calibracion(
        crudo1, real1, crudo2, real2)
    print("")
    print("   pendiente = {:.6f}".format(pendiente))
    print("   ordenada  = {:.4f}".format(ordenada))
    print("   Copie estas dos cifras al programa definitivo.")
    return pendiente, ordenada


def main():
    pendiente, ordenada = calibrar()
    print("")
    print("  crudo    calibrado")

    while True:
        crudo = leer_promedio()
        print("   {:6.0f}    {:7.2f}".format(
            crudo, aplicar(crudo, pendiente, ordenada)))
        time.sleep(1)


if __name__ == "__main__":
    main()
