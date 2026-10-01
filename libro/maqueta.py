# -*- coding: utf-8 -*-
"""Maqueta del libro «Programación aplicada a la sensórica».

Hereda el formato del primer libro: 170x230 mm, misma tipografia y
misma familia de colores, para que los dos se vean de la misma casa.
Lo que cambia es la plantilla de cada laboratorio, que aqui es fija:

    objetivo -> materiales -> circuito -> razonamiento -> programa
    -> que debe observarse -> si algo no sale -> el mismo algoritmo
    en la otra carrera

Esa ultima seccion es la que sostiene la idea del libro: un mismo
laboratorio sirve a electricidad industrial y a automotriz, porque
lo que se ordena por capitulos es el TIPO DE SEÑAL, no la aplicacion.
"""
import html as _html

AZUL = "#1B3A6B"
ROJO = "#A81C22"
VERDE = "#3E6B1B"
GRIS = "#8c8a85"

CSS = """
@page {
  size: 170mm 230mm;
  margin: 18mm 16mm 20mm 20mm;
}
/* Los margenes se reflejan: el ancho va del lado del lomo y el angosto
   del lado del corte. Sin esto las paginas pares quedan con 16 mm
   contra el lomo, y en un libro de doscientas paginas encuadernado al
   ras el texto se mete en el pliegue. La caja no cambia de ancho
   —20 + 16 de los dos lados— asi que la paginacion es la misma. */
@page :right {            /* paginas impares: el lomo esta a la izquierda */
  margin-left: 20mm; margin-right: 16mm;
}
@page :left {             /* paginas pares: el lomo esta a la derecha */
  margin-left: 16mm; margin-right: 20mm;
  @bottom-center { content: counter(page); font-size: 8pt; color: #666; }
}
/* Sin regla para :first. El cuerpo se compone aparte de los
   preliminares, de modo que su primera pagina es la apertura del
   capitulo 1 y tiene que llevar folio como cualquier otra; la
   portadilla se queda sin folio por su propia @page portada. */
/* La hoja que queda en blanco antes de un capitulo no lleva folio. */
@page :blank { @bottom-center { content: none; } }

body { font-family:"DejaVu Serif", serif; font-size:9.7pt; line-height:1.5;
       color:#1b1b1a; hyphens:auto; }

/* ---------------------------------------------------- capitulo */
.cap { break-before: right; }
.cap .num { font-family:"DejaVu Sans", sans-serif; font-size:9pt;
            letter-spacing:.35em; color:#1B3A6B; margin:0 0 2mm; }
.cap h1 { font-family:"DejaVu Sans", sans-serif; font-size:19pt;
          line-height:1.15; margin:0 0 4mm; color:#1b1b1a; font-weight:600; }
.cap .linea { border:0; border-top:0.6mm solid #1B3A6B; width:28mm;
              margin:0 0 5mm 0; }
.entrada { font-size:10.2pt; color:#3a3a38; margin-bottom:7mm; }
.entrada p { text-align:justify; }

/* ------------------------------------------------ laboratorio */
h2 { font-family:"DejaVu Sans", sans-serif; font-size:12.5pt; color:#1B3A6B;
     margin:9mm 0 1mm; break-after:avoid; font-weight:600; }
h2 .id { color:#8c8a85; font-weight:400; }
h3 { font-family:"DejaVu Sans", sans-serif; font-size:9.6pt; color:#1B3A6B;
     margin:5.5mm 0 1.5mm; break-after:avoid; font-weight:600;
     text-transform:uppercase; letter-spacing:.06em; }
h4 { font-family:"DejaVu Sans", sans-serif; font-size:9.4pt;
     margin:4mm 0 1mm; break-after:avoid; }
p { margin:0 0 2.6mm; text-align:justify; }
ul, ol { margin:0 0 2.6mm; padding-left:6mm; }
li { margin-bottom:1.2mm; text-align:justify; }
b, strong { font-weight:600; }

/* ------------------------------------------------------ tablas */
table { width:100%; border-collapse:collapse; margin:2mm 0 3.5mm;
        font-size:8.9pt; break-inside:avoid; }
th { background:#1B3A6B; color:#fff; text-align:left; padding:1.5mm 2mm;
     font-family:"DejaVu Sans", sans-serif; font-weight:600; font-size:8.5pt; }
td { border-bottom:0.2mm solid #cfd4da; padding:1.5mm 2mm; vertical-align:top; }
tr:last-child td { border-bottom:none; }
td.c { text-align:center; white-space:nowrap; }

/* ------------------------------------------------ codigo y consola */
code { font-family:"DejaVu Sans Mono", monospace; font-size:8.5pt;
       background:#eef1f5; padding:0.2mm 0.8mm; border-radius:0.6mm; }
pre { font-family:"DejaVu Sans Mono", monospace; font-size:8.1pt;
      white-space:pre; background:#f4f6f9; border-left:1mm solid #1B3A6B;
      padding:2.8mm 3mm; margin:2mm 0 3.5mm; line-height:1.38;
      overflow-wrap:normal; }
pre.con { border-left-color:#8c8a85; background:#f5f5f4; }
pre.cir { border-left-color:#3E6B1B; background:#f5f7f3; font-size:8.3pt; }
pre b { font-weight:700; }

/* -------------------------------------------------------- cajas */
.caja { padding:2.8mm 3.2mm; margin:3mm 0; break-inside:avoid; font-size:9.2pt; }
.caja p:last-child { margin-bottom:0; }
.caja h4 { margin:0 0 1.2mm; font-size:9pt; }
.aviso { background:#fdf3f3; border-left:1mm solid #A81C22; }
.aviso h4 { color:#A81C22; }
.nota  { background:#f2f4f7; border-left:1mm solid #8c8a85; }
.otra  { background:#f4f7f2; border-left:1mm solid #3E6B1B; }
.otra h4 { color:#3E6B1B; }

/* -------------------------------------------------------- figuras */
.fig { break-inside:avoid; margin:3mm 0 4mm; text-align:center; }
/* Una figura no se separa de su titulo: si no entran juntas en lo que
   queda de pagina, pasan las dos a la siguiente y el texto anterior
   sigue llenando esta. Sin esto quedaba una pagina con el titulo solo. */
h3 + .fig, h4 + .fig, p + .fig { break-before:avoid; }
.fig svg { max-width:134mm; max-height:158mm; }
.fig.ancha svg { max-width:134mm; max-height:158mm; }
.fig.ancha { break-before:auto; }
p.epi { font-size:8.2pt; color:#4a4a48; text-align:center; margin:0.5mm 0 0;
        font-family:"DejaVu Sans", sans-serif; }
p.epi b { color:#1B3A6B; }

/* ---------------------------------------------------- ejercicios */
.ejerc { break-inside:avoid-page; }
.ejerc ol { padding-left:7mm; }
.ejerc li { margin-bottom:2mm; }
"""


