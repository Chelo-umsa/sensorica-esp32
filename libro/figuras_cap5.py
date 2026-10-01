# -*- coding: utf-8 -*-
"""Las figuras del capítulo 5."""
import circuitos as C


def onda_pwm():
    """Tres ciclos de trabajo sobre la misma frecuencia, con su media."""
    W = 340
    ALTO_ONDA, SEP = 34, 52
    X0, X1 = 58, 300
    CICLOS = 4
    s = []

    for i, (duty, etiqueta) in enumerate(((25, "25 %"), (50, "50 %"),
                                          (75, "75 %"))):
        base = 48 + i * SEP
        arriba = base - ALTO_ONDA
        ancho = (X1 - X0) / CICLOS

        # eje y rotulo
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#C8CED6" '
                 'stroke-width="0.8"/>' % (X0, base, X1 + 6, base))
        s.append(C._txt(X0 - 10, base + 3, "0", 6.4, C.GRIS, "end"))
        s.append(C._txt(X0 - 10, arriba + 3, "3,3 V", 6.4, C.GRIS, "end"))
        s.append(C._txt(X1 + 12, base - ALTO_ONDA / 2 + 3, etiqueta, 8,
                        C.TEXTO, "start", "bold"))

        # la onda
        puntos = []
        for c in range(CICLOS):
            xi = X0 + c * ancho
            xm = xi + ancho * duty / 100.0
            puntos += [(xi, arriba), (xm, arriba), (xm, base),
                       (xi + ancho, base)]
        s.append('<polyline points="%s" fill="none" stroke="%s" '
                 'stroke-width="1.8" stroke-linejoin="miter"/>'
                 % (" ".join("%g,%g" % p for p in puntos), C.SENAL))

        # la media, que es lo que el LED o el motor "siente"
        ym = base - ALTO_ONDA * duty / 100.0
        s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
                 'stroke-width="1.4" stroke-dasharray="4,3"/>'
                 % (X0, ym, X1, ym, C.ROJO))

    s.append(C._txt((X0 + X1) / 2, 48 + 2 * SEP + 24,
                    "la línea de trazos es el valor medio: lo que el LED "
                    "o el motor perciben",
                    6.8, C.GRIS, "middle", inclinada=True))
    return C.envoltura("".join(s), W, 48 + 2 * SEP + 58)
