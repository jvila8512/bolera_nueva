from PyQt6.QtWidgets import QDialog,  QMessageBox
from ConexionBD.conexion import Conexion
from bd_modelos.usuario import Usuario
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
from PyQt6.QtCore import pyqtSignal
from bd_modelos import Sesion
import recursoAnimacion
import recursos
import bcrypt


from UI.CambiarContrasena import CambiarContrasena
class CambiarContrasenaDialog(QDialog):
     enviar_datos1 = pyqtSignal(int, str) # Señal para enviar datos
     def __init__(self,user:Usuario,sesion:Sesion):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        self.ui = CambiarContrasena()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))
        self.setWindowTitle("Cambiar Contraseña")
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
        # Referencia a mi ventana app_Gestion de pistas para poder cerrar mi Resultados
         # Limpiar mensajes de error
        self.ui.actual.setText("")
        self.ui.nueva.setText("")
        self.ui.nueva1.setText("")
        
       
        self.initGUI() 
      
                    
     def initGUI(self):
       self.ui.pushButton_2.clicked.connect(self.change_password                                             )      
       self.ui.pushButton.clicked.connect(self.close)
   
     def change_password(self):
        passActual = self.ui.passActual.text()
        passNueva = self.ui.passNueva.text()
        confirm_password =self.ui.passNuevaRep.text()

        # Limpiar mensajes de error
        self.ui.actual.setText("")
        self.ui.nueva.setText("")
        self.ui.nueva1.setText("")

        # Validar contraseña antigua
        if not self.validate_passActual(passActual):
            self.ui.actual.setText("Contraseña antigua incorrecta.")
            return

        # Validar nueva contraseña
        if passNueva != confirm_password:
            self.ui.nueva.setText("Las contraseñas no coinciden.")
            self.ui.nueva1.setText("Las contraseñas no coinciden.")
            return

        # Actualizar contraseña en la base de datos
        self.update_password(passNueva)

     def validate_passActual(self, passActual):
        # Aquí debes implementar la lógica para verificar la contraseña antigua
        # Por ejemplo, consultando la base de datos
        # Este es un ejemplo simple, deberías adaptarlo a tu lógica de negocio
        stored_hashed_password = self.UserLogueado.contrasena  # Reemplaza esto con la contraseña almacenada
        return bcrypt.checkpw(passActual.encode('utf-8'), stored_hashed_password)

     def update_password(self,passNueva):
        
        hashed_password = bcrypt.hashpw(passNueva.encode('utf-8'), bcrypt.gensalt())
        print(passNueva)
        
        # Aquí debes implementar la lógica para actualizar la contraseña en la base de datos  
       
        
        # Asumiendo que tienes una tabla 'usuarios' con un campo 'password'
        respo= self.con.ejecutar_sql("UPDATE usuario SET contrasena = ? WHERE id_usuario = ?", (hashed_password, self.UserLogueado.id_usuario))  # Cambia el ID según sea necesario
        print(respo)
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Confirmación")         
        msgBox.setText(f"Contraseña cambiada con éxito")
        msgBox.setIcon(QMessageBox.Icon.Information)
        self.close()
        msgBox.exec()
         
        # Mensaje de éxito o cerrar el formulario
        print("Contraseña actualizada con éxito.")   