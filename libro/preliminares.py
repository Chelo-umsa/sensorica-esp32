# -*- coding: utf-8 -*-
"""Preliminares del libro: portadilla, créditos, índice y prefacio."""
from maqueta import esc, p

# Las barras marcan dónde se parte el título en la portadilla. En
# cualquier otro lado el título va seguido: LLANO lo devuelve así.
TITULO = "Programación aplicada | a la sensórica | industrial y automotriz"
SUBTITULO = "ESP32, MicroPython y monitoreo IoT"


def llano(texto):
    return " ".join(t.strip() for t in texto.split("|"))
AUTOR = "Javier Marcelo Flores Monrroy"
REPOSITORIO = "github.com/Chelo-umsa/sensorica-esp32"
DEPOSITO_LEGAL = "4-4-115-2026"

CSS = """
/* ------------------------------------------------ preliminares */
@page portada { margin: 30mm 20mm; @bottom-center { content: none; } }
@page romana { @bottom-center { content: counter(page, lower-roman);
                                font-size:8pt; color:#666; } }

.portadilla { page: portada; break-after: page; text-align: center; }
/* Centrado y SIN justificar: la regla general de parrafo justifica, y
   un titulo de tres lineas justificado abre huecos enormes entre
   palabra y palabra. El salto de linea va escrito a mano, que es la
   unica manera de que "industrial y automotriz" no se parta. */
.portadilla .t { font-family:"DejaVu Sans", sans-serif; font-size:24pt;
                 font-weight:600; line-height:1.2; color:#1b1b1a;
                 margin:50mm 0 0; text-align:center; text-wrap:balance; }
.portadilla .st { font-family:"DejaVu Sans", sans-serif; font-size:12.5pt;
                  color:#1B3A6B; margin:7mm 0 0; font-weight:400;
                  text-align:center; line-height:1.35; }
.portadilla .raya { border:0; border-top:0.6mm solid #1B3A6B; width:36mm;
                    margin:12mm auto; }
.portadilla .a { font-family:"DejaVu Sans", sans-serif; font-size:12pt;
                 color:#3a3a38; margin:0; text-align:center; }

.creditos { page: romana; break-after: page; font-size:9pt; }
.creditos p { text-align:left; margin:0 0 3mm; }
/* La separacion es la que deja el bloque legal al pie sin empujarlo
   a una segunda pagina: la de creditos es siempre una sola. */
.creditos .pie { margin-top:46mm; color:#4a4a48; font-size:8.4pt; }

/* salto simple y no "a pagina derecha": con break-after:right
   cada fragmento del indice arrastraba una pagina en blanco. */
.indice { page: romana; break-after: page; }
.indice h2 { margin-top:0; }
/* El indice SI puede partirse entre paginas: la regla general de
   tablas lo impide, y sin esto salta entero a una pagina nueva
   dejando el titulo solo en la anterior. */
.indice table { font-size:9.2pt; break-inside: auto; }
.indice tr { break-inside: avoid; }
.indice td { border-bottom:none; padding:0.8mm 2mm; }
.indice td.n { text-align:right; color:#4a4a48; white-space:nowrap; }
/* La clase se llama ix-cap y no cap: "cap" es la apertura de
   capitulo, que lleva break-before:right, y cada fila de capitulo del
   indice arrastraba un salto de pagina. */
.indice tr.ix-cap td { font-family:"DejaVu Sans", sans-serif; font-weight:600;
                       color:#1B3A6B; padding-top:4mm; font-size:9.6pt; }
.indice tr.ix-lab td:first-child { padding-left:7mm; }

.prefacio { page: romana; }
.prefacio h2 { margin-top:0; }

/* El cuerpo no reinicia aqui su numeracion: se compone como
   documento aparte y se pega detras de estas paginas. El motor no
   reinicia el contador de pagina a mitad de documento —counter-reset
   sobre un elemento no lo toca— y ese es el motivo de que el libro se
   arme en dos piezas. */
"""


def portadilla():
    # El titulo se parte donde diga TITULO, con "|" como marca: a
    # merced del motor, "industrial y automotriz" queda cortado en dos
    # lineas y las dos carreras dejan de leerse como una sola idea.
    titulo = "<br>".join(esc(t.strip()) for t in TITULO.split("|"))
    return ('<div class="portadilla">'
            '<p class="t">{}</p>'
            '<p class="st">{}</p>'
            '<hr class="raya">'
            '<p class="a">{}</p>'
            '</div>\n').format(titulo, esc(SUBTITULO), esc(AUTOR))


