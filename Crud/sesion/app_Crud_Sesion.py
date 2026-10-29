import sys
from PyQt6 import uic
from PyQt6.QtWidgets import  QApplication,QWidget,QButtonGroup, QMessageBox,QPushButton,QTableWidget, QTableWidgetItem,QHeaderView,QHBoxLayout,QSizePolicy,QLabel
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
from ConexionBD.conexion import Conexion
from Crud.sesion.app_Reporte_Diario_Sesion import ResumenJuegosReporteSesion
from Crud.sesion.app_Resumen_SesionUser import ResumenSesionUser
from UI.crud_sesion import Sesion_CRUD
from UI.crud_user import Usuario_CRUD
from app_dialog_crud_user import DialogoUserCrud
from PyQt6.QtGui import QColor

from bd_modelos.usuario import Usuario
from bd_modelos import Sesion
import recursoAnimacion



class SesionCRUD(QWidget):
       # def __init__(self,user:Usuario,sesion: Sesion):

    def __init__(self,sesion:Sesion):
        super().__init__()
        # Initialize the UI from the generated 'main_ui' class
        self.ui = Sesion_CRUD()
        self.ui.setupUi(self)
        self.Sesion= sesion
         # Establecer la fecha actual
        self.ui.dateEdit.setDate(QDate.currentDate())
        #self.ui.todas.stateChanged.connect(self.cargar_datos)
        self.ui.dateEdit.dateChanged.connect(self.cargar_datos)
        self.ui.dateEdit.setEnabled(False)
         # Conectar a la base de datos  
       
        
        # Conectar a la base de datos  
        self.con = Conexion()  
        self.conexion = self.con.devolverConexion()
        self.cursor = self.conexion.cursor()
        
       # self.UserLogueado = user
        self.initGUI() 
     

                    
    def initGUI(self):
       # Agrupar los RadioButtons
       self.botones = QButtonGroup(self)
       self.botones.addButton(self.ui.todas_2, 1)
       self.botones.addButton(self.ui.activas, 2)
       self.botones.addButton(self.ui.fecha, 3)
        # Conectar la señal de cambio de botón
       self.botones.buttonClicked.connect(self.generar_accion)
       
       self.ui.activas.setChecked(True)
                 
       self.ui.tabla_usuarios.setColumnCount(5)
       self.ui.tabla_usuarios.setHorizontalHeaderLabels(["ID Sesion", "Usuario","Fecha", "Activa", "Acciones"])       
        # Ocultar el encabezado vertical (numeración de filas)
       self.ui.tabla_usuarios.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical        
        # Ocultar la primera columna
       self.ui.tabla_usuarios.setColumnHidden(0, True)  # Oculta la columna con índice 0 
       self.ui.pushButton.clicked.connect(self.abrirReportes)
          
        # Cargar los datos
       self.cargar_datos()
         # Aplicar CSS
       self.aplicar_estilos()
    def generar_accion(self):
        # Verificar cuál botón está seleccionado
        radio_seleccionado = self.botones.checkedButton()
        if radio_seleccionado is not None:
            if radio_seleccionado.text()=="Todas" or radio_seleccionado.text()=="Activas" :
               self.ui.dateEdit.setEnabled(False)
            else:
                self.ui.dateEdit.setEnabled(True) 
            
        self.cargar_datos()   
           # mensaje = f"Has seleccionado: {radio_seleccionado.text()}"
            #QMessageBox.information(self, "Selección", mensaje)    
    def abrirReportes(self):
         resportesUser= ResumenJuegosReporteSesion(self, self.Sesion)
         resportesUser.exec()
        
                 
    def abrirAdminPistas(self):
        self.dasboard=DialogoUserCrud(self.cargar_datos)
      
    def cargar_datos(self):
         # Obtener el estado del checkbox
        query =""
        params = []
        if self.ui.todas_2.isChecked():
                    query = "SELECT id_sesion,usuario,fecha,activa FROM sesion JOIN usuario u ON sesion.id_usuario = u.id_usuario ORDER BY fecha DESC "

        
        else:
         if self.ui.activas.isChecked():
        
        
           query="SELECT id_sesion,usuario,fecha,activa FROM sesion  JOIN usuario u ON sesion.id_usuario = u.id_usuario WHERE activa = 1 ORDER BY fecha DESC"
         else:
            query = "SELECT id_sesion,usuario,fecha,activa FROM sesion JOIN usuario u ON sesion.id_usuario = u.id_usuario Where  DATE(sesion.fecha)= ?  ORDER BY fecha DESC "
            params = ( self.ui.dateEdit.date().toString("yyyy-MM-dd"),)
       
       
       
       
      

      

        self.cursor.execute(query, params)
        
        rows = self.cursor.fetchall()

        self.ui.tabla_usuarios.setRowCount(0)
        for row in rows:
            row_position = self.ui.tabla_usuarios.rowCount()
            self.ui.tabla_usuarios.insertRow(row_position)

            for column, data in enumerate(row[:-1]):  # Excluyendo el último campo para las acciones
             table_item = QTableWidgetItem(str(data))
             table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
             self.ui.tabla_usuarios.setItem(row_position, column, table_item )
            

            # Botón para activar/desactivar
            activa_button = QPushButton("No Activa" if row[3] == 0 else "Activa")
            activa_button.setStyleSheet(  "QPushButton { color: red; text-align: center;font-weight: bold; font-family: Arial, sans-serif;}" if row[3] == 0 else  "QPushButton {   background-color: green; color: white; font-weight: bold; font-family: Arial, sans-serif; text-align: center;  border-radius: 5px;} ")
            
            
            activa_button.clicked.connect(lambda checked, r=row: self.toggle_activa(r[0], row_position))
            self.ui.tabla_usuarios.setCellWidget(row_position, 3, activa_button)  # Columna de 'Activa'

            # Botones de actualizar y borrar
            action_layout = QHBoxLayout()
            update_button = QPushButton()
            update_button.setIcon(QIcon(":/animacion/iconos/bolera.svg"))  # Cambia esta ruta a la de tu icono          
            update_button.clicked.connect(lambda checked, r=row: self.update_row(r))    
            delete_button = QPushButton()
            delete_button.clicked.connect(lambda checked, r=row: self.delete_row(r[0]))
            delete_button.setIcon(QIcon(":/animacion/iconos/delete.svg"))  # Cambia esta ruta a la de tu icono
             # Ajustar el tamaño de los botones
            update_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            delete_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
            button_layout.addWidget(update_button)
            button_layout.addWidget(delete_button)
            button_layout.addStretch(1)  # Espacio a la derecha
            button_layout.setContentsMargins(10, 5, 10, 20)  # (izquierda, arriba, derecha, abajo)
            action_layout.addWidget(update_button)
            action_layout.addWidget(delete_button)            
            # Crear un QWidget para contener el layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
              # Establecer un tamaño mínimo para el QWidget que contiene los botones
            button_widget.setMinimumHeight(40)  # Ajusta la altura mínima según sea necesario
            self.ui.tabla_usuarios.setCellWidget(row_position, 4, button_widget ) # Columna de Acciones

    def cargar_datos1(self,date):
         # Obtener el estado del checkbox
        
        query = "SELECT id_sesion,usuario,fecha,activa FROM sesion JOIN usuario u ON sesion.id_usuario = u.id_usuario Where  DATE(sesion.fecha)= ?  ORDER BY fecha DESC "

        
        print(date.toString("yyyy-MM-dd"))
       
       
       
       
        params = (date.toString("yyyy-MM-dd"),)

      

        self.cursor.execute(query, params)
        
        rows = self.cursor.fetchall()

        self.ui.tabla_usuarios.setRowCount(0)
        for row in rows:
            row_position = self.ui.tabla_usuarios.rowCount()
            self.ui.tabla_usuarios.insertRow(row_position)

            for column, data in enumerate(row[:-1]):  # Excluyendo el último campo para las acciones
             table_item = QTableWidgetItem(str(data))
             table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
             self.ui.tabla_usuarios.setItem(row_position, column, table_item )
            

            # Botón para activar/desactivar
            activa_button = QPushButton("No Activa" if row[3] == 0 else "Activa")
            activa_button.setStyleSheet(  "QPushButton { color: red; text-align: center;font-weight: bold; font-family: Arial, sans-serif;}" if row[3] == 0 else  "QPushButton {   background-color: green; color: white; font-weight: bold; font-family: Arial, sans-serif; text-align: center;  border-radius: 5px;} ")
            
            
            activa_button.clicked.connect(lambda checked, r=row: self.toggle_activa(r[0], row_position))
            self.ui.tabla_usuarios.setCellWidget(row_position, 3, activa_button)  # Columna de 'Activa'

            # Botones de actualizar y borrar
            action_layout = QHBoxLayout()
            update_button = QPushButton()
            update_button.setIcon(QIcon(":/animacion/iconos/bolera.svg"))  # Cambia esta ruta a la de tu icono          
            update_button.clicked.connect(lambda checked, r=row: self.update_row(r[0]))    
            delete_button = QPushButton()
            delete_button.clicked.connect(lambda checked, r=row: self.delete_row(r[0]))
            delete_button.setIcon(QIcon(":/animacion/iconos/delete.svg"))  # Cambia esta ruta a la de tu icono
             # Ajustar el tamaño de los botones
            update_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            delete_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
            button_layout.addWidget(update_button)
            button_layout.addWidget(delete_button)
            button_layout.addStretch(1)  # Espacio a la derecha
            button_layout.setContentsMargins(10, 5, 10, 20)  # (izquierda, arriba, derecha, abajo)
            action_layout.addWidget(update_button)
            action_layout.addWidget(delete_button)            
            # Crear un QWidget para contener el layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
              # Establecer un tamaño mínimo para el QWidget que contiene los botones
            button_widget.setMinimumHeight(40)  # Ajusta la altura mínima según sea necesario
            self.ui.tabla_usuarios.setCellWidget(row_position, 4, button_widget ) # Columna de Acciones
             
        
    def aplicar_estilos(self):
        self.ui.tabla_usuarios.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

            # Desactivar la selección
        
        self.ui.tabla_usuarios.setSelectionMode(QTableWidget.SelectionMode.NoSelection) 
         # Aplicar estilos CSS
        self.ui.tabla_usuarios.setStyleSheet("""
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
        self.ui.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.ui.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Habilitar la selección de toda la fila
       
        
    def toggle_activa(self, id_sesion, row_position):
        # Cambiar el estado de 'activa'
        self.cursor.execute("SELECT activa FROM sesion WHERE id_sesion = ?", (id_sesion,))
        activa_value = self.cursor.fetchone()[0]
        
        new_value = 1 if activa_value == 0 else 0
        self.cursor.execute("UPDATE sesion SET activa = ? WHERE id_sesion = ?", (new_value, id_sesion))
        self.conexion.commit()
        
        # Actualizar la tabla
        self.cargar_datos()
        

    def update_row(self, row):
        # Aquí puedes implementar la lógica para actualizar la fila seleccionada
        print(f"Actualizar fila11111111: {row[0]} {row[1]} {row[2]}")
        resportesUser= ResumenSesionUser(self, row[0],row[1],row[2])
        resportesUser.exec()
       

    def delete_row(self, id_sesion):
        # Eliminar la sesión
        confirmation = QMessageBox.question(self, 'Confirmar', '¿Estás seguro de que quieres borrar esta sesión?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmation == QMessageBox.StandardButton.Yes:
            self.cursor.execute("DELETE FROM sesion WHERE id_sesion = ?", (id_sesion,))
            self.conexion.commit()
            # Actualizar la tabla
            self.cargar_datos()

        
            
