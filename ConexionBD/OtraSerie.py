import serial
import struct
import time

class SiemensS7PPI:
    def __init__(self, port, baudrate=9600, timeout=1, address=1):
        """
        Inicializa la conexión serial para comunicarse con el PLC S7-200 utilizando PPI.
        
        :param port: El puerto serie (por ejemplo, 'COM1' en Windows o '/dev/ttyS0' en Linux).
        :param baudrate: La velocidad de comunicación (por defecto 9600 baudios).
        :param timeout: Tiempo de espera para las respuestas (en segundos).
        :param address: Dirección del PLC (0-31).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.address = address

        # Configurar la conexión serial
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.ser.flush()

    def _send_receive(self, data):
        """
        Envía datos al PLC y espera una respuesta. Verifica el error de comunicación.
        
        :param data: Datos a enviar al PLC.
        :return: Respuesta del PLC.
        """
        try:
            # Enviar la trama
            self.ser.write(data)
            time.sleep(0.1)  # Esperar un poco para que el PLC responda

            # Leer la respuesta
            response = self.ser.read(1024)  # Leemos hasta 1024 bytes
            if len(response) == 0:
                raise Exception("Timeout: No se recibió respuesta del PLC")
            
            return response
        
        except Exception as e:
            print(f"Error en la comunicación: {e}")
            return None

    def read_memory(self, db_number, start_address, length, is_bit=False):
        """
        Lee datos del PLC en el bloque de datos (DB) o en direcciones VW.
        
        :param db_number: Número del bloque de datos (DB).
        :param start_address: Dirección de inicio (en bytes o en bits dependiendo de la operación).
        :param length: Longitud de los datos a leer (en palabras o en bits).
        :param is_bit: Si es True, se lee a nivel de bits. Si es False, se lee a nivel de palabras.
        :return: Los datos leídos.
        """
        # Construir la trama PPI de lectura
        data = self._build_read_request(db_number, start_address, length, is_bit)
        response = self._send_receive(data)
        
        if response:
            # Verificar errores en la respuesta
            if response[0] == 0x00:  # Respuesta de éxito (sin error)
                return self._parse_response(response, is_bit)
            else:
                print(f"Error al leer la memoria: {response[0]}")
                return None
        else:
            return None

    def write_memory(self, db_number, start_address, values, is_bit=False):
        """
        Escribe datos en el PLC en el bloque de datos (DB) o en direcciones VW.
        
        :param db_number: Número del bloque de datos (DB).
        :param start_address: Dirección de inicio.
        :param values: Valores a escribir.
        :param is_bit: Si es True, se escribe a nivel de bits. Si es False, se escribe a nivel de palabras.
        """
        # Construir la trama PPI de escritura
        data = self._build_write_request(db_number, start_address, values, is_bit)
        response = self._send_receive(data)
        
        if response:
            # Verificar errores en la respuesta
            if response[0] == 0x00:  # Respuesta de éxito (sin error)
                print("Escritura exitosa")
            else:
                print(f"Error al escribir en la memoria: {response[0]}")
        else:
            print("Error en la comunicación durante la escritura")

    def _build_read_request(self, db_number, start_address, length, is_bit=False):
        """
        Construye la trama PPI para leer datos del PLC.
        
        :param db_number: Número del bloque de datos.
        :param start_address: Dirección de inicio.
        :param length: Longitud de la lectura (en palabras o en bits).
        :param is_bit: Si es True, se lee a nivel de bits. Si es False, se lee a nivel de palabras.
        :return: La trama de solicitud PPI para lectura.
        """
        # Encabezado del protocolo PPI (simplificado para la explicación)
        header = struct.pack("B", self.address)  # Dirección del PLC (1 byte)
        
        # Trama de lectura (simplificada)
        command = b'\x03'  # Código de comando para lectura (ejemplo)

        # Dirección de inicio (DB o VW), longitud, etc.
        if is_bit:
            address = struct.pack("B", start_address)  # Dirección en bits
        else:
            address = struct.pack(">H", start_address)  # Dirección en palabras
        
        length_bytes = struct.pack(">H", length)  # Longitud en palabras (2 bytes)

        # Concatenamos todos los componentes
        return header + command + address + length_bytes

    def _build_write_request(self, db_number, start_address, values, is_bit=False):
        """
        Construye la trama PPI para escribir datos al PLC.
        
        :param db_number: Número del bloque de datos.
        :param start_address: Dirección de inicio.
        :param values: Valores a escribir (lista de bytes o palabras).
        :param is_bit: Si es True, se escribe a nivel de bits. Si es False, se escribe a nivel de palabras.
        :return: La trama de solicitud PPI para escritura.
        """
        header = struct.pack("B", self.address)  # Dirección del PLC (1 byte)
        
        # Trama de escritura (simplificada)
        command = b'\x10'  # Código de comando para escritura
        
        # Dirección de inicio (DB o VW)
        if is_bit:
            address = struct.pack("B", start_address)  # Dirección en bits
        else:
            address = struct.pack(">H", start_address)  # Dirección en palabras
        
        # Escribir valores (simulación con un solo valor de ejemplo)
        # Si estamos escribiendo en "palabras" (16 bits), empaquetamos como 2 bytes
        if not is_bit:
            # Empaquetar como palabra (16 bits) - ejemplo con valor de 1234 (2 bytes)
            value_bytes = struct.pack(">H", values[0])  # 2 bytes para palabra de 16 bits
        else:
            # Si se trata de un bit, empaquetar como un solo byte (aunque no es común en este caso)
            value_bytes = struct.pack("B", values[0])  # 1 byte para bit (ejemplo de solo 1 bit)
        
        # Concatenamos todos los componentes
        return header + command + address + value_bytes

    def _parse_response(self, response, is_bit=False):
        """
        Parsea la respuesta del PLC.
        
        :param response: Respuesta recibida del PLC.
        :param is_bit: Si es True, parsea los datos a nivel de bits. Si es False, a nivel de palabras.
        :return: Los datos extraídos de la respuesta.
        """
        # Simplificación: En este ejemplo, solo consideramos las respuestas de longitud fija
        if is_bit:
            return response[1:]  # Bits leídos (simplificación)
        else:
            return struct.unpack(">H", response[1:3])[0]  # Palabra leída

    def close(self):
        """Cierra la conexión serial."""
        self.ser.close()