def esc(t):
    return _html.escape(t, quote=False)


# ------------------------------------------------------- piezas
def capitulo(numero, titulo, entrada):
    return ('<div class="cap">\n<p class="num">CAPÍTULO {}</p>\n'
            '<h1>{}</h1>\n<hr class="linea">\n'
            '<div class="entrada">{}</div>\n').format(
        numero, esc(titulo), entrada)


def lab(id_, titulo):
    return '<h2><span class="id">{}</span>  {}</h2>\n'.format(esc(id_), esc(titulo))


def sec(t):
    return "<h3>{}</h3>\n".format(esc(t))


def codigo(texto, clase="", archivo=None):
    cab = ''
    if archivo:
        cab = '<p style="margin-bottom:1mm;font-size:8.6pt;color:#666;">' \
              'Archivo <code>{}</code></p>'.format(esc(archivo))
    c = ' class="%s"' % clase if clase else ''
    return cab + "<pre{}>{}</pre>\n".format(c, esc(texto.rstrip("\n")))


def circuito(texto):
    return codigo(texto, "cir")


_figuras = [0]
_capitulo_actual = [None]


def figura(svg, epigrafe, capitulo=None, ancha=False):
    """Inserta un diagrama vectorial con su numero y su epigrafe.

    El SVG va en linea dentro del PDF: no es una imagen pegada sino
    trazos, de modo que la imprenta puede ampliarlo cuanto quiera y
    el texto de los rotulos sigue siendo texto.
    """
    # La cuenta se reinicia en cada capitulo: la figura 5.1 es la
    # primera del capitulo 5, no la sexta del libro.
    if capitulo != _capitulo_actual[0]:
        _capitulo_actual[0] = capitulo
        _figuras[0] = 0
    _figuras[0] += 1
    n = "%s.%d" % (capitulo, _figuras[0]) if capitulo else str(_figuras[0])
    clase = "fig ancha" if ancha else "fig"
    return ('<div class="{}">{}<p class="epi"><b>Figura {}</b> — {}</p></div>\n'
            .format(clase, svg, n, esc(epigrafe)))


def reiniciar_figuras():
    _figuras[0] = 0


def consola(texto):
    return codigo(texto, "con")


def tabla(encabezados, filas, centradas=()):
    h = "".join("<th>%s</th>" % esc(x) for x in encabezados)
    cuerpo = ""
    for f in filas:
        celdas = ""
        for i, c in enumerate(f):
            cl = ' class="c"' if i in centradas else ''
            celdas += "<td%s>%s</td>" % (cl, c)
        cuerpo += "<tr>%s</tr>" % celdas
    return "<table><tr>%s</tr>%s</table>\n" % (h, cuerpo)


def caja(clase, titulo, cuerpo):
    t = "<h4>%s</h4>" % esc(titulo) if titulo else ""
    return '<div class="caja {}">{}{}</div>\n'.format(clase, t, cuerpo)


