# -*- coding: utf-8 -*-
TEMPERATURA_MIN, TEMPERATURA_MAX = 0, 50
HUMEDAD_MIN, HUMEDAD_MAX = 20, 90


def porcentaje(valor, minimo, maximo):
    """Posicion de valor dentro de la escala, de 0 a 100.

    Recorta solo el LARGO DE LA BARRA. El numero que se escribe al
    lado sigue siendo el que entrego el sensor.
    """
    recorrido = maximo - minimo
    if recorrido <= 0:
        return 0.0
    proporcion = (valor - minimo) * 100.0 / recorrido
    if proporcion < 0:
        return 0.0
    if proporcion > 100:
        return 100.0
    return proporcion


def barra(etiqueta, valor, unidad, minimo, maximo, color):
    fuera = "" if minimo <= valor <= maximo else " (fuera de escala)"
    return """<div class="marco">
  <div class="relleno"
       style="width:{:.1f}%; background-color:{};"></div>
  <div class="cifra">{} {}</div>
</div>
<div class="rotulo">{} ({} a {} {}){}</div>""".format(
        porcentaje(valor, minimo, maximo), color, valor, unidad,
        etiqueta, minimo, maximo, unidad, fuera)
