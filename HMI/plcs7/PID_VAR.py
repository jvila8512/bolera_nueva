import sys
import struct
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt6.QtCore import QTimer

# Importar la clase PLC_S7_Communicator
from ConexionPLC import PLC_S7_Communicator  # Asegúrate de guardar la clase en un archivo llamado plc_communicator.py


class PIDApp(QMainWindow):
    def __init__(self, plc):
        super().__init__()
        self.plc = plc
        self.setWindowTitle("Monitor de PID")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Etiquetas para mostrar los valores del PID
        self.pv_label = QLabel("PV: --")
        self.sp_label = QLabel("SP: --")
        self.output_label = QLabel("Output: --")
        self.gain_label = QLabel("Gain: --")
        self.sample_time_label = QLabel("SampleTime: --")
        self.i_time_label = QLabel("I_Time: --")
        self.d_time_label = QLabel("D_Time: --")

        # Botón para actualizar los valores
        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.update_values)

        # Agregar widgets al layout
        layout.addWidget(self.pv_label)
        layout.addWidget(self.sp_label)
        layout.addWidget(self.output_label)
        layout.addWidget(self.gain_label)
        layout.addWidget(self.sample_time_label)
        layout.addWidget(self.i_time_label)
        layout.addWidget(self.d_time_label)
        layout.addWidget(self.update_button)

        # Configurar el widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Temporizador para actualizar los valores automáticamente
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)  # Actualizar cada 1 segundo

    def update_values(self):
        """Actualiza los valores del PID en la interfaz."""
        try:
            # Leer los valores del PID
            pv = self.plc.read_variable_float(484)  # PV
            sp = self.plc.read_variable_float(488)  # SP
            output = self.plc.read_variable_float(492)  # Output
            gain = self.plc.read_variable_float(496)  # Gain
            sample_time = self.plc.read_variable_float(500)  # SampleTime
            i_time = self.plc.read_variable_float(504)  # I_Time
            d_time = self.plc.read_variable_float(508)  # D_Time

            # Actualizar las etiquetas
            self.pv_label.setText(f"PV: {pv:.2f}")
            self.sp_label.setText(f"SP: {sp:.2f}")
            self.output_label.setText(f"Output: {output:.2f}")
            self.gain_label.setText(f"Gain: {gain:.2f}")
            self.sample_time_label.setText(f"SampleTime: {sample_time:.2f}")
            self.i_time_label.setText(f"I_Time: {i_time:.2f}")
            self.d_time_label.setText(f"D_Time: {d_time:.2f}")
        except Exception as e:
            print(f"Error al actualizar los valores: {e}")

    def closeEvent(self, event):
        """Desconecta el PLC al cerrar la aplicación."""
        self.plc.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear una instancia de PLC_S7_Communicator
    plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC

    # Crear y mostrar la ventana principal
    window = PIDApp(plc)
    window.show()

    sys.exit(app.exec())