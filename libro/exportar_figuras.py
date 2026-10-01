# -*- coding: utf-8 -*-
"""Escribe cada diagrama de conexión como archivo suelto.

El libro los lleva incrustados, pero sueltos sirven para la
diapositiva de la clase, para el pizarrón y para que un estudiante los
mire en el celular mientras arma el montaje. El SVG es el original —se
amplía cuanto se quiera— y el PNG es para pegar donde el SVG no entra.
"""
import os
import sys

# La raiz del proyecto es la carpeta que contiene programas/: asi
# estos archivos funcionan igual en la raiz o dentro de libro/.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = _AQUI if os.path.isdir(os.path.join(_AQUI, "programas")) \
    else os.path.dirname(_AQUI)
os.chdir(_RAIZ)
sys.path.insert(0, _AQUI)

import shutil

import cairosvg

import circuitos_cap2, circuitos_cap3, circuitos_cap4
import circuitos_cap5, circuitos_cap6, circuitos_cap7

MODULOS = [circuitos_cap2, circuitos_cap3, circuitos_cap4,
           circuitos_cap5, circuitos_cap6, circuitos_cap7]

DESTINO = "figuras"


def exportar():
    # La carpeta se vacía primero: si un diagrama cambia de nombre, el
    # archivo viejo queda ahí y alguien termina armando el montaje
    # equivocado.
    if os.path.isdir(DESTINO):
        shutil.rmtree(DESTINO)
    os.makedirs(DESTINO)

    escritos = 0
    for modulo in MODULOS:
        for nombre in sorted(modulo.TODOS):
            svg, _cruces = modulo.svg(nombre)
            with open(os.path.join(DESTINO, nombre + ".svg"), "w") as f:
                f.write(svg)
            cairosvg.svg2png(bytestring=svg.encode(),
                             write_to=os.path.join(DESTINO, nombre + ".png"),
                             scale=3)
            escritos += 1
    return escritos


if __name__ == "__main__":
    print("%d diagramas en %s/" % (exportar(), DESTINO))
