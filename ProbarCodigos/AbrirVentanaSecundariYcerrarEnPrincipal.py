import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana Principal")
        self.tercera_ventana = None
        
        self.label = QLabel("Esperando interacción...")
        self.boton_abrir_segunda = QPushButton("Abrir Segunda Ventana")
        self.boton_cerrar_tercera = QPushButton("Cerrar Tercera Ventana", self)
        
        self.boton_abrir_segunda.clicked.connect(self.abrir_segunda_ventana)
        self.boton_cerrar_tercera.clicked.connect(self.cerrar_tercera_ventana)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.boton_abrir_segunda)
        layout.addWidget(self.boton_cerrar_tercera)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_segunda_ventana(self):
        self.segunda_ventana = SegundaVentana(self)
        self.segunda_ventana.show()

    def cerrar_tercera_ventana(self):
        if self.tercera_ventana:
            self.tercera_ventana.close()
            self.tercera_ventana = None
            self.label.setText("Tercera ventana cerrada.")

    def recibir_texto(self, texto):
        self.label.setText(texto)

class SegundaVentana(QMainWindow):
    def __init__(self, ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal

        self.setWindowTitle("Segunda Ventana")
        
        self.boton_abrir_tercera = QPushButton("Abrir Tercera Ventana")
        self.boton_abrir_tercera.clicked.connect(self.abrir_tercera_ventana)

        layout = QVBoxLayout()
        layout.addWidget(self.boton_abrir_tercera)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_tercera_ventana(self):
        self.tercera_ventana = TerceraVentana(self)
        self.ventana_principal.tercera_ventana = self.tercera_ventana
        self.tercera_ventana.show()
        self.close()  # Cierra la segunda ventana

class TerceraVentana(QMainWindow):
    def __init__(self, segunda_ventana):
        super().__init__()
        self.segunda_ventana = segunda_ventana

        self.setWindowTitle("Tercera Ventana")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la tercera ventana."))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())