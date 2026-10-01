# -*- coding: utf-8 -*-
"""Arma el libro completo, con preliminares, índice y anexos.

Se compila en dos piezas y se unen al final. El cuerpo va por su lado
—así su primera página es la 1 y no la 7—, y los preliminares por el
suyo, con numeración romana. Unirlos al final no es un rodeo: el motor
de composición no reinicia el contador de página a mitad de un
documento, de modo que la única manera de tener las dos numeraciones
que lleva un libro es componer cada una por separado.

De paso, la primera compilación del cuerpo sirve para averiguar en qué
página cae cada laboratorio, que es lo que necesita el índice.
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

import re
import pdfplumber
from pypdf import PdfReader, PdfWriter
from weasyprint import HTML, CSS as WCSS

import maqueta
import preliminares as PRE
import cap1, cap2, cap3, cap4, cap5, cap6, cap7
import anexos

CAPITULOS = [
    (1, "El ESP32 y MicroPython", cap1),
    (2, "Entradas y salidas digitales", cap2),
    (3, "Señales analógicas", cap3),
    (4, "Señales de pulso", cap4),
    (5, "Salidas moduladas", cap5),
    (6, "Sensores con bus y protocolo", cap6),
    (7, "Monitoreo remoto", cap7),
]

CUERPO = []
for _n, _t, _m in CAPITULOS:
    CUERPO += _m.PARTES
CUERPO += anexos.PARTES

CSS_TOTAL = maqueta.CSS + PRE.CSS


def titulos():
    """Capítulos y laboratorios, en orden, leídos del código fuente."""
    salida = []
    for n, titulo, modulo in CAPITULOS:
        salida.append((0, "%d. %s" % (n, titulo), None))
        fuente = open(modulo.__file__).read()
        for ident, nombre in re.findall(r'A\(lab\("([\d.A-Z]+)",\s*"([^"]+)"',
                                        fuente):
            salida.append((1, "%s  %s" % (ident, nombre), ident))
    fuente = open(anexos.__file__).read()
    for letra, titulo in re.findall(r'A\(anexo\("([A-Z])",\s*"([^"]+)"',
                                    fuente):
        salida.append((0, "Anexo %s. %s" % (letra, titulo), None))
        for ident, nombre in re.findall(
                r'A\(lab\("(%s\.\d+)",\s*"([^"]+)"' % letra, fuente):
            salida.append((1, "%s  %s" % (ident, nombre), ident))
    return salida


def paginas_del_cuerpo(ruta):
    """Página de cada laboratorio y de cada capítulo, del PDF del cuerpo."""
    paginas = {}
    with pdfplumber.open(ruta) as pdf:
        for pg in pdf.pages:
            texto = pg.extract_text() or ""
            for linea in texto.split("\n"):
                linea = linea.strip()
                m = re.match(r"^([\d.]+|[A-Z]\.\d+)\s+\S", linea)
                if m and m.group(1) not in paginas:
                    paginas[m.group(1)] = pg.page_number
            # la apertura de capitulo: "CAPÍTULO n" con espaciado
            m = re.search(r"C\s*A\s*P\s*Í\s*T\s*U\s*L\s*O\s*(\d)", texto)
            if m:
                paginas.setdefault("cap%s" % m.group(1), pg.page_number)
            m = re.search(r"A\s*N\s*E\s*X\s*O\s*([A-Z])", texto)
            if m:
                paginas.setdefault("anexo%s" % m.group(1), pg.page_number)
    return paginas


def _componer(partes, destino):
    HTML(string="<html><head><meta charset='utf-8'></head><body>"
         + "".join(partes) + "</body></html>").write_pdf(
        destino, stylesheets=[WCSS(string=CSS_TOTAL)])


def _unir(preliminares, cuerpo, destino):
    """Pega los preliminares delante del cuerpo.

    Si los preliminares ocupan un número impar de páginas se agrega una
    en blanco, para que la página 1 del cuerpo caiga en página derecha:
    todo capítulo abre a la derecha, y si los preliminares corren la
    paginación en uno, abren todos a la izquierda.
    """
    salida = PdfWriter()
    pre = PdfReader(preliminares)
    for pagina in pre.pages:
        salida.add_page(pagina)
    if len(pre.pages) % 2:
        salida.add_blank_page()
    for pagina in PdfReader(cuerpo).pages:
        salida.add_page(pagina)
    with open(destino, "wb") as f:
        salida.write(f)
    return len(salida.pages), len(pre.pages) + len(pre.pages) % 2


def construir():
    # --- primera pasada: solo el cuerpo, para saber las paginas
    maqueta.reiniciar_figuras()
    _componer(CUERPO, "_cuerpo.pdf")
    paginas = paginas_del_cuerpo("_cuerpo.pdf")

    # --- el indice
    entradas = []
    n_cap = 0
    for nivel, texto, ident in titulos():
        if nivel == 0:
            if texto.startswith("Anexo"):
                clave = "anexo%s" % texto.split()[1].rstrip(".")
            else:
                n_cap += 1
                clave = "cap%d" % n_cap
            entradas.append((0, texto, paginas.get(clave, "")))
        else:
            entradas.append((1, texto, paginas.get(ident, "")))

    sin_pagina = [t for _n, t, pg in entradas if pg == ""]
    if sin_pagina:
        print("ATENCION: %d entradas del indice sin pagina" % len(sin_pagina))
        for t in sin_pagina[:6]:
            print("   ", t)

    # --- segunda pasada: el cuerpo definitivo y los preliminares
    maqueta.reiniciar_figuras()
    partes = [PRE.portadilla(), PRE.creditos(), PRE.indice(entradas),
              PRE.prefacio()] + list(CUERPO)

    largas = maqueta.revisar_ancho(partes)
    if largas:
        print("ATENCION: %d lineas de codigo no entran en la caja" % len(largas))
        for n, l in largas:
            print("   %3d car  %s" % (n, l[:72]))

    altas = maqueta.revisar_alto_figuras(partes)
    if altas:
        print("ATENCION: %d figura(s) no entran en una pagina" % len(altas))
        for alto_mm, w, h in altas:
            print("   %.0f mm de alto (viewBox %.0fx%.0f)" % (alto_mm, w, h))

    mal_llamados = maqueta.revisar_nombres(partes)
    if mal_llamados:
        print("ATENCION: %d programa(s) con el numero de laboratorio "
              "equivocado" % len(mal_llamados))
        for lab, nombre, esperado in mal_llamados:
            print("   %s -> %s  (deberia empezar con %s)"
                  % (lab, nombre, esperado))

    programas = maqueta.exportar_programas(partes)

    maqueta.reiniciar_figuras()
    _componer(CUERPO, "_cuerpo.pdf")
    _componer([PRE.portadilla(), PRE.creditos(), PRE.indice(entradas),
               PRE.prefacio()], "_pre.pdf")
    total, romanas = _unir("_pre.pdf", "_cuerpo.pdf", "libro.pdf")

    import os
    os.remove("_cuerpo.pdf")
    os.remove("_pre.pdf")
    print("listo: %d programas, %d entradas de indice" %
          (len(programas), len(entradas)))
    print("       %d paginas: %d de preliminares y %d de cuerpo"
          % (total, romanas, total - romanas))


if __name__ == "__main__":
    construir()
