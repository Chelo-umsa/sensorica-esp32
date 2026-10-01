# -*- coding: utf-8 -*-
from machine import Pin, PWM
import machine
import time

PIN_GENERADOR = 25
PIN_CONTADOR = 26

FRECUENCIA = 200          # pulsos por segundo que se generan
DURACION = 3              # segundos que dura cada medicion
TRABAJO_MS = 5            # lo que el programa tarda en cada vuelta

generador = PWM(Pin(PIN_GENERADOR), freq=FRECUENCIA)
generador.duty(512)       # 50 %: mitad alto, mitad bajo

entrada = Pin(PIN_CONTADOR, Pin.IN)

pulsos = 0


def al_llegar_un_pulso(pin):
    """Se ejecuta sola, apenas baja la senal. Solo suma uno."""
    global pulsos
    pulsos = pulsos + 1


def tomar_pulsos():
    global pulsos
    estado = machine.disable_irq()
    cuenta = pulsos
    pulsos = 0
    machine.enable_irq(estado)
    return cuenta


def contar_por_consulta(segundos):
    """Revisa el pin una y otra vez, haciendo otra cosa entre medio.

    Ese "otra cosa" es lo que ocurre en cualquier programa real. Si
    en ese rato la senal sube y vuelve a bajar, ese pulso no lo
    cuenta nadie.
    """
    cuenta = 0
    anterior = entrada.value()
    limite = time.ticks_add(time.ticks_ms(), segundos * 1000)

    while time.ticks_diff(limite, time.ticks_ms()) > 0:
        actual = entrada.value()
        if anterior == 1 and actual == 0:
            cuenta = cuenta + 1
        anterior = actual
        time.sleep_ms(TRABAJO_MS)      # el programa hace otra cosa

    return cuenta


def contar_por_interrupcion(segundos):
    """Deja que el pin avise, perdiendo el mismo tiempo que antes."""
    entrada.irq(trigger=Pin.IRQ_FALLING, handler=al_llegar_un_pulso)
    tomar_pulsos()                      # descarta lo acumulado

    limite = time.ticks_add(time.ticks_ms(), segundos * 1000)
    while time.ticks_diff(limite, time.ticks_ms()) > 0:
        time.sleep_ms(TRABAJO_MS)      # exactamente el mismo trabajo

    entrada.irq(handler=None)
    return tomar_pulsos()


def main():
    esperados = FRECUENCIA * DURACION
    print("Se generan {} pulsos por segundo durante {} s.".format(
        FRECUENCIA, DURACION))
    print("Deberian contarse {} pulsos.".format(esperados))
    print("")

    por_consulta = contar_por_consulta(DURACION)
    por_interrupcion = contar_por_interrupcion(DURACION)

    print("  metodo          contados   perdidos")
    for nombre, cuenta in (("consulta", por_consulta),
                           ("interrupcion", por_interrupcion)):
        perdidos = esperados - cuenta
        print("  {:<14}  {:6d}   {:5d}  ({:4.1f} %)".format(
            nombre, cuenta, perdidos, perdidos * 100.0 / esperados))


if __name__ == "__main__":
    main()
