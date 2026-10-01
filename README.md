# Programación aplicada a la sensórica industrial y automotriz

**ESP32, MicroPython y monitoreo IoT**

Programas, módulos y diagramas del libro. Cada programa de la carpeta
`programas/` es **el mismo texto que está impreso**: se extrae del libro
al compilarlo, de modo que no puede haber diferencia entre lo que se lee
en la página y lo que se copia a la placa.

## Antes de empezar

1. Copie `programas/config_ejemplo.py` con el nombre `config.py`.
2. Abra `config.py` y complete los cuatro datos: el nombre y la clave de
   su red inalámbrica, y su usuario y su clave de Adafruit IO.
3. Copie al ESP32 los archivos que use el laboratorio. El anexo B del
   libro dice cuáles son y cómo copiarlos con Thonny.

`config.py` **no se comparte ni se sube a ningún repositorio**. La clave
de Adafruit IO permite leer, escribir y borrar en toda la cuenta, de modo
que quien la tenga puede alterar los datos. Por eso figura en
`.gitignore`, y por eso ningún programa del libro la lleva escrita
adentro.

## Qué hay en cada carpeta

| Carpeta | Contenido |
|---|---|
| `programas/` | Un archivo por cada programa impreso, con el nombre con que aparece en el libro. Es lo que se copia a la placa. |
| `figuras/` | Los diagramas de conexión, en SVG y en PNG. Sirven para la diapositiva y para mirarlos en el celular mientras se arma el montaje. |
| `libro/` | El sistema que compone el libro y lo verifica, con el simulador en `libro/sim/`. Sólo hace falta para reconstruir el PDF. |

El PDF del libro está en la raíz, como `libro.pdf`.

## Los módulos que se copian a la placa

| Archivo | Para qué | Laboratorios |
|---|---|---|
| `config.py` | Guarda las claves fuera del programa. Se hace copiando `config_ejemplo.py`; **no está en el repositorio y no debe subirse**. | 7.1 en adelante |
| `programas/iot.py` | Conexión a la red y al servidor. | 7.1 y 7.6 a 7.9 |
| `ssd1306.py` (aparte) | Controlador de la pantalla OLED. Es de la biblioteca oficial de MicroPython. | 6.1, 6.2, 6.6 |
| `programas/ble_uart.py` | Puerto serie sobre Bluetooth. | 7.4 |
| `programas/pzem.py` | Protocolo Modbus del medidor eléctrico. | 6.5 |

## Un aviso sobre el laboratorio 2.5

Es el único del libro con tensión de red. El lado de 220 V no se cablea
en protoboard: va a los tornillos de la bornera del módulo de relé, con
conductor de instalación. Se arma desenchufado, se comprueba el
chasquido del relé antes de conectar la carga, y el relé corta la
**fase**, nunca el neutro. Los laboratorios 7.8 y 7.9 gobiernan ese
mismo montaje a distancia y heredan las mismas reglas.

## Cómo se comprueba

Los programas no se dan por buenos porque parezcan correctos. Cada
capítulo tiene su archivo de verificación, que los corre contra el
simulador y revisa la aritmética, los rangos y qué pasa cuando un sensor
se desconecta. Desde la raíz del repositorio:

```
python3 libro/verificar_cap3.py      # y cap12, cap4, cap5, cap6, cap7
```

Los diagramas también se revisan solos, porque un cable encima del
número de un pin no se ve al escribir las coordenadas:

```
python3 libro/revisar_figuras.py     # cables sobre rótulos y cruces sin salto
```

Y el libro entero se reconstruye con:

```
python3 libro/construir_libro.py     # produce libro.pdf y regenera programas/
python3 libro/exportar_figuras.py    # regenera figuras/
```

La compilación falla si alguna línea de código pasa de 72 caracteres —no
entraría en la caja impresa—, si alguna figura supera los 176 mm de alto,
o si el nombre de un programa no coincide con el número de su
laboratorio.

## Calibración

Donde el libro da una constante —el Beta del termistor, el cero y el
fondo de escala del HX710B, el desvío del LM35— es la del sensor con el
que se escribió. El apartado 3.5 explica el procedimiento de dos puntos
para obtener la del suyo, que es de dos mediciones y una resta.

## Licencia

Los programas, bajo licencia MIT. El texto, las figuras y los diagramas,
bajo Creative Commons BY-NC-SA 4.0.
