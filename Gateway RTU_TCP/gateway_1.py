import asyncio

from rtu import RTU
from tcp import TCP


async def main():

    plc = RTU("COM2")
    tcp = TCP(port=1502)

    await plc.connect()
    await tcp.start()

    while True:

        value = await plc.read_hr(0x4338) 

        #######################################################
        # COLOQUE AQUI OS HOLDING REGISTERS DO SEU SUPERVISÓRIO
        #######################################################

        # valueX_HR = await plc.read_hr(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueX_HR = await plc.read_hr(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueX_HR = await plc.read_hr(0xENDEREÇO_TPW_HEXADECIMAL) 



        ###########################################################
        # COLOQUE AQUI AS MEMÓRIAS DO SEU SUPERVISÓRIO M1,M2,M3....
        ###########################################################

        # valueX_M = await plc.read_memory(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueX_M = await plc.read_memory(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueX_M = await plc.read_memory(0xENDEREÇO_TPW_HEXADECIMAL) 



        if value is not None:
            
            await tcp.write_hr(0, value)

            #############################################
            # ESCREVER OS HOLDING REGISTERS NO MODBUS TCP  
            #############################################


            #await tcp.write_hr(X, valueX_HR)   
            #await tcp.write_hr(X, valueX_HR)
            #await tcp.write_hr(X, valueX_HR)   

            #############################################
            # ESCREVER AS MEMÓRIAS NO MODBUS TCP  
            #############################################


            #await tcp.write_memory(X, valueX_M)   
            #await tcp.write_memory(X, valueX_M)
            #await tcp.write_memory(X, valueX_M)   



            print("D0 =", value)

        await asyncio.sleep(0.5)


asyncio.run(main())