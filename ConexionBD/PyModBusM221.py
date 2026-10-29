
import sqlite3
import time
import datetime
from pymodbus.client import ModbusTcpClient

def leer_bits_palabra(client, address):
    """Lee una palabra de memoria y retorna los bits individuales."""
    try:
        result = client.read_holding_registers(address, 1, unit=1)
        if result.isError():
            print(f"Error al leer la palabra de memoria: {result}")
            return None
        word = result.registers[0]
        bits = [(word >> i) & 1 for i in range(15, -1, -1)]
        return bits
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def leer_db(client, db_number, start_address, num_words):
    """Lee datos de un Data Block."""
    try:
        #La direccion en Modbus de un DB depende del PLC, necesita ser mapeada correctamente.
        #Este ejemplo asume una mapeo directo, pero puede ser diferente en tu caso.

        modbus_address = db_number * 1000 + start_address  #Ejemplo de mapeo,  **Ajusta esto según la documentación de tu PLC**

        result = client.read_holding_registers(modbus_address, num_words, unit=1)
        if result.isError():
            print(f"Error al leer el DB: {result}")
            return None
        return result.registers
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def escribir_palabra(client, address, value):
    """Escribe un valor en una palabra de memoria."""
    try:
        result = client.write_register(address, value, unit=1)
        if result.isError():
            print(f"Error al escribir en la palabra de memoria: {result}")
            return False
        return True
    except Exception as e:
        print(f"Error inesperado al escribir: {e}")
        return False




def escribir_db(client, db_number, start_address, values):
    """Escribe datos en un Data Block."""
    try:
        #Igual que antes, la direccion Modbus del DB debe ser mapeada correctamente.
        modbus_address = db_number * 1000 + start_address  #Ejemplo de mapeo, **Ajusta esto según la documentación de tu PLC**

        result = client.write_registers(modbus_address, values, unit=1)
        if result.isError():
            print(f"Error al escribir en el DB: {result}")
            return False
        return True
    except Exception as e:
        print(f"Error inesperado al escribir en el DB: {e}")

    return False



def leer_bit(client, address, bit_number):
    """Lee un bit específico de una palabra de memoria."""
    try:
        result = client.read_coils(address, 1, unit=1) #Usamos read_coils para bits
        if result.isError():
            print(f"Error al leer el bit: {result}")
            return None
        return result.bits[0]
    except Exception as e:
        print(f"Error inesperado al leer bit: {e}")
        return None


def escribir_bit(client, address, bit_number, value):
    """Escribe un bit específico en una palabra de memoria."""
    try:
        result = client.write_coil(address, value, unit=1) #Usamos write_coil para bits
        if result.isError():
            print(f"Error al escribir el bit: {result}")
            return False
        return True
    except Exception as e:
        print(f"Error inesperado al escribir bit: {e}")
        return False
def crear_tabla_sqlite(conn):
    """Crea la tabla en la base de datos SQLite si no existe."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos_plc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            direccion INTEGER,
            valor TEXT, #Modificado para aceptar listas
            tipo TEXT,
            variable_tipo
        )
    ''')
    conn.commit()    
def guardar_datos_sqlite(conn, timestamp, direccion, valor, tipo, variable_tipo):
    """Guarda los datos en la base de datos SQLite, con tipo de variable"""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO datos_plc (timestamp, direccion, valor, tipo, variable_tipo) VALUES (?, ?, ?, ?, ?)",
                   (timestamp, direccion, str(valor), tipo, variable_tipo))
    conn.commit()
    
import time
import datetime

if __name__ == "__main__":
    ip_address = "192.168.1.188"  # Reemplaza con la IP de tu PLC
    port = 502
    db_file = "datos_plc.db"

    try:
        client = ModbusTcpClient(ip_address, port)
        client.connect()
        conn = sqlite3.connect(db_file)
        crear_tabla_sqlite(conn) #Agrega la columna variable_tipo a tu tabla

        while True:
            timestamp = datetime.datetime.now().isoformat()

            #Lecturas
            bits_mw0 = leer_bits_palabra(client, 0)
            if bits_mw0:
                guardar_datos_sqlite(conn, timestamp, 0, bits_mw0, "MW", "word")
            bit_mw1_bit0 = leer_bit(client,1,0) # Lee el bit 0 de la palabra MW1
            if bit_mw1_bit0 is not None:
                guardar_datos_sqlite(conn, timestamp, 1, bit_mw1_bit0, "MW", "bit")

            db_data = leer_db(client, 1, 0, 5)
            if db_data:
                for i, val in enumerate(db_data):
                    guardar_datos_sqlite(conn, timestamp, 1000 + i, val, "DB1", "word")

            #Escrituras (ejemplos)
            escribir_palabra(client, 10, 2500)  
            escribir_bit(client, 20, 0, True) #Escribe True en el bit 0 de la palabra MW20


            time.sleep(1)  # Espera 1 segundo

    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        if client.is_socket_open():
            client.close()
        if conn:
            conn.close()    