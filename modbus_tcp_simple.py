import network
import time
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

print("Wi-Fi connected ✅")
print("IP:", ip)

# -------------------------
# Modbus TCP
# -------------------------

modbus = ModbusTCP()

modbus.bind(
    local_ip=ip,
    local_port=502
)


def register_read(reg_type, address, val):

    print("Elipse read register!")


# -------------------------
# Holding Register 0
# -------------------------

modbus.add_hreg(
    address=0,
    value=123,
    on_get_cb = register_read
)



print("Modbus TCP started ✅")
print("Port: 502")


# -------------------------
# Main loop
# -------------------------

while True:
    modbus.process()
