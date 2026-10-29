import snap7
import struct
from typing import Union, List, Tuple

class PLCS71200:
    def __init__(self, ip='192.168.0.1', rack=0, slot=1):
        """Inicializa la conexión con el PLC S7-1200"""
        self.client = snap7.client.Client()
        self.connected = False
        try:
            self.client.connect(ip, rack, slot)
            self.connected = True
        except Exception as e:
            raise ConnectionError(f"Error de conexión: {str(e)}")

    def check_connection(self):
        """Verifica el estado de la conexión"""
        if not self.connected:
            raise ConnectionError("No hay conexión con el PLC")
        return True

    def read_db(self, db_number: int, start_offset: int, size: int) -> bytearray:
        """
        Lee datos de un DB
        db_number: número del DB
        start_offset: dirección inicial
        size: cantidad de bytes a leer
        """
        self.check_connection()
        try:
            return self.client.db_read(db_number, start_offset, size)
        except Exception as e:
            raise ValueError(f"Error al leer DB{db_number}: {str(e)}")

    def write_db(self, db_number: int, start_offset: int, data: bytearray):
        """
        Escribe datos en un DB
        db_number: número del DB
        start_offset: dirección inicial
        data: datos a escribir
        """
        self.check_connection()
        try:
            self.client.db_write(db_number, start_offset, data)
        except Exception as e:
            raise ValueError(f"Error al escribir en DB{db_number}: {str(e)}")

    def read_memory(self, area: str, address: int, size: int) -> bytearray:
        """
        Lee memoria del PLC (MW, VW, etc)
        area: tipo de área ('M', 'V', etc)
        address: dirección de memoria
        size: cantidad de bytes a leer
        """
        self.check_connection()
        area_code = {
            'M': snap7.type.Areas.MK,
            'V': snap7.type.Areas.DB,
            'I': snap7.type.Areas.PE,
            'Q': snap7.type.Areas.PA
        }
        
        try:
            return self.client.read_area(area_code[area], 0, address, size)
        except Exception as e:
            raise ValueError(f"Error al leer área {area}: {str(e)}")

    def write_memory(self, area: str, address: int, data: bytearray):
        """
        Escribe en memoria del PLC
        area: tipo de área ('M', 'V', etc)
        address: dirección de memoria
        data: datos a escribir
        """
        self.check_connection()
        area_code = {
            'M': snap7.types.Areas.MK,
            'V': snap7.types.Areas.DB,
            'I': snap7.types.Areas.PE,
            'Q': snap7.types.Areas.PA
        }
        
        try:
            self.client.write_area(area_code[area], 0, address, data)
        except Exception as e:
            raise ValueError(f"Error al escribir en área {area}: {str(e)}")

    def read_bit(self, area: str, byte_address: int, bit_position: int) -> bool:
        """
        Lee un bit específico
        area: tipo de área ('M', 'V', etc)
        byte_address: dirección del byte
        bit_position: posición del bit (0-7)
        """
        if not 0 <= bit_position <= 7:
            raise ValueError("Posición del bit debe estar entre 0 y 7")
            
        byte_data = self.read_memory(area, byte_address, 1)
        return bool((byte_data[0] >> bit_position) & 1)

    def write_bit(self, area: str, byte_address: int, bit_position: int, value: bool):
        """
        Escribe un bit específico
        area: tipo de área ('M', 'V', etc)
        byte_address: dirección del byte
        bit_position: posición del bit (0-7)
        value: valor a escribir (True/False)
        """
        if not 0 <= bit_position <= 7:
            raise ValueError("Posición del bit debe estar entre 0 y 7")
            
        byte_data = self.read_memory(area, byte_address, 1)
        if value:
            byte_data[0] |= (1 << bit_position)
        else:
            byte_data[0] &= ~(1 << bit_position)
            
        self.write_memory(area, byte_address, byte_data)

    def  read_real(self, area: str, address: int) -> float:
        """Lee un número real (REAL) de 4 bytes"""
        data = self.read_memory(area, address, 4)
        return struct.unpack('>f', data)[0]

    def write_real(self, area: str, address: int, value: float):
        """Escribe un número real (REAL) de 4 bytes"""
        data = struct.pack('>f', value)
        self.write_memory(area, address, bytearray(data))

    def close(self):
        """Cierra la conexión con el PLC"""
        if self.connected:
            self.client.disconnect()
            self.connected = False
            # Crear instancia del PLC
plc = PLCS71200()

try:
   
    # Leer word de memoria V
    word_data = plc.read_memory('V', 0, 1)
    valor_word = struct.unpack('>H', word_data)[0]
    print(f"Valor word: {valor_word}")

finally:
    plc.close()