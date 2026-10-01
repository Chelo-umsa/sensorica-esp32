# -*- coding: utf-8 -*-
"""Revisa los diagramas de conexión antes de imprimir.

Busca una sola falla, pero es la que arruina un diagrama impreso: un
cable que pasa por encima de un rótulo y tapa el número del pin. En
pantalla se nota poco; en papel, a una tinta y reducido al ancho de la
caja de texto, el número desaparece.

Informa además cuántos saltos de cable lleva cada figura. Un salto es
correcto —es la convención del esquema eléctrico— pero muchos saltos
son señal de que el ruteo se puede simplificar.
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

import circuitos_cap2, circuitos_cap3, circuitos_cap4
import circuitos_cap5, circuitos_cap6, circuitos_cap7

MODULOS = [circuitos_cap2, circuitos_cap3, circuitos_cap4,
           circuitos_cap5, circuitos_cap6, circuitos_cap7]


def revisar():
    tapados = 0
    saltos = 0
    figuras = 0
    for modulo in MODULOS:
        for nombre in sorted(modulo.TODOS):
            salida = modulo.TODOS[nombre]()
            if isinstance(salida, tuple):
                d, alto = salida
            else:
                d, alto = salida, None
            figuras += 1
            # rotulos que se salen del lienzo: al recortar el SVG
            # quedan cortados a la mitad en la pagina
            ancho = getattr(modulo, "ANCHO_FIJO", {}).get(
                nombre, getattr(modulo, "LIENZO", None))
            if ancho:
                for (cx1, cy1, cx2, cy2) in d.protegidas:
                    if cx2 > ancho + 0.5 or cx1 < -0.5:
                        tapados += 1
                        print("        rotulo fuera del lienzo en x %.0f-%.0f "
                              "(lienzo %d)" % (cx1, cx2, ancho))
            cruces = len(d.cruces())
            saltos += cruces
            encima = d.tapados()
            sobre = d.encimados()
            for texto, caja in sobre:
                tapados += 1
                print("        rotulo %r encima del cuerpo de otra pieza"
                      % (texto or "(de la placa)"))
            estado = "ok" if not (encima or sobre) else "MAL"
            print("  %-10s  %2d salto(s)   %s" % (nombre, cruces, estado))
            for (a, b, caja) in encima:
                tapados += 1
                print("        cable %s-%s encima del rotulo en %s"
                      % (a, b, tuple(round(v) for v in caja)))
    print()
    print("  %d figuras, %d saltos, %d rotulos tapados"
          % (figuras, saltos, tapados))
    return tapados


if __name__ == "__main__":
    print("=" * 62)
    malas = revisar()
    print("=" * 62)
    sys.exit(1 if malas else 0)
