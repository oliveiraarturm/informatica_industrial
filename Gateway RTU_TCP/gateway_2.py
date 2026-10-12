import asyncio

from pymodbus.client import AsyncModbusTcpClient

from rtu import RTU


async def main():

    # PLC2 RTU connection
    plc2 = RTU("COM4")

    # Connect to Gateway 1 TCP server
    tcp = AsyncModbusTcpClient(
        "127.0.0.1",
        port=1502
    )

    await plc2.connect()
    await tcp.connect()

    print("Gateway 2 running")

    while True:

        result = await tcp.read_holding_registers(
            address=0,
            count=1,
            device_id=1
        )

        if not result.isError():

            value = result.registers[0]

            # Force digital behaviour
            value = 1 if value else 0

            # PLC2 D0
            await plc2.write(
                0x4338,
                value
            )

            print("PLC2 D0 =", value)

        await asyncio.sleep(0.1)


asyncio.run(main())