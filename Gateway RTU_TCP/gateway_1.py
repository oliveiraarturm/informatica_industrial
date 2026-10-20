import asyncio

from rtu import RTU
from tcp import TCP


async def main():

    tcp = TCP(port=1502)
    plc = RTU("COM2")

    await plc.connect()
    await tcp.start()

    last_command = None
    last_hr_command = await tcp.read_hr(1)

    while True:

        value = await plc.read_hr(0x4338) 

        #######################################################
        # COLOQUE AQUI OS HOLDING REGISTERS DO SEU SUPERVISÓRIO
        #######################################################

        # valueHR_X = await plc.read_hr(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueHR_X = await plc.read_hr(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueHR_X = await plc.read_hr(0xENDEREÇO_TPW_HEXADECIMAL) 



        ###########################################################
        # COLOQUE AQUI AS MEMÓRIAS DO SEU SUPERVISÓRIO M1,M2,M3....
        ###########################################################

        # valueM_X = await plc.read_memory(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueM_X = await plc.read_memory(0xENDEREÇO_TPW_HEXADECIMAL) 
        # valueM_X = await plc.read_memory(0xENDEREÇO_TPW_HEXADECIMAL)
        

        

        if value is not None:
            
            await tcp.write_hr(0, value)

            #############################################
            # ESCREVER OS HOLDING REGISTERS NO MODBUS TCP  
            #############################################


            #await tcp.write_hr(X, valueHR_X)   
            #await tcp.write_hr(X, valueHR_X)
            #await tcp.write_hr(X, valueHR_X)   

            #############################################
            # ESCREVER AS MEMÓRIAS NO MODBUS TCP  
            #############################################


            #await tcp.write_memory(X, valueM_X)   
            #await tcp.write_memory(X, valueM_X)
            #await tcp.write_memory(X, valueM_X)   



            print("D0 =", value)
            

        command_m = await tcp.read_memory(X)


        if command_m is not None and command_m != last_command:

            success = await plc.write_memory(0xENDEREÇO_TPW_HEXADECIMAL, command_m)

   



        command_hr = await tcp.read_hr(X)

        if command_hr != last_hr_command:

            await plc.write_hr(0xENDEREÇO_TPW_HEXADECIMAL, command_hr)

          

        await asyncio.sleep(0.5)


asyncio.run(main())