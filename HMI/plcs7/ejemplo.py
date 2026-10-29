import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
)
from PyQt6.QtCore import QTimer
import struct
import snap7

# Importar la clase PLC_S7_Communicator
from ConexionPLC import PLC_S7_Communicator  # Asegúrate de guardar la clase en un archivo llamado plc_communicator.py

class PLCApp(QMainWindow):
    def __init__(self, plc):
        super().__init__()
        self.plc = plc
        self.setWindowTitle("Comunicación con PLC S7-200")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Entradas (I)
        self.input_label = QLabel("Entrada (I): --")
        self.input_edit = QLineEdit()
        self.input_button = QPushButton("Escribir en Entrada")
        self.input_button.clicked.connect(self.write_input)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_edit)
        layout.addWidget(self.input_button)

        # Salidas (Q)
        self.output_label = QLabel("Salida (Q): --")
        layout.addWidget(self.output_label)

        # Variables de datos (VD)
        self.vd_label = QLabel("VD100: --")
        self.vd_edit = QLineEdit()
        self.vd_button = QPushButton("Escribir en VD100")
        self.vd_button.clicked.connect(self.write_vd)
        layout.addWidget(self.vd_label)
        layout.addWidget(self.vd_edit)
        layout.addWidget(self.vd_button)

        # Marcadores (M)
        self.marker_label = QLabel("M0: --")
        self.marker_edit = QLineEdit()
        self.marker_button = QPushButton("Escribir en M0")
        self.marker_button.clicked.connect(self.write_marker)
        layout.addWidget(self.marker_label)
        layout.addWidget(self.marker_edit)
        layout.addWidget(self.marker_button)

        # Configurar el widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualizar cada 1 segundo

    def update_data(self):
        """Actualiza los datos en la interfaz."""
        try:
            # Leer entrada (I)
            input_data = self.plc.read_input(0, 3)  # Lee 1 byte de la entrada I0.0
            self.input_label.setText(f"Entrada (I): {input_data.hex()}")

            # Leer salida (Q)
            output_data = self.plc.read_output(0, 1)  # Lee 1 byte de la salida Q0.0
            self.output_label.setText(f"Salida (Q): {output_data.hex()}")

            # Leer VD100
            vd_data = self.plc.read_vd(1, 100, 4)  # Lee 4 bytes de VD100
            self.vd_label.setText(f"VD100: {struct.unpack('>f', vd_data)[0]:.2f}")

            # Leer M0
            marker_data = self.plc.read_marker(0, 1)  # Lee 1 byte del marcador M0
            self.marker_label.setText(f"M0: {marker_data.hex()}")
        except Exception as e:
            print(f"Error al leer datos: {e}")

    def write_input(self):
        """Escribe en la entrada (I)."""
        try:
            data = int(self.input_edit.text(), 16).to_bytes(1, 'big')
            self.plc.write_output(0, data)  # Escribe en la salida Q0.0 (simulación)
        except Exception as e:
            print(f"Error al escribir en la entrada: {e}")

    def write_vd(self):
        """Escribe en VD100."""
        try:
            value = float(self.vd_edit.text())
            data = struct.pack('>f', value)
            self.plc.write_vd(1, 100, data)
        except Exception as e:
            print(f"Error al escribir en VD100: {e}")

    def write_marker(self):
        """Escribe en el marcador M0."""
        try:
            data = int(self.marker_edit.text(), 16).to_bytes(1, 'big')
            self.plc.write_marker(0, data)
        except Exception as e:
            print(f"Error al escribir en M0: {e}")

    def closeEvent(self, event):
        """Desconecta el PLC al cerrar la aplicación."""
        self.plc.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear una instancia de PLC_S7_Communicator
    plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC

    # Crear y mostrar la ventana principal
    window = PLCApp(plc)
    window.show()

    sys.exit(app.exec())