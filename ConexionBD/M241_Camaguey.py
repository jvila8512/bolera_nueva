from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

class M221:
    def __init__(self, plc_ip, port=502):
        self.cliente = ModbusClient(plc_ip, port=port, timeout=3)
        self.conexion_exitosa = False

    def conectar(self):
        """Intenta conectar al PLC."""
        try:
            self.conexion_exitosa = self.cliente.connect()
            if self.conexion_exitosa:
                print("Conexión exitosa al PLC.")
            else:
                print("Error: No se pudo conectar al PLC.")
            return self.conexion_exitosa
        except ConnectionException as e:
            print(f"Error de conexión: {e}")
            return False

    def desconectar(self):
        """Desconecta del PLC."""
        self.cliente.close()
        print("Desconectado del PLC.")

    def leer_MW(self, address):
        """Lee una palabra de memoria (MW) y retorna su valor."""
        try:
            result = self.cliente.read_holding_registers(address, count=1)
            if result.isError():
                print(f"Error al leer MW{address}: {result}")
                return None
            return result.registers[0]
        except Exception as e:
            print(f"Error inesperado al leer MW{address}: {e}")
            return None

    def escribir_MW(self, address, value):
        """Escribe un valor en una palabra de memoria (MW)."""
        try:
            result = self.cliente.write_register(address, value)
            if result.isError():
                print(f"Error al escribir MW{address}: {result}")
                return False
            return True
        except Exception as e:
            print(f"Error inesperado al escribir MW{address}: {e}")
            return False

    def leer_bitM241(self, address, bit_number):
        """
        Lee un bit específico de la memoria M (por ejemplo, %MX20001.3).
        
        Parámetros:
            address (int): Dirección base Modbus (por ejemplo, 20001 para %MX20001).
            bit_number (int): Número del bit a leer (por ejemplo, 3 para .3).
        
        Retorna:
            El valor del bit (0 o 1), o None si hay un error.
        """
        try:
            result = self.cliente.read_coils(address + bit_number, count=1)
            if result.isError():
                print(f"Error al leer el bit en %MX{address}.{bit_number}: {result}")
                return None
            return result.bits[0]
        except Exception as e:
            print(f"Error inesperado al leer bit en %MX{address}.{bit_number}: {e}")
            return None

    def escribir_bit_M241(self, address, bit_number, value):
        """
        Escribe un bit específico en la memoria M (por ejemplo, %MX20001.3).
        
        Parámetros:
            address (int): Dirección base Modbus (por ejemplo, 20001 para %MX20001).
            bit_number (int): Número del bit a escribir (por ejemplo, 3 para .3).
            value (bool): Valor a escribir (True para 1, False para 0).
        
        Retorna:
            True si la escritura fue exitosa, False si hubo un error.
        """
        try:
            result = self.cliente.write_coil(address + bit_number, value)
            if result.isError():
                print(f"Error al escribir el bit en %MX{address}.{bit_number}: {result}")
                return False
            return True
        except Exception as e:
            print(f"Error inesperado al escribir bit en %MX{address}.{bit_number}: {e}")
            return False


# Programa principal
if __name__ == "__main__":
    # Configuración del PLC
    plc_ip = "192.168.0.1"  # Cambia esto por la IP de tu PLC
    plc = M221(plc_ip)

    # Conectar al PLC
    #if not plc.conectar():
     #   exit(1)  # Terminar el programa si no hay conexión

    # Leer M11 (%MX20001.3)
    valor_M11 = plc.leer_bitM241(20001, 3)
    if valor_M11 is not None:
        print(f"Valor de M11 (%MX20001.3): {valor_M11}")

    # Escribir 1 en M11 (%MX20001.3)
    if plc.escribir_bit_M241(20001, 3, True):
        print("Escritura exitosa en M11 (%MX20001.3).")

    # Leer MW10
    valor_MW10 = plc.leer_MW(10)
    if valor_MW10 is not None:
        print(f"Valor de MW10: {valor_MW10}")

    # Escribir en MW12
    if plc.escribir_MW(12, 1234):  # Escribir el valor 1234 en MW12
        print("Escritura exitosa en MW12.")

    # Mantener el programa en ejecución hasta que el usuario presione Enter
    input("Presiona Enter para salir...")

    # Desconectar del PLC
    plc.desconectar()