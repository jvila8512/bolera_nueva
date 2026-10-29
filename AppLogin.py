import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox,QDialog
import bcrypt
from PyQt6.QtCore import Qt

from ConexionBD.conexion import Conexion
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
         # Quitar el botón de cerrar
        self.ui.pushButton_2.clicked.connect(self.cerrar)
        self.show() 
        self.con = Conexion('./bolera.db')  
        
    def cerrar(self):
     self.close()        
    def loginfunction(self):
            usuario=self.ui.email.text()
            contrasena=self.ui.password.text()          
            
           # print("Successfully logged in with email: ", usuario, "and password:",contrasena)
                # Llamar al método para verificar el usuario y la contraseña
            if self.con.verificar_usuario(usuario, contrasena):
                  
                    # Si las credenciales son correctas, abrir la ventana adminPistas
                    self.abrir_admin_pistas(self.con.devolverUsuario(usuario,contrasena))
                    self.con.cerrar_conexion()
            else:
                    # Mostrar un mensaje de error si las credenciales son incorrectas
                    QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

   
    
    def abrir_admin_pistas(self,user:Usuario):    
     
      self.dasboard=MainWindow(user)
        
      self.hide()
       




    
    