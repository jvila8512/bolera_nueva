import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class VentanaSecundaria(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Secundaria")
        self.setGeometry(150, 150, 300, 200)  # Tamaño y posición de la ventana

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        
        self.boton_abrir = QPushButton("Abrir Ventana Secundaria", self)
        self.boton_abrir.clicked.connect(self.abrir_ventana_secundaria)
        
        self.boton_cerrar = QPushButton("Cerrar Ventana Secundaria", self)
        self.boton_cerrar.clicked.connect(self.cerrar_ventana_secundaria)
        self.boton_cerrar.setEnabled(False)  # Deshabilitar al inicio
        
        # Configurar el layout
        layout = QVBoxLayout()
        layout.addWidget(self.boton_abrir)
        layout.addWidget(self.boton_cerrar)
        self.setLayout(layout)
        
        self.ventana_secundaria = None  # Inicialmente no hay ventana secundaria

    def abrir_ventana_secundaria(self):
        if not self.ventana_secundaria:
            self.ventana_secundaria = VentanaSecundaria()
            self.ventana_secundaria.show()
            self.boton_cerrar.setEnabled(True)  # Habilitar el botón para cerrar

    def cerrar_ventana_secundaria(self):
        if self.ventana_secundaria:
            self.ventana_secundaria.close()
            self.ventana_secundaria = None  # Limpiar la referencia
            self.boton_cerrar.setEnabled(False)  # Deshabilitar el botón

# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec())
