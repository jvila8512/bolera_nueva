import sys
import struct
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import snap7

# Configuración de la conexión
PLC_IP = '192.168.1.188'  # Reemplaza con la IP de tu PLC
RACK = 0
SLOT = 1

# Direcciones de memoria
VD100 = 100  # Dirección de VD100
VD104 = 104  # Dirección de VD104
SIZE = 4     # Tamaño en bytes (un flotante ocupa 4 bytes)

# Crear un cliente Snap7
client = snap7.client.Client()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Monitor de Temperaturas")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Etiquetas para mostrar los valores
        self.label_vd100 = QLabel("VD100: -- °C")
        self.label_vd104 = QLabel("VD104: -- °C")
        layout.addWidget(self.label_vd100)
        layout.addWidget(self.label_vd104)

        # Gráfica en tiempo real
        self.graph = pg.PlotWidget()
        self.graph.setBackground('w')
        self.graph.setTitle("Temperaturas en Tiempo Real", color='b', size='20pt')
        self.graph.setLabel('left', 'Temperatura (°C)')
        self.graph.setLabel('bottom', 'Tiempo (s)')
        self.graph.showGrid(x=True, y=True)
        layout.addWidget(self.graph)

        # Configurar el widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Datos para la gráfica
        self.time_data = []
        self.temp_vd100 = []
        self.temp_vd104 = []
        self.max_points = 50  # Número máximo de puntos en la gráfica

        # Temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualizar cada 1 segundo

        # Conectar al PLC
        try:
            client.connect(PLC_IP, RACK, SLOT)
            print("Conectado al PLC")
        except Exception as e:
            print(f"Error al conectar al PLC: {e}")

    def read_real(self, db_number, start_address):
        """
        Lee un valor real (flotante de 32 bits) desde el PLC.
        """
        data = client.db_read(db_number, start_address, SIZE)
        return struct.unpack('>f', data)[0]  # Interpreta los bytes como un flotante (big-endian)

    def update_data(self):
        """
        Actualiza los valores de temperatura y la gráfica.
        """
        try:
            # Leer valores del PLC
            temp_vd100 = self.read_real(1, VD100)
            temp_vd104 = self.read_real(1, VD104)

            # Actualizar etiquetas
            self.label_vd100.setText(f"VD100: {temp_vd100:.2f} °C")
            self.label_vd104.setText(f"VD104: {temp_vd104:.2f} °C")

            # Agregar datos a la gráfica
            self.time_data.append(time.time())
            self.temp_vd100.append(temp_vd100)
            self.temp_vd104.append(temp_vd104)

            # Limitar el número de puntos en la gráfica
            if len(self.time_data) > self.max_points:
                self.time_data.pop(0)
                self.temp_vd100.pop(0)
                self.temp_vd104.pop(0)

            # Actualizar la gráfica
            self.graph.clear()
            self.graph.plot(self.time_data, self.temp_vd100, pen='r', name='VD100')
            self.graph.plot(self.time_data, self.temp_vd104, pen='b', name='VD104')

        except Exception as e:
            print(f"Error al leer datos del PLC: {e}")

    def closeEvent(self, event):
        """
        Cerrar la conexión con el PLC al cerrar la aplicación.
        """
        client.disconnect()
        print("Desconectado del PLC")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())