def creditos(anio=2026):
    return ('<div class="creditos">'
            + p("<b>{}</b><br>{}".format(esc(llano(TITULO)), esc(SUBTITULO)),
                "© {} {}".format(anio, esc(AUTOR)),
                "Primera edición.",
                "Depósito legal: {}".format(esc(DEPOSITO_LEGAL)))
            + p("Los programas de este libro se publican bajo licencia MIT. "
                "Pueden copiarse, modificarse y usarse en clase o en trabajo "
                "profesional, con la sola condición de conservar el aviso de "
                "licencia.",
                "El texto, las figuras y los diagramas de conexión se "
                "publican bajo Creative Commons BY-NC-SA 4.0: pueden "
                "reproducirse citando la fuente, sin uso comercial y "
                "compartiendo igual.")
            + p("Todos los programas, los módulos que se copian a la placa y "
                "los archivos de las figuras están en:<br>"
                "<code>{}</code>".format(esc(REPOSITORIO)))
            + '<div class="pie">'
            + p("Los nombres de marcas y productos mencionados —ESP32, "
                "Adafruit IO, Grafana, InfluxDB, Thonny, Wokwi— pertenecen a "
                "sus respectivos titulares y se citan con fines didácticos.",
                "Cada programa de este libro se comprobó contra un simulador "
                "de MicroPython escrito para ese fin, que verifica la "
                "aritmética, los rangos y el comportamiento ante fallas de "
                "cableado. Las constantes de calibración corresponden a los "
                "sensores con los que se escribió el libro y deben ajustarse "
                "a los de cada laboratorio, con el procedimiento del "
                "apartado 3.5.")
            + '</div></div>\n')


def prefacio():
    return ('<div class="prefacio"><h2>Prefacio</h2>'
            + p("Este libro nació de un problema de aula. Dicto "
                "<b>Programación</b> en mecánica automotriz e "
                "<b>Informática Industrial</b> en electricidad: dos materias "
                "que enseñan lo mismo con nombres distintos. En una se llama "
                "monitoreo de procesos y en la otra, sensores del vehículo. "
                "Los estudiantes de cada carrera creen que lo suyo no le "
                "sirve a la otra, y no es así: un termistor que mide el "
                "bobinado de un motor y uno que mide el refrigerante de un "
                "vehículo se leen con el mismo programa.",

                "De ahí sale la única decisión de fondo del libro: los "
                "capítulos están ordenados por <b>tipo de señal</b> y no por "
                "aplicación. Un capítulo para las señales digitales, otro "
                "para las analógicas, otro para los pulsos, otro para los "
                "sensores que hablan por bus. Así el mismo laboratorio sirve "
                "a las dos áreas, y cada uno cierra con un recuadro que "
                "muestra el otro uso del mismo algoritmo.",

                "Por eso el libro no está escrito para una carrera sino para "
                "dos familias de carreras. En el <b>área eléctrica y "
                "electrónica</b> —electricidad, electromecánica, electrónica "
                "y telecomunicaciones— porque un sensor es, antes que nada, "
                "una señal que hay que acondicionar, medir y transmitir. Y en "
                "el <b>área mecánica</b> —mecánica automotriz, mecánica "
                "industrial, mantenimiento— porque el motor, la caja y el "
                "sistema hidráulico de hoy se diagnostican leyendo esos "
                "mismos sensores. Quien dicte una materia de sensores, de "
                "instrumentación, de automatización o de diagnóstico "
                "electrónico va a encontrar aquí sus contenidos, con el "
                "acomodo de que los laboratorios no hay que rehacerlos para "
                "cada curso.",

                "El método de cada laboratorio es el del volumen anterior de "
                "esta serie: primero el razonamiento, después el circuito y "
                "recién entonces el programa. Un programa que se copia sin "
                "haber entendido qué problema resuelve no enseña nada, y "
                "cuando falla no hay por dónde empezar.",

                "Los errores que aparecen en estas páginas no son "
                "hipotéticos. Casi todos salieron de las guías que vengo "
                "usando en clase: un LED cableado al revés que hacía que "
                "<code>on()</code> lo apagara, un servomotor mandado contra "
                "su tope mecánico, un pulsador que ponía la fuente en "
                "cortocircuito, un servidor web que moría con la primera "
                "trama defectuosa del sensor. Están señalados con su síntoma "
                "y su causa porque un error explicado enseña más que un "
                "programa que siempre funcionó.",

                "Los programas están verificados uno por uno. No contra el "
                "criterio de quien los escribió, sino contra un simulador que "
                "comprueba la aritmética, los rangos y lo que ocurre cuando "
                "un sensor se desconecta. Aun así, la placa siempre tiene la "
                "última palabra: donde el libro da una constante de "
                "calibración, es la del sensor con que se escribió, y el "
                "apartado 3.5 explica cómo obtener la del suyo.",

                "Está pensado para que un estudiante pueda armar cada "
                "montaje con lo que hay en un laboratorio de una universidad "
                "pública. Ningún laboratorio necesita instrumental que no sea "
                "un multímetro, y los tres primeros del capítulo 4 no "
                "necesitan ni un sensor: la placa se genera las señales a sí "
                "misma.")
            + '</div>\n')


def indice(entradas):
    """Arma el índice a partir de (nivel, texto, pagina)."""
    filas = []
    for nivel, texto, pagina in entradas:
        clase = "ix-cap" if nivel == 0 else "ix-lab"
        filas.append('<tr class="{}"><td>{}</td><td class="n">{}</td></tr>'
                     .format(clase, esc(texto), pagina))
    return ('<div class="indice"><h2>Índice</h2><table>'
            + "".join(filas) + '</table></div>\n')
