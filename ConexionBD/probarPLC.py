
    
import time

from ConexionBD.OtraSerie import SiemensS7PPI

def test_s7_200_ppi():
    # Parámetros de la conexión
    port = 'COM2'  # Reemplaza con el puerto correcto de tu PC (en Linux sería algo como '/dev/ttyS0')
    plc_address = 2 # Dirección del PLC (0-31)
    baudrate = 9600  # Baudrate
    timeout = 1  # Timeout de comunicación en segundos
    
    # Crear una instancia de la clase SiemensS7PPI
    plc = SiemensS7PPI(port, baudrate, timeout, plc_address)

    try:
        # --- Prueba de lectura ---
        print("Leyendo datos de DB1, Dirección 0, Longitud 1 palabra (2 bytes)...")
        response = plc.read_memory(db_number=1, start_address=0, length=1, is_bit=False)
        if response is not None:
            print(f"Datos leídos: {response}")
        else:
            print("Error al leer los datos")

        # --- Prueba de escritura ---
        print("\nEscribiendo en DB1, Dirección 0, Valor 1234 (en palabra)...")
        plc.write_memory(db_number=1, start_address=0, values=[1234], is_bit=False)

        # Verificar si los datos fueron escritos correctamente
        print("\nLeyendo nuevamente para verificar la escritura...")
        response = plc.read_memory(db_number=1, start_address=0, length=1, is_bit=False)
        if response is not None:
            print(f"Datos leídos (verificación): {response}")
        else:
            print("Error al leer los datos para verificar la escritura")
        
    except Exception as e:
        print(f"Error en la prueba: {e}")
    finally:
        # Cerrar la conexión al final
        plc.close()

# Ejecutar la prueba
if __name__ == "__main__":
    test_s7_200_ppi()