import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
import bcrypt
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
import recursoAnimacion
import recursos
from ConexionBD.conexion import Conexion
from UI.dialog_user_crud import UserCrud


class DialogoUserCrud(QDialog):
      def __init__(self,  cargar_datos,id_usuario=None):  
        super().__init__()
                 # Initialize the UI from the generated 'main_ui' class
        self.ui = UserCrud()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))
    

        #self.ui.setWindowTitle("Formulario de Usuario")
        self.con = Conexion()  
        self.cargar_datos = cargar_datos       
        self.id=id_usuario
        self.login= self.con.obtener_usuario_por_id(id_usuario)
        
        self.ui.sms_usuario.setText("")
        self.ui.sms_nombre.setText("")
        self.ui.sms_contrasena.setText("")
         # Recuperar los roles
        roles = self.con.ejecutar_sql("SELECT * FROM rol")
          # Llenar el QComboBox
        for rol in roles:
            self.ui.rol.addItem(rol[1], rol[0])  # Agregamos el nombre y el ID como datos del item
            
        self.ui.btn_guardar.clicked.connect(self.guardar_usuario)
        self.ui.pushButton_2.clicked.connect(self.close)
        
         # Si se proporcionó un usuario, cargar sus datos en el formulario
        if id_usuario:
            self.cargar_usuario(id_usuario)
        
        
        self.exec() 
        
      def guardar_usuario(self):
        nombre = self.ui.nombre.text()
        usuario = self.ui.usuario.text()
        rol_id = self.ui.rol.currentData()  # Obtener el ID del rol seleccionado
        contrasena = self.ui.contrasena.text()
        activo= self.ui.activo.isChecked()  # Obtener el estado del QCheckBox    

         # Encriptar la contraseña
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        
        
        # Validar los datos (asegúrate de que todos los campos obligatorios estén completos)
        if not nombre or not usuario or  (self.id is None and not contrasena):
            # Mostrar un mensaje de error si los campos obligatorios no están llenos        
            if not nombre:
              self.ui.sms_nombre.setText(" *Campo obligatorio: nombre")
            else:
               self.ui.sms_nombre.setText("")
               
            if not usuario:
                self.ui.sms_usuario.setText(" *Campo obligatorio: usuario")
            else:
               self.ui.sms_usuario.setText("")    
            if not contrasena :  # Cambios aquí
                self.ui.sms_contrasena.setText(" *Campo obligatorio: contraseña")
            else:
               self.ui.sms_contrasena.setText("")
            return
        

        # Si se proporciono un usuario, actualizar sus datos
        if self.id is not None:
            # Actualizar los datos del usuario en la base de datos
            # (Debes implementar la lÃ³gica para actualizar el usuario)
            # Por ejemplo:
            existe_usuario = self.con.ejecutar_sql( "SELECT usuario FROM usuario WHERE usuario = ?", (usuario,) )
         
           
            if usuario != self.login[1] :
            
              if existe_usuario and len(existe_usuario) > 0 and self.id is not None : # Verifica si el usuario ya existe
                # Mostrar un mensaje de error si el usuario ya existe
                self.ui.sms_usuario.setText("El usuario ya existe en la base de datos")          
                self.ui.sms_nombre.setText("")
                self.ui.sms_contrasena.setText("")
                return 
            
            
            if contrasena:
              resp=  self.con.ejecutar_sql(
                  "UPDATE usuario SET usuario = ? ,contrasena = ?, activo = ?, id_rol = ?,nombre = ? WHERE id_usuario = ?",
                  ( usuario,  bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()), activo, rol_id, nombre, self.id)
              )
            else:
             resp=  self.con.ejecutar_sql(
                  "UPDATE usuario SET usuario = ? , activo = ?, id_rol = ?,nombre = ? WHERE id_usuario = ?",
                  ( usuario, activo, rol_id, nombre, self.id)
              )
             print(resp)
        else:
            # Insertar el nuevo usuario en la base de datos
             # Validar que el usuario no exista en la base de datos
         existe_usuario = self.con.ejecutar_sql( "SELECT 1 FROM usuario WHERE usuario = ?", (usuario,) )
         if existe_usuario and len(existe_usuario) > 0 and self.id is  None : # Verifica si el usuario ya existe
            # Mostrar un mensaje de error si el usuario ya existe
            self.ui.sms_usuario.setText("El usuario ya existe en la base de datos")          
            self.ui.sms_nombre.setText("")
            self.ui.sms_contrasena.setText("")
            return 
        # Si no se proporcionÃ³ un usuario, insertar uno nuevo
         resp=self.con.ejecutar_sql("INSERT INTO usuario (usuario,contrasena,nombre,activo,id_rol) VALUES (?,?,?,?,?)",(usuario,hashed_contrasena,nombre,activo,rol_id))
         
         
        self.con.cerrar_conexion()
        self.cargar_datos()
        self.close()
         
        #self.cargar_datos()  # Ejecuta el método al cargar datos en la tabla        
          # Limpiar los campos
        self.ui.nombre.clear()
        self.ui.usuario.clear()
        self.ui.contrasena.clear()  # Limpiar el campo de contraseña
        self.ui.rol.setCurrentIndex(0)  # Restablecer el combobox al primer elemento
        self.ui.activo.setChecked(False)  # Restablecer el checkbox    
            
      def cargar_usuario(self, id_usuario):
        # Obtener los datos del usuario desde la base de datos
        # (Debes implementar la lógica para obtener el usuario basado en su ID o nombre)
        # Por ejemplo:
        datos_usuario = self.con.obtener_usuario_por_id(id_usuario)
        if datos_usuario:
          
            #print( datos_usuario)
               # Establecer los valores en los campos del formulario
            self.ui.usuario.setText(datos_usuario[1])
            self.ui.login=datos_usuario[1]
            #self.contrasena.setText(datos_usuario[2])
            self.ui.activo.setChecked(datos_usuario[3])
            self.ui.rol.setCurrentIndex(self.ui.rol.findData(datos_usuario[4]))  # Establecer el rol
            self.ui.nombre.setText(datos_usuario[5])
         
            
           
          
            # ... (Establece el resto de los campos del formulario)
        else:
            # Mostrar un mensaje de error si el usuario no se encontró
            print(f"Error: Usuario con ID  no encontrado.")
    

