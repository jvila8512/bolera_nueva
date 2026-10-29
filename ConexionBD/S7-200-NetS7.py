import snap7
import struct

# Configuración de la conexión
PLC_IP = '192.168.1.188'  # Reemplaza con la IP de tu PLC
RACK = 0
SLOT = 1

# Crear un cliente Snap7
client = snap7.client.Client()

# Conectar al PLC
client.connect(PLC_IP, RACK, SLOT)

# Verificar si la conexión fue exitosa
if client.get_connected():
    print("Conectado al PLC")
else:
    print("No se pudo conectar al PLC")
    exit(1)

# Leer un área de memoria (por ejemplo, DB1, 10 bytes)
db_number = 1
start_address = 0
size = 10
data = client.db_read(db_number, start_address, size)

print("Datos leídos:", data)


# Supongamos que los primeros 2 bytes son un entero (16 bits)
valor_entero = struct.unpack('>h', data[:2])[0]  # '>h' indica un entero de 16 bits (big-endian)
print("Valor entero leído:", valor_entero)

# Si los datos son flotantes (32 bits)
valor_flotante = struct.unpack('>f', data[:4])[0]  # '>f' indica un flotante de 32 bits (big-endian)
print("Valor flotante leído:", valor_flotante)

# Escribir en un área de memoria (por ejemplo, DB1, 10 bytes)
new_data = bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A])
client.db_write(db_number, start_address, new_data)

print("Datos escritos en el PLC")

# Desconectar del PLC
client.disconnect()
print("Desconectado del PLC")