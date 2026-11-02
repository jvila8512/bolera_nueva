import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt6.QtCore import Qt

from database_manager import DatabaseManager
from UI.Login import Login
from dasboard.DasBoard import MainWindow
from dasboard.main1 import Principal
from bd_modelos.usuario import Usuario


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
                self.abrir_admin_pistas(Usuario(*fila))
            self.con.cerrar()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def abrir_admin_pistas(self, user: Usuario):
        self.dasboard = MainWindow(user)
        self.hide()
