import asyncio

from pymodbus.server import ModbusTcpServer
from pymodbus.simulator import SimDevice, SimData, DataType


class TCP:

    def __init__(self, port=1502, device_id=1):

        self.device_id = device_id

        device = SimDevice(
            device_id,
            SimData(
                0,
                values=[0] * 100,
                datatype=DataType.REGISTERS,
            )
        )

        self.server = ModbusTcpServer(
            device,
            address=("0.0.0.0", port),
        )

    async def start(self):

        self.task = asyncio.create_task(
            self.server.serve_forever()
        )

    async def write(self, address, value):

        await self.server.async_setValues(
            self.device_id,
            3,
            address,
            [value],
        )