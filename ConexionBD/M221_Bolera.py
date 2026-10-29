from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

class M221():   
    def __init__(self,plc_ip,port=502):        
       
        self.cliente = ModbusClient(plc_ip)
        self.conexion_exitosa = False  # Variable para rastrear el estado de la conexión
       # self.cliente = ModbusClient(plc_ip,port)
    def connectar(self):
        try:
          
            self.cliente.connect()
            if self.cliente.is_socket_open():
                self.conexion_exitosa = True
                print("Conexión Modbus exitosa.")
                return  self.conexion_exitosa
            else:
                self.conexion_exitosa = False
                print("Error: No se pudo abrir el socket.")
                return  self.conexion_exitosa
            
            
        except ConnectionException as e:
           self.conexion_exitosa = False
           print(f"Error de conexión Modbus: {e}")
        except Exception as e:
            self.conexion_exitosa = False
            print(f"Error inesperado al conectar: {e}")

    def desconectar(self):
      if self.cliente:
            self.cliente.close()
            print("Conexión Modbus cerrada.")   
       
       
       
       
       
       
    
    def leer_MW(self,address):
        """Lee una palabra de memoria y retorna los bits individuales."""
        try:
            result = self.cliente.read_holding_registers(address)
            if result.isError():
                print(f"Error al leer la palabra de memoria: {result}")
                return None
            word = result.registers[0]
           # bits = [(word >> i) & 1 for i in range(15, -1, -1)]
            return word
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
    def escribir_bit_M241(self, address, bit_number, value):
        """
        Escribe un bit específico en una dirección de memoria.
        
        Parámetros:
            address (int): Dirección base Modbus (por ejemplo, 20000 para %MX20000).
            bit_number (int): Número del bit a escribir (0 para .1, 1 para .2, etc.).
            value (bool): Valor a escribir (True para 1, False para 0).
        
        Retorna:
            True si la escritura fue exitosa, False si hubo un error.
        """
        try:
            # Calcular la dirección Modbus del bit específico
            modbus_address = address + bit_number
            
            # Escribir el bit usando write_coil
            result = self.cliente.write_coil(modbus_address, value)
            
            if result.isError():
                print(f"Error al escribir el bit: {result}")
                return False
            return True
        except Exception as e:
            print(f"Error inesperado al escribir bit: {e}")
            return False    
    def escribir_bit_M( self,address, bit_number, value):
        """Escribe un bit específico en una palabra de memoria."""
        try:
            result = self.cliente.write_coil(address, value) #Usamos write_coil para bits
            if result.isError():
                print(f"Error al escribir el bit: {result}")
                return False
            return True
        except Exception as e:
            print(f"Error inesperado al escribir bit: {e}")
            return False
    def leer_bitM241(self, address, bit_number):
        """
        Lee un bit específico de una dirección de memoria.
        
        Parámetros:
            address (int): Dirección base Modbus (por ejemplo, 20001 para %MX20001).
            bit_number (int): Número del bit a leer (por ejemplo, 3 para .3).
        
        Retorna:
            El valor del bit (0 o 1), o None si hay un error.
        """
        try:
            # Calcular la dirección Modbus del bit específico
            modbus_address = address + bit_number
            
            # Leer el coil específico
            result = self.cliente.read_coils(modbus_address, count=1)
            if result.isError():
                print(f"Error al leer el bit en %MX{address}.{bit_number}: {result}")
                return None
            
            # Retornar el valor del bit
            return result.bits[0]
        except Exception as e:
            print(f"Error inesperado al leer bit en %MX{address}.{bit_number}: {e}")
            return None
    def leer_bit(self, address, bit_number):

        """Lee un bit específico de una palabra de memoria."""
        try:
            result = self.cliente.read_coils(address) #Usamos read_coils para bits
            if result.isError():
                print(f"Error al leer el bit: {result}")
                return None
            return result.bits[0]
        except Exception as e:
            print(f"Error inesperado al leer bit: {e}")
            return None
    def escribir_MW(self, address, value):

        """Escribe un valor en una MW en memoria."""
        try:
            result = self.cliente.write_register(address, value)
            if result.isError():
                print(f"Error al escribir en la palabra de memoria: {result}")
                return False
            return True
        except Exception as e:
            print(f"Error inesperado al escribir: {e}")
            return False    


import time
import datetime
if __name__ == "__main__":
    ip_address = "192.168.0.1"  # Reemplaza con la IP de tu PLC
    port = 502
    cliente = M221(ip_address)
    bandera=True

    try:       
        conexion =cliente.connectar()     

        while conexion:
            timestamp = datetime.datetime.now().isoformat()
   
            print("Se establecio comunicación con el Automata M221 IP -", ip_address )
            if bandera:
                
                 # Leer M11 (%MX20001.3)
                valor_M11 = cliente.leer_bitM241(20001, 3)
                if valor_M11 is not None:
                    print(f"Valor de M11 (%MX20001.3): {valor_M11}")

                # Escribir 1 en M11 (%MX20001.3)
                if cliente.escribir_bit_M241(20001, 3, True):
                    print("Escritura exitosa en M11 (%MX20001.3).")

                # Leer MW10
                valor_MW10 =cliente.leer_MW(10)
                if valor_MW10 is not None:
                    print(f"Valor de MW10: {valor_MW10}")

                # Escribir en MW12
                if cliente.escribir_MW(12, 1234):  # Escribir el valor 1234 en MW12
                    print("Escritura exitosa en MW12.")
                
                #escritura=cliente.escribir_MW(2,52)
                #read=cliente.leer_MW(2)
                #print('Lectura de Registro MW2= ',read)

               # escribir=cliente.escribir_bit_M(0,1, True)
                escribir1=cliente.escribir_bit_M(0x01,1, True) 
               # if escribir:
                # print('Se escribio en %M0= Activo')
                #if escribir1 :
                # print('Se escribio en %M1= Activo')

                #leerbit=cliente.leer_bit(0,1)
                #print('Lectura de un bit de M0', leerbit)
                #escritura=cliente.escribir_MW(10,2000)
            bandera=False 
            
            
             # Leer M11 (%MX20001.3)
            valor_M11 = cliente.leer_bitM241(20001, 3)
            if valor_M11 is not None:
                    print(f"Valor de M11 (%MX20001.3): {valor_M11}") 
             # Leer MW10
            valor_MW10 =cliente.leer_MW(10)
            if valor_MW10 is not None:
                    print(f"Valor de %MW10: {valor_MW10}")
            
            
            
            

            time.sleep(2)  # Espera 1 segundo
    except KeyboardInterrupt:
         print("Programa interrumpido por el usuario.")
    except Exception as e:
         print(f"Error general DEbemos Revisarrrrrrrr: {e}")
         
    finally:
         
            cliente.desconectar()


   