import sys
from PyQt6 import uic
from PyQt6.QtWidgets import  QApplication,QWidget,QButtonGroup, QMessageBox,QPushButton,QTableWidget, QTableWidgetItem,QHeaderView,QHBoxLayout,QSizePolicy,QLabel
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
from ConexionBD.conexion import Conexion
from Crud.sesion.app_Reporte_Diario_Sesion import ResumenJuegosReporteSesion
from Crud.sesion.app_Resumen_SesionUser import ResumenSesionUser
from UI.crud_juegos import JuegosCRUD
from app_dialog_crud_user import DialogoUserCrud
from PyQt6.QtGui import QColor

from bd_modelos.usuario import Usuario
from bd_modelos import Sesion
import recursoAnimacion



class JuegosCrudADmin(QWidget):
       # def __init__(self,user:Usuario,sesion: Sesion):

    def __init__(self,sesion:Sesion):
        super().__init__()
        # Initialize the UI from the generated 'main_ui' class
        self.ui = JuegosCRUD()
        self.ui.setupUi(self)
        self.Sesion= sesion
         # Establecer la fecha actual
        self.ui.dateEdit.setDate(QDate.currentDate())
        # Establecer la fecha actual
        self.ui.dateEdit_2.setDate(QDate.currentDate())
        #self.ui.todas.stateChanged.connect(self.cargar_datos)
        self.ui.dateEdit.dateChanged.connect(self.fechaSesion)
        self.ui.dateEdit_2.dateChanged.connect(self.fechaJuego)
        # self.ui.dateEdit.setEnabled(False)
         # Conectar a la base de datos  
        self.ui.tabla_usuarios.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

            # Desactivar la selección
     
        self.ui.tabla_usuarios.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        self.op=1
        
        # Conectar a la base de datos  
        self.con = Conexion()  
        self.conexion = self.con.devolverConexion()
        self.cursor = self.conexion.cursor()
        
       # self.UserLogueado = user
        self.initGUI() 
     

                    
    def initGUI(self):
      
                 
       self.ui.tabla_usuarios.setColumnCount(11)
        
       self.ui.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Fecha Sesión","Fecha Juego","Tipo Juego", "Jugadores","Precio", "Pista","Tiempo","Terminado","Usuario","Acciones"])       
        # Ocultar el encabezado vertical (numeración de filas)
       self.ui.tabla_usuarios.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical        
        # Ocultar la primera columna
       self.ui.tabla_usuarios.setColumnHidden(0, True)  # Oculta la columna con índice 0 
       #self.ui.pushButton.clicked.connect(self.abrirReportes)
       self.ui.pushButton.clicked.connect(self.borrarFiltro)  
        # Cargar los datos
       self.cargar_datos(self.op)
         # Aplicar CSS
       self.aplicar_estilos()
    
    
    def fechaSesion(self):
        self.op=3
        self.cargar_datos(3)
   
   
    def fechaJuego(self):
        self.op=2
        self.cargar_datos(self.op)
        
    def abrirReportes(self):
         resportesUser= ResumenJuegosReporteSesion(self, self.Sesion)
         resportesUser.exec()
        
    def borrarFiltro(self):
        self.op=1
        self.cargar_datos(self.op)        
   
      
    def cargar_datos(self,op):
         # Obtener el estado del checkbox
        query =""
        params = []
        if op==1:
         query = """ SELECT juego.id_juego,sesion.fecha, juego.fecha, tipo_juego, juego.cant_jugadores,precio.precio, juego.pista, tiempo_juego.tiempo,terminado, usuario
                   FROM juego 
                   LEFT JOIN tiempo_juego ON juego.id_tiempo = tiempo_juego.id_tiempo
                   LEFT JOIN sesion ON sesion.id_sesion = juego.id_sesion 
                   LEFT JOIN precio ON juego.id_precio = precio.id_precio
                   LEFT JOIN tipo_juego ON juego.id_tipo_juego = tipo_juego.id_tipo_juego
                   JOIN usuario ON sesion.id_usuario = usuario.id_usuario
                   ORDER BY sesion.fecha ASC"""
        else:          
         if op==2:
         
            query = """ SELECT juego.id_juego,sesion.fecha, juego.fecha, tipo_juego, juego.cant_jugadores,precio.precio, juego.pista, tiempo_juego.tiempo,terminado, usuario
                   FROM juego 
                   LEFT JOIN tiempo_juego ON juego.id_tiempo = tiempo_juego.id_tiempo
                   LEFT JOIN sesion ON sesion.id_sesion = juego.id_sesion 
                   LEFT JOIN precio ON juego.id_precio = precio.id_precio
                   LEFT JOIN tipo_juego ON juego.id_tipo_juego = tipo_juego.id_tipo_juego
                   JOIN usuario ON sesion.id_usuario = usuario.id_usuario
                   where  DATE(juego.fecha) = ?
                   ORDER BY sesion.fecha ASC"""
                
            params=(self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),)     
         else:   
          if op==3:
          
          
            query = """ SELECT juego.id_juego,sesion.fecha, juego.fecha, tipo_juego, juego.cant_jugadores,precio.precio, juego.pista, tiempo_juego.tiempo,terminado, usuario
                   FROM juego 
                   LEFT JOIN tiempo_juego ON juego.id_tiempo = tiempo_juego.id_tiempo
                   LEFT JOIN sesion ON sesion.id_sesion = juego.id_sesion 
                   LEFT JOIN precio ON juego.id_precio = precio.id_precio
                   LEFT JOIN tipo_juego ON juego.id_tipo_juego = tipo_juego.id_tipo_juego
                   JOIN usuario ON sesion.id_usuario = usuario.id_usuario
                   where  DATE(sesion.fecha) = ?
                   ORDER BY sesion.fecha ASC"""
            params=(self.ui.dateEdit.date().toString("yyyy-MM-dd"),)
       
       
      

      

        self.cursor.execute(query, params)
        
        rows = self.cursor.fetchall()
        
        self.ui.tabla_usuarios.setRowCount(len(rows))
        
         # Rellenar el QTableWidget con los datos
        for row_index, row_data in enumerate(rows):
            bandera=False
            for column_index, item in enumerate(row_data):
                   
                   table_item = QTableWidgetItem(str(item))                   
                   table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                   
                   if column_index == 3 and item == "Torneo": 
                       bandera=True
                   if column_index == 5 and bandera:                      
                        table_item_4 = QTableWidgetItem("-----")
                        table_item_4.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.ui.tabla_usuarios.setItem(row_index, column_index, table_item_4)
                     
                   else:
                      if column_index == 8 :
                             
                                if item == 1:
                                    item_estado = QLabel("Terminado")                           
                                    item_estado.setStyleSheet("QLabel { color: green; text-align: center;}")
                                    item_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.ui.tabla_usuarios.setCellWidget(row_index, column_index, item_estado)
                                else:
                                    item_estado = QLabel("----")
                                    item_estado.setStyleSheet("QLabel { color: red;text-align: center; }")
                                    item_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.ui.tabla_usuarios.setCellWidget(row_index, column_index, item_estado)
                   
                      else:
                            self.ui.tabla_usuarios.setItem(row_index, column_index, table_item )
        
        
        
        

                         
             # Botones de actualizar y borrar
            action_layout = QHBoxLayout()
            update_button = QPushButton()
            update_button.setIcon(QIcon(":/animacion/iconos/update.svg"))  # Cambia esta ruta a la de tu icono          
            update_button.clicked.connect(lambda checked, r=row_index: self.update_row(r))    
            delete_button = QPushButton()
            delete_button.clicked.connect(lambda checked, r=row_index: self.delete_row(r))
            delete_button.setIcon(QIcon(":/animacion/iconos/delete.svg"))  # Cambia esta ruta a la de tu icono
             # Ajustar el tamaño de los botones
            update_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            delete_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
            #button_layout.addWidget(update_button)
            button_layout.addWidget(delete_button)
            button_layout.addStretch(1)  # Espacio a la derecha
            button_layout.setContentsMargins(10, 5, 10, 20)  # (izquierda, arriba, derecha, abajo)
            #action_layout.addWidget(update_button)
            action_layout.addWidget(delete_button)            
            # Crear un QWidget para contener el layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
              # Establecer un tamaño mínimo para el QWidget que contiene los botones
            button_widget.setMinimumHeight(40)  # Ajusta la altura mínima según sea necesario
            self.ui.tabla_usuarios.setCellWidget(row_index, 10, button_widget ) # Columna de Acciones
        self.add_column_footer()   
  
    def add_column_footer(self):
        # Calculando la suma de cada columna y añadiéndola como fila de pie de columna
        row_count = self.ui.tabla_usuarios.rowCount()
        column_count = self.ui.tabla_usuarios.columnCount()
        
        footer_row = row_count  # Row where the footer will be added

        self.ui.tabla_usuarios.insertRow(footer_row)  # Insertar una nueva fila

        for column in range(column_count):
            total = 0
            if column==4 :
                for row in range(row_count):
                    
                    item = self.ui.tabla_usuarios.item(row, column)
                    if item is not None:
                        total += int(item.text())  # Sumar los valores

                # Añadiendo la suma total en la nueva fila
                self.ui.tabla_usuarios.setItem(footer_row, column, QTableWidgetItem(f"Total: {total}"))    
            if column==4 :
                for row in range(row_count):
                    
                    item = self.ui.tabla_usuarios.item(row, column)
                    if item is not None:
                        total += int(item.text())  # Sumar los valores

                # Añadiendo la suma total en la nueva fila
                self.ui.tabla_usuarios.setItem(footer_row, column, QTableWidgetItem(f"Total: {total}"))   
                
                
                
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
       # print(f"Actualizar fila11111111: {row[0]} {row[1]} {row[2]}")
        resportesUser= ResumenSesionUser(self, row[0],row[1],row[2])
        resportesUser.exec()
       

    def delete_row(self, row):
        id_juego = int(self.ui.tabla_usuarios.item(row, 0).text())
        # Eliminar la sesión
        confirmation = QMessageBox.question(self, 'Confirmar', '¿Estás seguro de que quieres borrar el Juego?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmation == QMessageBox.StandardButton.Yes:
            self.cursor.execute("DELETE FROM juego WHERE id_juego = ?", (id_juego,))
            self.conexion.commit()
            # Actualizar la tabla
            self.cargar_datos(self.op)

        
            
