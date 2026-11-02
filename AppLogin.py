import sys
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt6.QtCore import Qt

from database_manager import DatabaseManager
from UI.Login import Login
from dasboard.DasBoard import MainWindow
from dasboard.main1 import Principal
from bd_modelos.usuario import Usuario
from bd_modelos.Sesion import Sesion


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Inicializar la Clase
        self.ui = Login()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.loginfunction)
        # Quitar el boton de cerrar
        self.ui.pushButton_2.clicked.connect(self.cerrar)
        self.show()
        self.con = DatabaseManager('./bolera.db')

    def cerrar(self):
        self.close()

    def loginfunction(self):
        usuario = self.ui.email.text()
        contrasena = self.ui.password.text()

        # Verificacion con bcrypt via DatabaseManager (misma semantica que Conexion)
        if self.con.verificar_usuario_hash(usuario, contrasena):
            fila = self.con.obtener_usuario_por_nombre(usuario)
            if fila:
                user = Usuario(*fila)
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id_sesion = self.con.crear_sesion(user.id_usuario, fecha)
                sesion = Sesion(id_sesion, user.id_usuario, 1, fecha)
                self.abrir_admin_pistas(user, sesion)
            self.con.cerrar()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def abrir_admin_pistas(self, user: Usuario, sesion: Sesion):
        self.dasboard = MainWindow(user, sesion)
        # MainWindow llama setWindowFlags() despues de showMaximized(), lo que oculta
        # la ventana; hay que volver a mostrarla para que aparezca el dashboard.
        self.dasboard.showMaximized()
        self.hide()
