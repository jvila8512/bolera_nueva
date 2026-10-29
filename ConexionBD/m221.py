import datetime
from pymodbus.client import ModbusTcpClient as ModbusClient


plc_ip='127.0.0.1'
port=502
cliente = ModbusClient("localhost")

       
cliente.connect()

print('Conexcion establecida')


write=cliente.write_register(2,8000)
read=cliente.read_holding_registers(2)

escribir=cliente.write_coil(0, True)
escribir1=cliente.write_coil(0x01, True)

leerbit=cliente.read_coils(0)

print('Lectura de Registro MW2= ',read.registers[0])
print('Lectura de un bit de M0', leerbit.bits[0])

"""Lee un bit específico de una palabra de memoria."""
try:
    result = cliente.read_coils(1) #Usamos read_coils para bits
    if result.isError():
            print(f"Error al leer el bit: {result}")
           
    print('Bit de M0',result.bits[0])
except Exception as e:
        print(f"Error inesperado al leer bit: {e}")
        


cliente.close()

