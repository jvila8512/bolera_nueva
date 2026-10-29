import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QDialog, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt


class VentanaSecundaria(QDialog):
    senal_datos = pyqtSignal(str, int) # Señal para enviar datos

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ventana Secundaria")
        self.layout = QVBoxLayout()
        self.label_resultado = QLabel("Ingrese los datos")
        self.layout.addWidget(self.label_resultado)
        self.button = QPushButton("Aceptar")
        self.button.clicked.connect(self.aceptar)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def aceptar(self):
        dato1 = "Este es el dato 1"  #Reemplaza con tu lógica para obtener dato1
        dato2 = 123 #Reemplaza con tu lógica para obtener dato2
        self.senal_datos.emit(dato1, dato2)  # Emitir la señal con los datos
        self.close()  # Cierra la ventana secundaria
