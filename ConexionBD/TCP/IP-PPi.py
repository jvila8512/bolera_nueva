import snap7
from snap7.exceptions import Snap7Exception


class S7Connection:
    def __init__(self, ip, local_tsap, remote_tsap):
        """
        Inicializa los parámetros de conexión para el PLC S7-200.
        :param ip: Dirección IP del PLC.
        :param local_tsap: TSAP local (lado de la PC).
        :param remote_tsap: TSAP remoto (lado del PLC).
        """
        self.ip = ip
        self.local_tsap = local_tsap
        self.remote_tsap = remote_tsap
        self.client = snap7.client.Client()

    def set_connection_params(self):
        """
        Configura los parámetros de conexión utilizando Cli_SetConnectionParams.
        """
        try:
            self.client.set_connection_params(self.ip, self.local_tsap, self.remote_tsap)
            print(f"Parámetros de conexión configurados:\n  IP: {self.ip}\n  TSAP Local: {hex(self.local_tsap)}\n  TSAP Remoto: {hex(self.remote_tsap)}")
        except Snap7Exception as e:
            raise Exception(f"Error al configurar los parámetros de conexión: {e}")

    def connect(self):
        """
        Establece la conexión con el PLC.
        """
        try:
            self.client.connect()
            print(f"Conexión establecida con el PLC en {self.ip}.")
        except Snap7Exception as e:
            raise Exception(f"Error al conectar con el PLC: {e}")

    def disconnect(self):
        """
        Cierra la conexión con el PLC.
        """
        try:
            self.client.disconnect()
            print("Conexión cerrada correctamente.")
        except Snap7Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    def read_data(self, area, db_number, start, size):
        """
        Lee datos del PLC.
        :param area: Área de datos (ej. snap7.types.areas.PE para entradas).
        :param db_number: Número de bloque de datos (usualmente 0 para áreas no DB).
        :param start: Dirección inicial a leer.
        :param size: Tamaño de los datos a leer (en bytes).
        :return: Datos leídos.
        """
        try:
            data = self.client.read_area(area, db_number, start, size)
            print(f"Datos leídos desde el PLC: {data}")
            return data
        except Snap7Exception as e:
            raise Exception(f"Error al leer datos del PLC: {e}")

    def write_data(self, area, db_number, start, data):
        """
        Escribe datos en el PLC.
        :param area: Área de datos (ej. snap7.types.areas.PE para entradas).
        :param db_number: Número de bloque de datos (usualmente 0 para áreas no DB).
        :param start: Dirección inicial donde escribir.
        :param data: Datos a escribir (bytes).
        """
        try:
            self.client.write_area(area, db_number, start, data)
            print(f"Datos escritos en el PLC: {data}")
        except Snap7Exception as e:
            raise Exception(f"Error al escribir datos en el PLC: {e}")
        
        
from snap7.type import areas

# Dirección IP del PLC
plc_ip = "192.168.1.188"

# TSAP Local y Remoto (en hexadecimal)
local_tsap = 0x0200  # TSAP local de la PC
remote_tsap = 0x0300  # TSAP remoto del PLC

# Crear una instancia de la clase
plc = S7Connection(plc_ip, local_tsap, remote_tsap)

# Configurar y establecer conexión
try:
    plc.set_connection_params()
    plc.connect()

    # Leer datos de la memoria de entrada (ejemplo)
    data = plc.read_data(areas.PE, 0, 0, 4)  # Lee 4 bytes desde el área de entradas

    # Escribir datos en la memoria de salida (ejemplo)
    plc.write_data(areas.PA, 0, 0, b'\x01\x02\x03\x04')  # Escribe 4 bytes en el área de salidas

finally:
    # Asegúrate de desconectar
    plc.disconnect()       