from pymodbus.client import AsyncModbusSerialClient


class RTU:
    def __init__(self, port, device_id=1):
        self.device_id = device_id
        self.client = AsyncModbusSerialClient(
            port=port,
            baudrate=19200,
            bytesize=8,
            parity="N",
            stopbits=2,
            timeout=2,
        )

    async def connect(self):
        await self.client.connect()

    async def read(self, address):
        r = await self.client.read_holding_registers(
            address=address,
            count=1,
            device_id=self.device_id,
        )

        if r.isError():
            return None

        return r.registers[0]