def aviso(titulo, cuerpo):
    return caja("aviso", titulo, cuerpo)


def nota(titulo, cuerpo):
    return caja("nota", titulo, cuerpo)


def otra_carrera(cuerpo):
    return caja("otra", "El mismo algoritmo en…", cuerpo)


def ejercicios(items):
    lis = "".join("<li>%s</li>" % x for x in items)
    return ('<div class="ejerc"><h3>Ejercicios propuestos</h3>'
            '<ol>%s</ol></div>\n' % lis)


def p(*textos):
    return "".join("<p>%s</p>\n" % t for t in textos)


def construir(partes, salida, css_extra=""):
    from weasyprint import HTML, CSS as WCSS
    doc = ("<html><head><meta charset='utf-8'></head><body>"
           + "".join(partes) + "</body></html>")
    HTML(string=doc).write_pdf(salida, stylesheets=[WCSS(string=CSS + css_extra)])
    return salida


# --------------------------------------------------- control de ancho
ANCHO_MAXIMO = 72   # caracteres que entran en una linea impresa de codigo


def revisar_ancho(partes):
    """Avisa de toda linea de codigo que se saldria de la caja impresa.

    A 8,1 pt en DejaVu Sans Mono, dentro de una caja de 127 mm, entran
    72 caracteres. Una linea mas larga se sale del margen y la imprenta
    la corta. Conviene comprobarlo antes de maquetar, no despues.
    """
    import re
    largas = []
    for bloque in partes:
        for pre in re.findall(r"<pre[^>]*>(.*?)</pre>", bloque, re.S):
            for linea in _html.unescape(pre).split("\n"):
                if len(linea) > ANCHO_MAXIMO:
                    largas.append((len(linea), linea.strip()))
    return largas


def exportar_programas(partes, destino="programas"):
    """Escribe en disco cada programa rotulado con un nombre de archivo.

    Asi el texto que sale impreso y el archivo que el lector descarga
    del repositorio son el mismo, y no dos copias que se separan en
    cuanto alguien corrige una y se olvida de la otra.
    """
    import re, os
    # Se vacia la carpeta primero: si un programa cambia de nombre, la
    # version vieja se quedaria ahi y acabaria publicada en el
    # repositorio junto a la buena.
    os.makedirs(destino, exist_ok=True)
    for viejo in os.listdir(destino):
        if viejo.endswith(".py"):
            os.remove(os.path.join(destino, viejo))
    escritos = []
    for bloque in partes:
        for nombre, cuerpo in re.findall(
                r"Archivo <code>([^<]+)</code></p><pre[^>]*>(.*?)</pre>", bloque, re.S):
            # config.py es el unico archivo del libro que NO se publica:
            # lleva las claves de cada uno. El repositorio reparte
            # config_ejemplo.py y cada lector hace el suyo.
            if nombre == "config.py":
                continue
            ruta = os.path.join(destino, nombre)
            with open(ruta, "w") as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write(_html.unescape(cuerpo).strip() + "\n")
            escritos.append(ruta)
    return escritos


def revisar_nombres(partes):
    """Programas cuyo archivo no coincide con su laboratorio.

    Al insertar un laboratorio en medio de un capitulo, los que vienen
    despues cambian de numero; los nombres de archivo, que estan
    escritos a mano, no se mueven solos. El lector busca el programa
    del 7.6 y encuentra uno que se llama lab_7_5. Que lo compruebe la
    maquina.
    """
    import re
    malos, actual = [], None
    for bloque in partes:
        m = re.search(r'<span class="id">([\d]+\.[\d]+)</span>', bloque)
        if m:
            actual = m.group(1)
        for nombre in re.findall(r"Archivo <code>(lab_[^<]+)</code>", bloque):
            if actual is None:
                continue
            esperado = "lab_%s_" % actual.replace(".", "_")
            if not nombre.startswith(esperado):
                malos.append((actual, nombre, esperado + "..."))
    return malos


# ------------------------------------- control de altura de figuras
# La caja de texto mide 192 mm. Una figura mas alta que eso, con su
# epigrafe, no entra en ninguna pagina: el maquetador la manda entera
# a la siguiente y deja la anterior casi vacia. Conviene saberlo antes
# de imprimir y no despues.
ALTO_CAJA_MM = 192
MARGEN_EPIGRAFE_MM = 16


def revisar_alto_figuras(partes, ancho_mm=134):
    """Figuras que no entrarian en una pagina junto a su epigrafe."""
    import re
    altas = []
    for bloque in partes:
        for vb, ancho_svg in re.findall(
                r'viewBox="0 0 ([\d.]+) ([\d.]+)"', bloque):
            pass
        for m in re.finditer(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', bloque):
            w, h = float(m.group(1)), float(m.group(2))
            alto_mm = h * ancho_mm / w
            if alto_mm + MARGEN_EPIGRAFE_MM > ALTO_CAJA_MM:
                altas.append((alto_mm, w, h))
    return altas
