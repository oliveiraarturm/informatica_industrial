import network
import time

from machine import Pin
from umodbus.tcp import ModbusTCP


# -------------------------
# Wi-Fi
# -------------------------

SSID = "Kitnet06"
PASSWORD = "478288324@"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(0.5)

ip = wifi.ifconfig()[0]

print("Wi-Fi connected")
print("IP:", ip)


# -------------------------
# LED
# -------------------------

led = Pin(2, Pin.OUT)
led.value(0)


# -------------------------
# Called when Elipse writes
# -------------------------

def led_write(reg_type, address, val):

    value = val[0]

    if value == 1:
        led.value(1)
        print("LED ON")

    else:
        led.value(0)
        print("LED OFF")


# -------------------------
# Modbus TCP
# -------------------------

modbus = ModbusTCP()

modbus.bind(
    local_ip=ip,
    local_port=502
)


# Holding Register 0
modbus.add_hreg(
    address=0,
    value=0,
    on_set_cb=led_write
)


print("Modbus TCP ready")
print("Register hr0 controls LED")
print("0 = OFF")
print("1 = ON")


# -------------------------
# Main loop
# -------------------------

while True:
    modbus.process()