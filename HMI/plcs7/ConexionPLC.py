import snap7
from snap7.type import Areas

import struct
import time

class PLC_S7_Communicator:
    def __init__(self, ip, rack=0, slot=1):
        """
        Inicializa la conexión con el PLC.
        :param ip: Dirección IP del PLC.
        :param rack: Número de rack (por defecto 0).
        :param slot: Número de slot (por defecto 1).
        """
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        

    def connect(self):
        """
        Conecta el cliente al PLC con manejo de errores.
        :return: True si la conexión fue exitosa, False en caso contrario.
        """
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            if self.client.get_connected():
                print(f"Conexión exitosa al PLC en {self.ip}")
                return True
            else:
                print(f"No se pudo conectar al PLC en {self.ip}")
                return False
        
        except Exception as e:
            print(f"Error inesperado al conectar al PLC: {e}")
            return False

    def disconnect(self):
        """
        Desconecta el cliente del PLC con manejo de errores.
        :return: True si la desconexión fue exitosa, False en caso contrario.
        """
        try:
            if self.client.get_connected():
                self.client.disconnect()
                print(f"Desconexión exitosa del PLC en {self.ip}")
                return True
            else:
                print(f"No había una conexión activa con el PLC en {self.ip}")
                return False
      
        except Exception as e:
            print(f"Error inesperado al desconectar del PLC: {e}")
            return False

    def is_connected(self):
        """
        Verifica si el cliente está conectado al PLC.
        :return: True si está conectado, False en caso contrario.
        """
        return self.client.get_connected()

    def read_vd(self, db_number, start_address, size):
        """
        Lee un bloque de datos (VD) desde el PLC.
        :param db_number: Número del bloque de datos.
        :param start_address: Dirección inicial.
        :param size: Tamaño en bytes.
        :return: bytearray con los datos leídos.
        """
        return self.client.db_read(db_number, start_address, size)

    def write_vd(self, db_number, start_address, data):
        """
        Escribe un bloque de datos (VD) en el PLC.
        :param db_number: Número del bloque de datos.
        :param start_address: Dirección inicial.
        :param data: bytearray con los datos a escribir.
        """
        self.client.db_write(db_number, start_address, data)

    def read_marker_bit(self, byte_address, bit_position):
        """
        Lee un bit específico de un marcador (M) del PLC.
        :param byte_address: Dirección del byte (por ejemplo, 1 para MB1).
        :param bit_position: Posición del bit (0-7, por ejemplo, 2 para M1.2).
        :return: Valor del bit (0 o 1).
        """
        try:
            # Leer el byte que contiene el bit deseado
            marker_data = self.client.read_area(snap7.type.Areas.MK, 0, byte_address, 1)

            # Extraer el bit específico
            bit_value = (marker_data[0] >> bit_position) & 0x01
            print(f"Valor de M{byte_address}.{bit_position}: {bit_value}")
            return bit_value
        except Exception as e:
            print(f"Error al leer el marcador: {e}")
            return None

    def write_marker(self, start_address, bit_position, value):
        """
        Escribe un bit específico en un marcador (M) del PLC.
        :param start_address: Dirección inicial del byte (por ejemplo, 0 para M0.x).
        :param bit_position: Posición del bit (0-7, por ejemplo, 2 para M0.2).
        :param value: Valor a escribir (0 o 1).
        """
        try:
            # Leer el byte actual del marcador
            marker_data = self.client.read_area(snap7.type.Areas.MK, 0, start_address, 1)

            # Modificar el bit específico
            if value == 1:
                marker_data[0] |= (1 << bit_position)  # Activar el bit
            else:
                marker_data[0] &= ~(1 << bit_position)  # Desactivar el bit

            # Escribir el byte modificado en el marcador
            self.client.write_area(snap7.type.Areas.MK, 0, start_address, marker_data)
            print(f"Marcador M{start_address}.{bit_position} actualizado: {marker_data.hex()}")
        except Exception as e:
            print(f"Error al escribir en el marcador: {e}")

    def read_input_bit(self, byte_address, bit_position):
        """
        Lee un bit específico de una entrada (I) del PLC.
        :param byte_address: Dirección del byte (por ejemplo, 0 para IB0).
        :param bit_position: Posición del bit (0-7, por ejemplo, 2 para I0.2).
        :return: Valor del bit (0 o 1).
        """
        try:
            # Leer el byte que contiene el bit deseado
            input_data = self.client.read_area(snap7.type.Areas.PE, 0, byte_address, 1)

            # Extraer el bit específico
            bit_value = (input_data[0] >> bit_position) & 0x01
            print(f"Valor de I{byte_address}.{bit_position}: {bit_value}")
            return bit_value
        except Exception as e:
            print(f"Error al leer la entrada: {e}")
            return None

    def read_output_bit(self, byte_address, bit_position):
        """
        Lee un bit específico de una salida (Q) del PLC.
        :param byte_address: Dirección del byte (por ejemplo, 0 para QB0).
        :param bit_position: Posición del bit (0-7, por ejemplo, 1 para Q0.1).
        :return: Valor del bit (0 o 1).
        """
        try:
            # Leer el byte que contiene el bit deseado
            output_data = self.client.read_area(snap7.type.Areas.PA, 0, byte_address, 1)

            # Extraer el bit específico
            bit_value = (output_data[0] >> bit_position) & 0x01
            print(f"Valor de Q{byte_address}.{bit_position}: {bit_value}")
            return bit_value
        except Exception as e:
            print(f"Error al leer la salida: {e}")
            return None


    def write_output_bit(self, byte_address, bit_position, value):
        """Escribe un bit en una salida (Q) del PLC."""
        try:
            # Leer el byte actual de las salidas
            output_data = self.client.read_area(Areas.PA, 0, byte_address, 1)

            # Modificar el bit específico
            if value == 1:
                output_data[0] |= (1 << bit_position)  # Activar el bit
            else:
                output_data[0] &= ~(1 << bit_position)  # Desactivar el bit

            # Escribir el byte modificado en las salidas
            self.client.write_area(Areas.PA, 0, byte_address, output_data)
            print(f"Salida Q{byte_address}.{bit_position} actualizada: {value}")
        except Exception as e:
            print(f"Error al escribir en la salida: {e}")
        
    def write_variable_float(self, start_address, value):
        """Escribe un valor flotante en una variable de datos (V)."""
        try:
            data = struct.pack('>f', value)
            self.client.write_area(Areas.DB, 1, start_address, data)
            print(f"Valor {value} escrito en VD{start_address}")
        except Exception as e:
            print(f"Error al escribir en VD{start_address}: {e}")
    def read_variable_float(self, start_address):
        """
        Lee un valor flotante de una variable de datos (V) del PLC.
        :param start_address: Dirección inicial (por ejemplo, 100 para VD100).
        :return: Valor flotante leído.
        """
        try:
            # Leer 4 bytes desde la dirección especificada
            data = self.client.read_area(snap7.type.Areas.DB, 1, start_address, 4)

            # Convertir los bytes a un valor flotante
            value = struct.unpack('>f', data)[0]
            print(f"Valor leído de VD{start_address}: {value}")
            return value
        except Exception as e:
            print(f"Error al leer de VD{start_address}: {e}")
            return None 
    
    
    def write_db(self, db_number, start_address, data):
        """Escribe datos en un bloque de datos (DB)."""
        try:
            self.client.db_write(db_number, start_address, data)
            print(f"Datos escritos en DB{db_number} desde la dirección {start_address}")
        except Exception as e:
            print(f"Error al escribir en DB{db_number}: {e}")    
  
    def save_to_eeprom(self, v_address):
        """
        Guarda un valor de la memoria V en la EEPROM.
        :param v_address: Dirección de la variable V (por ejemplo, 120 para VD120).
        """
        try:
            # Verificar que la dirección esté dentro del rango permitido
            if v_address < 0 or v_address > 8191:  # Ajusta este valor según tu modelo de PLC
                raise ValueError(f"Dirección {v_address} fuera de rango")

            # Configurar SMW32 con la dirección de la variable V
            smw32_data = struct.pack('>H', v_address)  # '>H' indica un entero de 16 bits (big-endian)
            self.client.write_area(snap7.type.Areas.PE, 0, 32, smw32_data)  # SMW32 está en PE, dirección 32

            # Configurar SMB31 para iniciar la escritura en la EEPROM
            smb31_data = bytearray([0x02])  # Comando para escribir un valor de 32 bits (VD)
            self.client.write_area(snap7.type.Areas.PE, 0, 31, smb31_data)  # SMB31 está en PE, dirección 31

            # Esperar a que la escritura en la EEPROM se complete
            while True:
                smb31_data = self.client.read_area(snap7.type.Areas.PE, 0, 31, 1)
                if smb31_data[0] & 0x80:  # Verificar el bit 7 de SMB31
                    print(f"Valor en VD{v_address} guardado en la EEPROM")
                    break
                time.sleep(0.1)  # Esperar 100 ms antes de verificar nuevamente
        except Exception as e:
            print(f"Error al guardar en la EEPROM: {e}")
    def save_to_eeprom1(self, v_address):
        """
        Guarda un valor de la memoria V en la EEPROM.
        :param v_address: Dirección de la variable V (por ejemplo, 120 para VD120).
        """
        try:
            # Verificar que la dirección esté dentro del rango permitido
            if v_address < 0 or v_address > 8191:  # Ajusta este valor según tu modelo de PLC
                raise ValueError(f"Dirección {v_address} fuera de rango")

            # Configurar SMW32 con la dirección de la variable V
            smw32_data = struct.pack('>H', v_address)  # '>H' indica un entero de 16 bits (big-endian)
            self.client.write_area(snap7.type.Areas.PE, 0, 32, smw32_data)  # SMW32 está en PE, dirección 32

            # Configurar SMB31 para iniciar la escritura en la EEPROM
            smb31_data = bytearray([0x02])  # Comando para escribir un valor de 32 bits (VD)
            self.client.write_area(snap7.type.Areas.PE, 0, 31, smb31_data)  # SMB31 está en PE, dirección 31

            # Esperar a que la escritura en la EEPROM se complete
            while True:
                smb31_data = self.client.read_area(snap7.type.Areas.PE, 0, 31, 1)
                if smb31_data[0] & 0x80:  # Verificar el bit 7 de SMB31
                    print(f"Valor en VD{v_address} guardado en la EEPROM")
                    break
                time.sleep(0.1)  # Esperar 100 ms antes de verificar nuevamente
        except Exception as e:
            print(f"Error al guardar en la EEPROM: {e}")
    def write_variable_word(self, start_address, value):
        """
        Escribe un valor WORD (16 bits) en una variable VW del PLC.
        :param start_address: Dirección VW (ej: 10 para VW10).
        :param value: Valor entero a escribir (rango: -32768 a 32767).
        """
        try:
            # Empaquetar el valor como un entero de 16 bits (big-endian)
            data = struct.pack('>h', value)
            self.client.write_area(Areas.DB, 1, start_address, data)
            print(f"Valor {value} escrito en VW{start_address}")
        except Exception as e:
            print(f"Error al escribir en VW{start_address}: {e}")

    def read_variable_word(self, start_address):
        """
        Lee un valor WORD (16 bits) de una variable VW del PLC.
        :param start_address: Dirección VW (ej: 10 para VW10).
        :return: Valor entero leído o None si hay error.
        """
        try:
            # Leer 2 bytes (VW = 16 bits)
            data = self.client.read_area(Areas.DB, 1, start_address, 2)
            # Desempaquetar como entero de 16 bits con signo (big-endian)
            value = struct.unpack('>h', data)[0]
            print(f"Valor leído de VW{start_address}: {value}")
            return value
        except Exception as e:
            print(f"Error al leer VW{start_address}: {e}")
            return None
   
    # Escribir en M0.0
  #  plc.write_marker_bit(0, 0, 1)

# Escribir en VD100
# plc.write_variable_float(100, 3.14)

# Escribir en DB1
# data = bytearray([0x01, 0x02, 0x03, 0x04])
# plc.write_db(1, 0, data)        

# Leer el valor de M1.2
#bit_value = plc.read_marker_bit(1, 2)

#if bit_value is not None:
    #print(f"El valor de M1.2 es: {bit_value}")
#else:
   # print("No se pudo leer el valor de M1.2")
   
   

# Leer el setpoint, máximo y mínimo
#setpoint = plc.read_variable_float(100)
#max_temp = plc.read_variable_float(104)
#min_temp = plc.read_variable_float(108)

#print(f"Setpoint: {setpoint}, Máximo: {max_temp}, Mínimo: {min_temp}")
