import asyncio

from rtu import RTU
from tcp import TCP


async def main():

    plc = RTU("COM2")
    tcp = TCP(port=1502)

    await plc.connect()
    await tcp.start()

    while True:

        value = await plc.read(0x4338)

        if value is not None:
            await tcp.write(0, value)
            print("D0 =", value)

        await asyncio.sleep(0.5)


asyncio.run(main())