import network
import time
from umodbus.tcp import ModbusTCP

# -------------------------
# Wi-Fi
# -------------------------

SSID = "ssid"
PASSWORD = 

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():
    print("Connecting Wi-Fi...")
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(0.5)

ip = wifi.ifconfig()[0]

print("Connected")
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
# Counter
# -------------------------

counter = 0


def register_read(reg_type, address, val):
    global counter

    counter += 1

    if counter > 65535:
        counter = 0

    modbus.set_hreg(
        address=0,
        value=counter
    )

    print("Elipse read register:", counter)


# Holding Register 0
modbus.add_hreg(
    address=0,
    value=0,
    on_get_cb=register_read
)


print("Modbus TCP ready")
print("Holding Register 0")


# -------------------------
# Main loop
# -------------------------

while True:
    modbus.process()
