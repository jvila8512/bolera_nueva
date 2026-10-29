import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget,QLineEdit,QVBoxLayout, QMessageBox,QPushButton,QTableWidget, QTableWidgetItem,QHeaderView,QHBoxLayout,QSizePolicy,QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
from ConexionBD.conexion import Conexion
from app_dialog_crud_user import DialogoUserCrud
from PyQt6.QtGui import QColor

from bd_modelos.usuario import Usuario



class UserCRUD(QWidget):
    def __init__(self,user:Usuario):
        super().__init__()
        # Cargar la UI desde el archivo .ui
        uic.loadUi("UI/crud_user.ui", self) 
      
         # Conectar a la base de datos  
        self.con = Conexion()  
        self.UserLogueado = user
        self.initGUI() 
                    
    def initGUI(self):
        self.btn_nuevo.clicked.connect(self.abrirAdminPistas)
                
        self.tabla_usuarios.setColumnCount(7)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Usuario", "Contraseña","Nombre", "Activo","Rol","Acciones"])
       
        # Ocultar el encabezado vertical (numeración de filas)
        self.tabla_usuarios.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical
        
        # Ocultar la primera columna
        self.tabla_usuarios.setColumnHidden(0, True)  # Oculta la columna con índice 0
    
        
        # Cargar los datos
        self.cargar_datos()

         # Aplicar CSS
        self.aplicar_estilos()
        
        
        
    def abrirAdminPistas(self):
        self.dasboard=DialogoUserCrud(self.cargar_datos)
      
    def cargar_datos(self):
        con1 = Conexion()
               # Obtener los datos de la tabla User
        usuarios= con1.ejecutar_sql("SELECT id_usuario, usuario, contrasena, nombre, activo, r.rol FROM usuario JOIN rol r ON usuario.id_rol = r.id_rol ")
        # Configurar el número de filas
        self.tabla_usuarios.setRowCount(len(usuarios))

        # Rellenar el QTableWidget con los datos
        for row_index, row_data in enumerate(usuarios):
            for column_index, item in enumerate(row_data):
                
               if column_index == 4:  # Columna 4 (índice 3) para el estado
                    if item == 1:
                        item_estado = QLabel("Activo")                           
                        item_estado.setStyleSheet("QLabel { color: green; text-align: center;}")
                        item_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.tabla_usuarios.setCellWidget(row_index, column_index, item_estado)
                    else:
                        item_estado = QLabel("Inactivo")
                        item_estado.setStyleSheet("QLabel { color: green;text-align: center; }")
                        item_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.tabla_usuarios.setCellWidget(row_index, column_index, item_estado)
               else:
                   table_item = QTableWidgetItem(str(item))
                   table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  
                   self.tabla_usuarios.setItem(row_index, column_index, table_item )
                  
                
                

            # Crear los botones de Editar y Borrar
            btn_editar = QPushButton()
            btn_borrar = QPushButton()
              # Establecer íconos para los botones
            btn_editar.setIcon(QIcon("iconos/update.svg"))  # Cambia esta ruta a la de tu icono
            btn_borrar.setIcon(QIcon("iconos/delete.svg"))  # Cambia esta ruta a la de tu icono

            if row_data[0]==self.UserLogueado.id_usuario:
             btn_borrar.setEnabled(False)
            # Conectar las señales de los botones a sus respectivas funciones
            btn_editar.clicked.connect(lambda checked, row=row_index: self.editar_usuario(row))
            btn_borrar.clicked.connect(lambda checked, row=row_index: self.borrar_usuario(row))

          # Ajustar el tamaño de los botones
            btn_editar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            btn_borrar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
            button_layout.addWidget(btn_editar)
            button_layout.addWidget(btn_borrar)
            button_layout.addStretch(1)  # Espacio a la derecha
              # Establecer el alineamiento del layout al centro
            # button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Establecer márgenes para el layout de los botones
            button_layout.setContentsMargins(10, 5, 10, 20)  # (izquierda, arriba, derecha, abajo)
        # Crear un QWidget para contener el layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
              # Establecer un tamaño mínimo para el QWidget que contiene los botones
            button_widget.setMinimumHeight(40)  # Ajusta la altura mínima según sea necesario
        # Añadir los botones a la tabla en la columna de acciones
            self.tabla_usuarios.setCellWidget(row_index, 6, button_widget ) # Columna de Acciones
            #self.tabla_usuarios.setColumnWidth(6, 30)  # Cambia 150 al tamaño que desees

         # Establecer un tamaño fijo para la última columna (índice 6)
        
          # Ajustar el tamaño de las columnas
        #self.tabla_usuarios.resizeColumnsToContents()
        # Cerrar la conexión
        con1.cerrar_conexion()    
        
        
        
    def aplicar_estilos(self):
         # Aplicar estilos CSS
        self.tabla_usuarios.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #ccc;
                background-color: #f9f9f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 1px;
            }
            QHeaderView::section {
                background-color: #0078d7;
                color: white;
                padding: 1px;
                font-weight: bold;
            }
            QPushButton {
          
            margin: 2px 4px;  /* Añadir margen para separar botones */
          
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #dadada;
        }
        """)

        # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Habilitar la selección de toda la fila
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

    def editar_usuario(self, row):
    
        id_usuario = int(self.tabla_usuarios.item(row, 0).text())    
        print("Id del usuarioooo",id_usuario)
        self.dasboard=DialogoUserCrud(self.cargar_datos,id_usuario)
        self.cargar_datos()
    def borrar_usuario(self, row):
        # Aquí puedes implementar la lógica para borrar el usuario
        #QMessageBox.information(self, "Borrar Usuario", f"Borrar usuario en la fila {row}")
        
        id_usuario = int(self.tabla_usuarios.item(row, 0).text())
        login=self.tabla_usuarios.item(row, 1).text()
         # Crea un mensaje de confirmación
    
                
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Confirmación de Eliminación")
        msgBox.setText(f"¿Está seguro de que desea borrar el usuario: {login} ?")
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setStandardButtons( QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                # Obtén el botón "Yes"
        boton_si = msgBox.button(QMessageBox.StandardButton.Yes)
        # Cambia el texto del botón a "Sí"
        boton_si.setText("Sí")

        # Obtén el botón "No"
        boton_no = msgBox.button(QMessageBox.StandardButton.No)
        # Deja el texto del botón "No" como está (opcional)
        # boton_no.setText("No")
       
       
    
        # Muestra el mensaje y obtiene la respuesta
        respuesta = msgBox.exec()
        
        # Si el usuario confirma (clickea en 'Yes')
        if respuesta == QMessageBox.StandardButton.Yes:
            self.con.ejecutar_sql("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            self.cargar_datos()
            
            
