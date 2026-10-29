import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana Principal")
        
        self.label = QLabel("Texto de la segunda ventana aparecerá aquí")
        self.boton = QPushButton("Abrir Nueva Ventana")
        self.boton.clicked.connect(self.abrir_nueva_ventana)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.boton)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_nueva_ventana(self):
        self.nueva_ventana = NuevaVentana(self)
        self.nueva_ventana.show()
        self.close()


        # Crear un temporizador para cerrar la nueva ventana después de 1 segundo
        QTimer.singleShot(5000, self.nueva_ventana.close)  # 1000 ms = 1 segundo

    def recibir_texto(self, texto):
        self.label.setText(texto)

class NuevaVentana(QMainWindow):
    def __init__(self, ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal

        self.setWindowTitle("Nueva Ventana")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta ventana se cerrará en 1 segundo"))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        self.ventana_principal.recibir_texto("La segunda ventana se cerró.")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())