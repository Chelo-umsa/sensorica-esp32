# -*- coding: utf-8 -*-
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = wlan.config("mac")
print("MAC de esta placa:")
print("  legible  : " + ":".join("{:02X}".format(b) for b in mac))
print("  para el codigo del transmisor:")
escapada = "".join("\\x{:02x}".format(b) for b in mac)
print("    PAREJA = b'" + escapada + "'")
