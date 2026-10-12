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

    async def read_hr(self, address):
        r = await self.client.read_holding_registers(
            address=address,
            count=1,
            device_id=self.device_id,
        )

        if r.isError():
            return None

        return r.registers[0]

    async def read_memory(self, address):
        r = await self.client.read_coils(
            address=address,
            count=1,
            device_id=self.device_id,
        )

        if r.isError():
            return None

        return r.bits[0]

    async def write_hr(self, address, value):

        r = await self.client.write_register(
            address=address,
            value=value,
            device_id=self.device_id,
        )

        if r.isError():
            return False

        return True

    async def write_memory(self, address, value):

        r = await self.client.write_coil(
            address=address,
            value=bool(value),
            device_id=self.device_id,
        )

        if r.isError():
            return False

        return True


 