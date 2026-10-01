# -*- coding: utf-8 -*-
"""Las figuras del capítulo 1."""
import placa as P


def plano_placa():
    """El plano de pines de la placa, en vista superior.

    El lienzo va ajustado al contenido a proposito. Lo que decide el
    tamaño aparente de un rotulo no es su tamaño en pixeles sino la
    proporcion entre ese tamaño y el ancho del viewBox: con el lienzo
    de 480 que tenia antes, los rotulos salian impresos a 5,7 pt.
    Ajustandolo a 320 los mismos rotulos salen a 8,5 pt, que es el
    cuerpo del texto corriente del libro.
    """
    cuerpo, pos, alto, _cajas = P.placa(108, 26)
    leyenda, fin = P.leyenda(16, alto + 62, ancho=300, columnas=1)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 %g" '
            'width="100%%" style="display:block;margin:1mm auto 1.5mm;">'
            '%s%s</svg>' % (fin + 6, cuerpo, leyenda))
