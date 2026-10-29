from PyQt6.QtWidgets import QDialog,  QMessageBox
from ConexionBD.conexion import Conexion
from UI.perfil import Perfil
from bd_modelos.usuario import Usuario
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
from PyQt6.QtCore import pyqtSignal
from bd_modelos import Sesion
import recursoAnimacion
import recursos
import bcrypt

class PerfilDialog(QDialog):
     enviar_datosUser = pyqtSignal(Usuario) # Señal para enviar datos
     def __init__(self,user:Usuario,sesion:Sesion):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        self.ui = Perfil()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))
        self.setWindowTitle("Perfil")
          # Conectar a la base de datos  
        self.con = Conexion()  
        self.cursor =  self.con.devolverConexion().cursor()
        self.UserLogueado = user
        self.Sesion= sesion
        # Referencia a mi ventana app_Gestion de pistas para poder cerrar mi Resultados
       # Conectar a la base de datos  
        self.con = Conexion()  
        self.UserLogueado = user
        self.Sesion= sesion
        self.ui.usuarioLabel.setText("")
        self.ui.nombreLabel.setText("")
        self.initGUI() 
      
                    
     def initGUI(self):
       self.ui.pushButton_2.clicked.connect(self.actualizar)      
       self.ui.pushButton.clicked.connect(self.close)
       
     def actualizar(self):
        usuario = self.ui.usuario.text()
        nombre = self.ui.nombre.text()

        if not usuario and not nombre:
            self.ui.usuarioLabel.setText("Debe escribir datos para actualizar")
            self.ui.nombreLabel.setText("Debe escribir datos para actualizar")
            return
# Construir la consulta de actualización
        query = "UPDATE usuario SET "
        params = []

        if usuario:
            query += "usuario = ? "
            params.append(usuario)

        if nombre:
            if params:  # Si ya hay un parámetro, agrega una coma
                query += ", "
            query += "nombre = ? "
            params.append(nombre)

        query += "WHERE id_usuario = ?"
        params.append(self.UserLogueado.id_usuario)

        # Ejecutar la consulta
      
        self.con.ejecutar_sql(query, params)
        UserActualizado=self.con.devolverUsuarioporID(self.UserLogueado.id_usuario)
      
        self.enviar_datosUser.emit(UserActualizado) 
      
        

        # Limpiar campos después de la actualización
        self.ui.usuario.clear()
        self.ui.nombre.clear()
        self.close()
        # Mensaje de éxito
        QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")

     def closeEvent(self, event):
        # Cerrar la conexión a la base de datos al cerrar la aplicación
        self.con.cerrar_conexion()
        event.accept()