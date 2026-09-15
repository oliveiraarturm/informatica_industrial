from pymodbus.client import ModbusSerialClient

PORT = "COM9"       # change this
PLC_ID = 1          # Modbus slave address

client = ModbusSerialClient(
    port=PORT,
    baudrate=19200,
    bytesize=8,
    parity="N",
    stopbits=2,
    timeout=2
)

print("Opening", PORT)

if not client.connect():
    print("Could not open COM port")
    quit()

print("COM port opened")

# TPW04:
# D0 = 0x4338
response = client.read_holding_registers(
    address=0x4338,
    count=1,
    device_id=PLC_ID
)

if response.isError():
    print("Modbus error:", response)
else:
    print("D0 =", response.registers[0])

client.close()
