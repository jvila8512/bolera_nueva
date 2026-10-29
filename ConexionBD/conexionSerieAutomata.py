import serial
import struct
import time

class PLCS7200:
    def __init__(self, port='COM2', baudrate=9600):
        
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            timeout=2
        )
        self.plc_address = 2  # Dirección por defecto del PLC
        
    def _calculate_checksum(self, data):
        return sum(data) & 0xFF
    
    def _verify_response(self, response):
        if len(response) < 3:
            raise Exception("Respuesta incompleta del PLC")
        if response[0] != 0x68:
            raise Exception("Cabecera de respuesta inválida")
        checksum = self._calculate_checksum(response[:-2])
        if checksum != response[-2]:
            raise Exception("Error de checksum en la respuesta")
            
    def read_vw(self, address, length=1):
        """Lee palabras (words) de la memoria V"""
        command = [
            0x68,                   # Inicio
            0x1B,                   # Longitud
            0x1B,                   # Longitud repetida
            0x68,                   # Inicio repetido
            self.plc_address,       # Dirección del PLC
            0x6C,                   # Comando de lectura
            0x32,                   # Tipo de área (VW)
            address >> 8,           # Dirección High
            address & 0xFF,         # Dirección Low
            length                  # Cantidad de words
        ]
        
        command.append(self._calculate_checksum(command))
        command.append(0x16)        # Fin de trama
        
        self.serial.write(bytes(command))
        response = self.serial.read(length * 2 + 10)       
        if len(response) == 0:
         raise Exception("No se recibió respuesta del PLC")
        
        self._verify_response(response)
        
        return struct.unpack(f'>{length}H', response[10:-2])
        
    def write_vw(self, address, value):
        """Escribe una palabra (word) en la memoria V"""
        command = [
            0x68,                   # Inicio
            0x1D,                   # Longitud
            0x1D,                   # Longitud repetida
            0x68,                   # Inicio repetido
            self.plc_address,       # Dirección del PLC
            0x7C,                   # Comando de escritura
            0x32,                   # Tipo de área (VW)
            address >> 8,           # Dirección High
            address & 0xFF,         # Dirección Low
            0x01,                   # Cantidad de words
            value >> 8,             # Valor High
            value & 0xFF            # Valor Low
        ]
        
        command.append(self._calculate_checksum(command))
        command.append(0x16)        # Fin de trama
        
        self.serial.write(bytes(command))
        response = self.serial.read(10)
        self._verify_response(response)
        
    def read_bit(self, byte_address, bit_position):
        """Lee un bit específico de la memoria V"""
        if not 0 <= bit_position <= 7:
            raise ValueError("Posición del bit debe estar entre 0 y 7")
            
        word_data = self.read_vw(byte_address)[0]
        return (word_data >> bit_position) & 1
        
    def write_bit(self, byte_address, bit_position, value):
        """Escribe un bit específico en la memoria V"""
        if not 0 <= bit_position <= 7:
            raise ValueError("Posición del bit debe estar entre 0 y 7")
            
        current_word = self.read_vw(byte_address)[0]
        if value:
            new_word = current_word | (1 << bit_position)
        else:
            new_word = current_word & ~(1 << bit_position)
        
        self.write_vw(byte_address, new_word)
        
    def read_db(self, db_number, start_address, length=1):
        """Lee datos de un bloque de datos (DB)"""
        command = [
            0x68,                   # Inicio
            0x1B,                   # Longitud
            0x1B,                   # Longitud repetida
            0x68,                   # Inicio repetido
            self.plc_address,       # Dirección del PLC
            0x6C,                   # Comando de lectura
            0x84,                   # Tipo de área (DB)
            db_number,              # Número de DB
            start_address >> 8,     # Dirección High
            start_address & 0xFF,   # Dirección Low
            length                  # Cantidad de words
        ]
        
        command.append(self._calculate_checksum(command))
        command.append(0x16)        # Fin de trama
        
        self.serial.write(bytes(command))
        response = self.serial.read(length * 2 + 10)
        
        self._verify_response(response)
        return struct.unpack(f'>{length}H', response[10:-2])
        
    def close(self):
        """Cierra la conexión serial"""
        self.serial.close()
        





from ConexionBD.conexionSerieAutomata import PLCS7200


plc = PLCS7200()  # Ajusta el puerto según tu configuración

try:
    # Leer una palabra de VW100
    valor = plc.read_vw(100)
    print(f"Valor en VW0: {valor}")
    
    # Escribir el valor 1234 en VW102
    plc.write_vw(102, 1234)
    
    
finally:
    plc.close()    
    