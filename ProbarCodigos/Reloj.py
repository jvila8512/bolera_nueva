
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, QTime

class ClockApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Reloj")
        self.setFixedSize(200, 100)

        # Crear un layout vertical
        layout = QVBoxLayout()

        # Crear una etiqueta para mostrar la hora
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 24px;")  # Cambiar tamaño de fuente
        layout.addWidget(self.time_label)

        # Establecer el layout en la ventana
        self.setLayout(layout)

        # Crear un temporizador que actualiza la hora cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1000 ms = 1 segundo

        # Actualizar la hora al iniciar
        self.update_time()

    def update_time(self):
        # Obtener la hora actual y formatearla
        current_time = QTime.currentTime()
        formatted_time = current_time.toString('HH:mm:ss')
        # Actualizar la etiqueta
        self.time_label.setText(formatted_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    clock = ClockApp()
    clock.show()
    
    sys.exit(app.exec())
