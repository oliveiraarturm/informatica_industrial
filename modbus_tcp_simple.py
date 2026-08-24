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

# -------------------------
# Holding Register 0
# -------------------------

registers = {
    "HREGS": {
        "TEST": {
            "register": 0,
            "len": 1,
            "val": 123
        }
    }
}

modbus.setup_registers(registers=registers)

print("Modbus TCP started ✅")
print("Port: 502")
print("Holding Register 0 = 123")

# -------------------------
# Main loop
# -------------------------

while True:
    modbus.process()
