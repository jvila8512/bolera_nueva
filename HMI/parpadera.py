import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class BlinkingLabel(QWidget):
     def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Label Circular Parpadeante")
        self.setFixedSize(200, 200)  # Tamaño fijo de la ventana

        # Crear un QWidget que actuará como el "label" circular
        self.circle = QWidget(self)
        self.circle.setFixedSize(20, 20)  # Tamaño fijo del círculo
        self.circle.setStyleSheet("background-color: red; border-radius: 10px;")

        # Configurar el layout
        layout = QVBoxLayout()
        layout.addWidget(self.circle, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Configurar el QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_state)
        self.timer.start(800)  # Intervalo de 2 segundos

        # Estado inicial
        self.is_on = False

     def toggle_state(self):
        # Alternar entre encendido y apagado
        if self.is_on:
            self.circle.setStyleSheet("background-color: red; border-radius: 10px;")
        else:
            self.circle.setStyleSheet("background-color: #cccccc; border-radius: 10px;")

        self.is_on = not self.is_on

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlinkingLabel()
    window.show()
    sys.exit(app.exec())