import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")

        # Llamar a la función para abrir el diálogo en la segunda pantalla
        self.abrir_dialogo_en_segunda_pantalla()

    def abrir_dialogo_en_segunda_pantalla(self):
    # Obtener información sobre las pantallas
        screen_count = QApplication.screens()
        
        if len(screen_count) < 2:
            print("No hay suficientes pantallas conectadas.")
         
            return

        # Obtener la segunda pantalla
        segunda_pantalla = screen_count[1]

        # Crear un mensaje de diálogo
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Título del Diálogo")
        msg_box.setText("Este es un diálogo en la segunda pantalla.")
        
        # Calcular la posición de la segunda pantalla
        screen_geometry = segunda_pantalla.geometry()
        msg_box.setGeometry(screen_geometry.x() + 100, screen_geometry.y() + 100, 300, 100)

        # Mostrar el diálogo
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())