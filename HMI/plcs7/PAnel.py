import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QPalette
# Importar la clase PLC_S7_Communicator
from BoleraHolguin.plcs7.ConexionPLC import PLC_S7_Communicator



class ControlPanelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC
        self.plcConectado=self.plc.connect()
        self.setWindowTitle("Panel de Control y Visualización")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Indicadores para las entradas (I0.0 a I0.4)
        self.input_buttons = []
        input_layout = QHBoxLayout()
        for i in range(5):  # I0.0 a I0.4
            button = QPushButton(f"I0.{i}\nApagado")
            button.setFixedSize(80, 80)
            button.setStyleSheet("background-color: gray; border-radius: 40px;")
            input_layout.addWidget(button)
            self.input_buttons.append(button)
        layout.addLayout(input_layout)

        # Botones de pulsación para marcas (M10.0 en adelante)
        self.marker_buttons = []
        marker_layout = QHBoxLayout()
        for i in range(5):  # M10.0 a M10.4
            button = QPushButton(f"M10.{i}\nOFF")
            button.setFixedSize(80, 80)
            button.setStyleSheet("background-color: gray; border-radius: 0px;")
            button.clicked.connect(lambda _, i=i: self.toggle_marker(10, i))
            marker_layout.addWidget(button)
            self.marker_buttons.append(button)
        layout.addLayout(marker_layout)

        # Indicadores para las salidas (Q0.0 a Q0.4)
        self.output_buttons = []
        output_layout = QHBoxLayout()
        for i in range(5):  # Q0.0 a Q0.4
            button = QPushButton(f"Q0.{i}\nApagado")
            button.setFixedSize(80, 80)
            button.setStyleSheet("background-color: gray; border-radius: 30px;")
            output_layout.addWidget(button)
            self.output_buttons.append(button)
        layout.addLayout(output_layout)

        # Configurar el widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Temporizador para actualizar los indicadores
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_indicators)
        self.timer.start(500)  # Actualizar cada 500 ms

    def toggle_marker(self, byte_address, bit_position):
        """
        Cambia el estado de un marcador (M) y actualiza el botón correspondiente.
        """
        try:
            # Leer el estado actual del marcador
            current_value = self.plc.read_marker_bit( byte_address,bit_position)  # Lee 1 byte del marcador M1.0
            print(f" el valor leido {current_value}")
            # Cambiar el estado del marcador
            new_value = 1 if current_value == 0 else 0
            self.plc.write_marker(byte_address, bit_position, new_value)
            # Cambiar el bit 0 (M0.0) según el estado del checkbox
          
            # Actualizar el botón
            button = self.marker_buttons[bit_position]
            if new_value == 1:
                button.setText(f"M{byte_address}.{bit_position}\nON")
                button.setStyleSheet("background-color: green; border-radius: 0px;")
            else:
                button.setText(f"M{byte_address}.{bit_position}\nOFF")
                button.setStyleSheet("background-color: gray; border-radius: 0px;")
        except Exception as e:
            print(f"Error al cambiar el marcador: {e}")

    def update_indicators(self):
        """Actualiza los indicadores de entradas y salidas."""
        try:
            # Actualizar indicadores de entradas (I0.0 a I0.4)
            for i in range(5):
                bit_value = self.plc.read_input_bit(0, i)
                button = self.input_buttons[i]
                if bit_value == 1:
                    button.setText(f"I0.{i}\nEncendido")
                    button.setStyleSheet("background-color: green; border-radius: 40px;")
                else:
                    button.setText(f"I0.{i}\nApagado")
                    button.setStyleSheet("background-color: gray; border-radius: 40px;")

            # Actualizar indicadores de salidas (Q0.0 a Q0.4)
            for i in range(5):
                bit_value = self.plc.read_output_bit(0, i)
                button = self.output_buttons[i]
                if bit_value == 1:
                    button.setText(f"Q0.{i}\nEncendido")
                    button.setStyleSheet("background-color: green; border-radius: 40px;")
                else:
                    button.setText(f"Q0.{i}\nApagado")
                    button.setStyleSheet("background-color: gray; border-radius: 40px;")
        except Exception as e:
            print(f"Error al actualizar los indicadores: {e}")

    def closeEvent(self, event):
        """Desconecta el PLC al cerrar la aplicación."""
        self.plc.disconnect()
        event.accept()
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear una instancia de PLC_S7_Communicator
    plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC

    # Crear y mostrar la ventana principal
    window = ControlPanelApp()
    window.show()

    sys.exit(app.exec())