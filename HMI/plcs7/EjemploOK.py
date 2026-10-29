import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QCheckBox
)
from PyQt6.QtCore import QTimer
import struct

# Importar la clase PLC_S7_Communicator
from ConexionPLC import PLC_S7_Communicator  # Asegúrate de guardar la clase en un archivo llamado plc_communicator.py

class PLCApp(QMainWindow):
    def __init__(self, plc):
        super().__init__()
        self.plc = plc
        self.setWindowTitle("Comunicación con PLC S7-200")
        self.setGeometry(100, 100, 400, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Sección de Entradas (I)
        self.input_label = QLabel("Entrada I0.0: --")
        layout.addWidget(self.input_label)

        # Sección de Salidas (Q)
        self.output_label = QLabel("Salida Q0.7: --")
        self.output_checkbox = QCheckBox("Activar Salida Q0.7")
        self.output_checkbox.stateChanged.connect(self.toggle_output)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_checkbox)

        # Sección de Variables de Datos (VD)
        self.vd_label = QLabel("VD100: --")
        self.vd_edit = QLineEdit()
        self.vd_button = QPushButton("Escribir en VD100")
        self.vd_button.clicked.connect(self.write_vd)
        layout.addWidget(self.vd_label)
        layout.addWidget(self.vd_edit)
        layout.addWidget(self.vd_button)

        # Sección de Marcadores (M)
        self.marker_label = QLabel("Marcador M0.0: --")
        self.marker_checkbox = QCheckBox("Activar Marcador M1.0")
        self.marker_checkbox.stateChanged.connect(self.toggle_marker)
        layout.addWidget(self.marker_label)
        layout.addWidget(self.marker_checkbox)

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
            # Leer entrada (I0.0)
            input_bit= self.plc.read_input_bit(0, 3)  # Lee 1 byte de la entrada I0.0
            
            self.input_label.setText(f"Entrada I0.3: {input_bit}")

            # Leer salida (Q0.0)
            output_bit = self.plc.read_output_bit(0, 7)  # Lee 1 byte de la salida Q0.0
            
           
            self.output_label.setText(f"Salida Q0.7: {output_bit}")

            # Leer VD100
            vd_data = self.plc.read_vd(1, 100, 4)  # Lee 4 bytes de VD100
            vd_value = struct.unpack('>f', vd_data)[0]  # Convierte a flotante
            self.vd_label.setText(f"VD100: {vd_value:.2f}")

            # Leer marcador (M0.0)
            marker_bit = self.plc.read_marker_bit(1, 0)  # Lee 1 byte del marcador M0.0
           
            self.marker_label.setText(f"Marcador M1.0: {marker_bit}")
        except Exception as e:
            print(f"Error al leer datos: {e}")

    def toggle_output(self):
        """Activa o desactiva la salida Q0.0."""
        try:
            # Leer el estado actual de las salidas (Q)
            output_data = self.plc.read_output_bit(0, 1)  # Lee 1 byte de la salida Q0.0

            # Cambiar el bit 0 (Q0.0) según el estado del checkbox
            if self.output_checkbox.isChecked():
               self.plc.write_output_bit(0, 1,1)
            else:
              self.plc.write_output_bit(0, 1,0)

            # Escribir el nuevo valor en las salidas (Q)
           # self.plc.write_output_bit(0, output_data)
        except Exception as e:
            print(f"Error al escribir en Q0.0: {e}")

    def write_vd(self):
        """Escribe en VD100."""
        try:
            value = float(self.vd_edit.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 100, data)
        except Exception as e:
            print(f"Error al escribir en VD100: {e}")

    def toggle_marker(self):
        """Activa o desactiva el marcador M0.0."""
        try:
            # Leer el estado actual de los marcadores (M)
            marker_data = self.plc.read_marker_bit(1, 0)  # Lee 1 byte del marcador M1.0

            # Cambiar el bit 0 (M0.0) según el estado del checkbox
            if self.marker_checkbox.isChecked():
                 self.plc.write_marker(1, 0,1)  # Escribe 1
            else:
               self.plc.write_marker(1, 0,0)  # Escribe 0

            # Escribir el nuevo valor en los marcadores (M)
          
           # self.plc.write_marker(1, 0,bytearray([0x01]))  # Escribe 0x01 en M0.0
        except Exception as e:
            print(f"Error al escribir en M0.0: {e}")

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