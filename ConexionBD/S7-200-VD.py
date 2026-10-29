import snap7
import struct
import time

# Configuración de la conexión
PLC_IP = '192.168.1.188'  # Reemplaza con la IP de tu PLC
RACK = 0
SLOT = 1

# Direcciones de memoria
VD100 = 100  # Dirección de VD100
VD104 = 104  # Dirección de VD104
VD128 = 120 # Dirección de VD104
SIZE = 4     # Tamaño en bytes (un flotante ocupa 4 bytes)

# Crear un cliente Snap7
client = snap7.client.Client()

def read_real(db_number, start_address):
    """
    Lee un valor real (flotante de 32 bits) desde el PLC.
    """
    data = client.db_read(db_number, start_address, SIZE)
    return struct.unpack('>f', data)[0]  # Interpreta los bytes como un flotante (big-endian)

def write_real(db_number, start_address, value):
    """
    Escribe un valor real (flotante de 32 bits) en el PLC.
    """
    data = struct.pack('>f', value)  # Convierte el flotante a bytes (big-endian)
    client.db_write(db_number, start_address, data)

def main():
    try:
        # Conectar al PLC
        client.connect(PLC_IP, RACK, SLOT)
        print("Conectado al PLC")

        # Bucle de monitoreo y automatización
        while True:
            try:
                # Leer VD100 y VD104
                valor_vd100 = read_real(1, VD100)  # DB1, dirección VD100
                valor_vd104 = read_real(1, VD104)  # DB1, dirección VD104
                print(f"Valor de VD100: {valor_vd100}")
                print(f"Valor de VD104: {valor_vd104}")

                # Escribir un valor en VD100 (ejemplo: incrementar en 1.0)
                nuevo_valor = valor_vd100 + 1.0
                write_real(1, VD128, nuevo_valor)
                print(f"Escrito {nuevo_valor} en VD128")

            except snap7.exceptions.Snap7Exception as e:
                print(f"Error de Snap7 durante la operación: {e}")
            except Exception as e:
                print(f"Error inesperado durante la operación: {e}")

            # Esperar 2 segundos antes de la siguiente iteración
            time.sleep(2)

    except snap7.exceptions.Snap7Exception as e:
        print(f"Error de Snap7 al conectar: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # Desconectar del PLC
        client.disconnect()
        print("Desconectado del PLC")

if __name__ == "__main__":
    main()