import serial

class PLCSerialCommunication:
    def __init__(self, serial_port, baudrate=9600):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.serial_connection = None

        self.connect()

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.serial_port, self.baudrate, timeout=1)
            print(f"Conexión serie establecida en {self.serial_port} a {self.baudrate} baudios.")
        except Exception as e:
            print(f"Error al conectar: {e}")

    def disconnect(self):
        if self.serial_connection:
            self.serial_connection.close()
            print("Conexión serie cerrada.")

    def send_data(self, data):
        if self.serial_connection:
            self.serial_connection.write(data)
            print(f"Datos enviados: {data}")

    def receive_data(self, size):
        if self.serial_connection:
            data = self.serial_connection.read(size)
            print(f"Datos recibidos: {data}")
            return data

    def write_vw(self, start, data):
        # Formato del comando para escribir en VW
        command = f'VW{start}:{data.hex()}\n'  # Ejemplo de comando
        self.send_data(command.encode())

    def read_vw(self, start, size):
        # Formato del comando para leer de VW
        command = f'RVW{start}:{size}\n'  # Ejemplo de comando
        self.send_data(command.encode())
        return self.receive_data(size)

# Ejemplo de uso
if __name__ == "__main__":
    plc = PLCSerialCommunication('COM2')  # Cambia 'COM3' según tu configuración

    # Escribir en VW
    plc.write_vw(0, b'\x01\x02\x03\x04')  # Escribe 4 bytes en VW0

    # Leer de VW
    vw_data = plc.read_vw(0, 4)  # Lee 4 bytes de VW0
    print(f"Datos leídos de VW0: {vw_data}")

    plc.disconnect()