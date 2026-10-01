# -*- coding: utf-8 -*-
from machine import Pin, SoftI2C

PIN_SCL = 22
PIN_SDA = 21

CONOCIDOS = {
    0x3C: "pantalla OLED SSD1306",
    0x3D: "pantalla OLED SSD1306 (direccion alternativa)",
    0x27: "pantalla LCD con adaptador PCF8574",
    0x68: "reloj DS1307 o acelerometro MPU6050",
    0x76: "sensor de presion BMP280 o BME280",
    0x77: "sensor de presion BMP280 (direccion alternativa)",
}

i2c = SoftI2C(scl=Pin(PIN_SCL), sda=Pin(PIN_SDA), freq=400000)

print("Explorando el bus I2C en SCL=GPIO{}, SDA=GPIO{}".format(
    PIN_SCL, PIN_SDA))
print("")

encontrados = i2c.scan()

if not encontrados:
    print("No contesta nadie.")
    print("  - Revise VCC y GND del modulo.")
    print("  - Revise que SCL y SDA no esten intercambiados.")
    print("  - Algunos modulos necesitan resistencias de elevacion.")
else:
    print("  direccion         que suele ser")
    for direccion in encontrados:
        nombre = CONOCIDOS.get(direccion, "desconocido")
        print("   0x{:02X}  ({:3d})    {}".format(
            direccion, direccion, nombre))
    print("")
    print("{} dispositivo(s) en el bus.".format(len(encontrados)))
