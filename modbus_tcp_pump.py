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
    print("Connecting Wi-Fi...")
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(0.5)

ip = wifi.ifconfig()[0]

print("Connected")
print("IP:", ip)


# -------------------------
# LED = Pump
# -------------------------

led = Pin(2, Pin.OUT)
led.value(0)


# -------------------------
# Variables
# -------------------------

level = 0
pump_running = False

HIGH_LEVEL = 80


# -------------------------
# Modbus TCP
# -------------------------

modbus = ModbusTCP()

modbus.bind(
    local_ip=ip,
    local_port=502
)


# -------------------------
# Pump command callback
# -------------------------

def pump_write(reg_type, address, val):
    global pump_running

    value = val[0]

    if value == 1 and level < HIGH_LEVEL:
        pump_running = True
        led.value(1)
        print("Pump ON")

    else:
        pump_running = False
        led.value(0)
        print("Pump OFF")


# -------------------------
# Registers
# -------------------------

# hr0 -> Pump command
modbus.add_hreg(
    address=0,
    value=0,
    on_set_cb=pump_write
)

# hr1 -> Tank level
modbus.add_hreg(
    address=1,
    value=0
)

# hr2 -> High-level alarm
modbus.add_hreg(
    address=2,
    value=0
)


print("Modbus TCP ready")
print("hr0 = Pump")
print("hr1 = Level")
print("hr2 = Alarm")


# -------------------------
# Tank simulation
# -------------------------

last_update = time.ticks_ms()

while True:

    modbus.process()

    # Update tank every second
    if time.ticks_diff(time.ticks_ms(), last_update) >= 1000:

        last_update = time.ticks_ms()

        if pump_running:

            level += 5

            if level > 100:
                level = 100

            modbus.set_hreg(
                address=1,
                value=level
            )

            print("Level:", level, "%")

            # -------------------------
            # High-level alarm
            # -------------------------

            if level >= HIGH_LEVEL:

                pump_running = False
                led.value(0)

                # Pump command -> OFF
                modbus.set_hreg(
                    address=0,
                    value=0
                )

                # Alarm -> ON
                modbus.set_hreg(
                    address=2,
                    value=1
                )

                print("HIGH LEVEL ALARM!")
                print("Pump stopped")