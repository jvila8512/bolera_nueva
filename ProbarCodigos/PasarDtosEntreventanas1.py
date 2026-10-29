import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

from ProbarCodigos.PAsarDatosEntreventananas import VentanaSecundaria



class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.layout = QVBoxLayout()
        self.label_resultado = QLabel("Aquí se mostrarán los datos")
        self.layout.addWidget(self.label_resultado)
        self.button = QPushButton("Abrir Ventana Secundaria")
        self.button.clicked.connect(self.abrir_secundaria)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.secundaria = None #Iniciliza la ventana secundaria como None

    def abrir_secundaria(self):
        self.secundaria = VentanaSecundaria(self)
        self.secundaria.senal_datos.connect(self.recibir_datos)  # Conecta la señal a un slot
        self.secundaria.exec() # Abre como un diálogo modal

    def recibir_datos(self, dato1, dato2):
        self.label_resultado.setText(f"Datos recibidos: {dato1}, {dato2}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())