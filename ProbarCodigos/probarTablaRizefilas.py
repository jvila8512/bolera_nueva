import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, QTime,Qt
from PyQt6.QtGui import QFont


class Cronometro(QWidget):
    def __init__(self, segundos_iniciales):
        super().__init__()

        self.setWindowTitle("Cronómetro")
        self.segundos_iniciales = segundos_iniciales
        self.tiempo_restante = segundos_iniciales
        self.tiempo = QTime(0, 0, 0).addSecs(segundos_iniciales)  #Creamos un objeto QTime a partir de los segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_cronometro)


        self.label_cronometro = QLabel(self.formato_tiempo())
        font = QFont("Arial", 48)  #Ajusta el tamaño de la fuente según tu gusto
        font.setBold(True)
        self.label_cronometro.setFont(font)
        self.label_cronometro.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centrar el texto

        layout = QVBoxLayout()
        layout.addWidget(self.label_cronometro)
        self.setLayout(layout)

    def formato_tiempo(self):
        horas = self.tiempo.hour()
        minutos = self.tiempo.minute()
        segundos = self.tiempo.second()
        return f"{horas:02}:{minutos:02}:{segundos:02}"  #Formato HH:MM:SS

    def iniciar_cronometro(self):
        self.timer.start(1000)  # 1000 milisegundos = 1 segundo
    def actualizar_cronometro(self):
        self.tiempo = self.tiempo.addSecs(-1)
        self.label_cronometro.setText(self.formato_tiempo())
        self.tiempo_restante -=1
        if self.tiempo_restante <=0:
            self.timer.stop()

    def detener_cronometro(self):
      self.timer.stop()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    segundos_inicio = 3650  # Comienza con 60 segundos (1 minuto) - Cambia este valor a tu gusto
    cronometro = Cronometro(segundos_inicio)
    cronometro.show()
    cronometro.iniciar_cronometro()
    sys.exit(app.exec())