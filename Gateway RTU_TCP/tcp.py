import asyncio

from pymodbus.server import ModbusTcpServer
from pymodbus.simulator import SimDevice, SimData, DataType


class TCP:
    """Modbus TCP server with separate holding-register and coil areas."""

    def __init__(self, port=1502, device_id=1, count=100):
        self.device_id = device_id

        device = SimDevice(

            device_id,

            (
                [SimData(0, count=count, values=False, datatype=DataType.BITS)],
                
                [SimData(0, count=count, values=0, datatype=DataType.REGISTERS)],
               
            ),
            
        )

        self.server = ModbusTcpServer(

            device,

            address=("0.0.0.0", port),

        )

    async def start(self):

        self.task = asyncio.create_task(self.server.serve_forever())


    async def write_hr(self, address, value):

        await self.server.async_setValues(

            self.device_id, 6, address, [int(value)]

        )

        return True

    async def write_memory(self, address, value):

        await self.server.async_setValues(

            self.device_id, 5, address, [bool(value)]

        )

        return True