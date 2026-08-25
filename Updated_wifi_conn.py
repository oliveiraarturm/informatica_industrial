import network
import time

SSID = "..."
PASSWORD = "..."

wifi = network.WLAN(network.STA_IF)

wifi.active(False)
time.sleep(1)

wifi.active(True)
time.sleep(1)

wifi.disconnect()
time.sleep(0.5)

print("Connecting to Wi-Fi...")
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(0.5)

print("Connected!")
print(wifi.ifconfig())
