
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMenu
from PyQt6.QtGui import  QAction
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Ejemplo de Menú Contextual")
        self.setGeometry(100, 100, 300, 200)

        # Crear un botón
        self.boton_usuario = QPushButton("Usuario", self)
        self.boton_usuario.setGeometry(100, 80, 100, 30)

        # Conectar el botón a la función que muestra el menú contextual
        self.boton_usuario.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.boton_usuario.clicked.connect(self.mostrar_menu)

        # Crear el menú contextual
        self.menu_contextual = QMenu(self)

        # Añadir acciones al menú
        self.accion_cerrar_sesion = QAction("Cerrar sesión", self)
        self.accion_cambiar_contrasena = QAction("Cambiar contraseña", self)

        # Conectar las acciones a funciones (puedes definir las funciones según sea necesario)
        self.accion_cerrar_sesion.triggered.connect(self.cerrar_sesion)
        self.accion_cambiar_contrasena.triggered.connect(self.cambiar_contrasena)

        # Añadir acciones al menú
        self.menu_contextual.addAction(self.accion_cerrar_sesion)
        self.menu_contextual.addAction(self.accion_cambiar_contrasena)

    def mostrar_menu(self):
        # Mostrar el menú contextual en la posición del botón
        self.menu_contextual.exec(self.boton_usuario.mapToGlobal(self.boton_usuario.rect().bottomLeft()))

    def cerrar_sesion(self):
        print("Cerrar sesión")

    def cambiar_contrasena(self):
        print("Cambiar contraseña")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
