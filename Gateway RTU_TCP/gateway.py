import asyncio

from rtu import RTU
from tcp import TCP


async def main():

    tcp = TCP(port=1502)
    plc = RTU("COM2")

    await plc.connect()
    await tcp.start()



    while True:


        #######################################################
        # COLOQUE AQUI OS HOLDING REGISTERS DO SEU SUPERVISÓRIO
        #######################################################

        valueHR_0 = await plc.read_hr(0x4338) 
        valueHR_1 = await plc.read_hr(0x4339) 
        valueHR_2 = await plc.read_hr(0x433A) 
        

        ###########################################################
        # COLOQUE AQUI AS MEMÓRIAS DO SEU SUPERVISÓRIO M1,M2,M3....
        ###########################################################

        valueM_0 = await plc.read_memory(0x0200) 
        valueM_1 = await plc.read_memory(0x0201) 
        valueM_2 = await plc.read_memory(0x0202)
        

        values = [
        valueHR_0, valueHR_1, valueHR_2,
        valueM_0, valueM_1, valueM_2
        ]

        if all(x is not None for x in values):
            

            #############################################
            # ESCREVER OS HOLDING REGISTERS NO MODBUS TCP  
            #############################################


            await tcp.write_hr(0, valueHR_0)
            await tcp.write_hr(1, valueHR_1)   
            await tcp.write_hr(2, valueHR_2)
             

            #############################################
            # ESCREVER AS MEMÓRIAS NO MODBUS TCP  
            #############################################


            await tcp.write_memory(0, valueM_0)   
            await tcp.write_memory(1, valueM_1)
            await tcp.write_memory(2, valueM_2)   

  
        print(
            "valueHR_0:", valueHR_0,
            "valueHR_1:", valueHR_1,
            "valueHR_2:", valueHR_2,
            "valueM_0:", valueM_0,
            "valueM_1:", valueM_1,
            "valueM_2:", valueM_2,
            sep="\n"
        )

        # M_0 = await tcp.read_memory(0)
        # M_1 = await tcp.read_memory(1)
        # M_2 = await tcp.read_memory(2)

        # await plc.write_memory(0x0200, M_0)
        # await plc.write_memory(0x0201, M_1)
        # await plc.write_memory(0x0202, M_2)

        # HR_X = await tcp.read_hr(X)

        # await plc.write_hr(0xENDEREÇO_TPW_HEXADECIMAL, HR_X)
         
        await asyncio.sleep(.2)


asyncio.run(main())