import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog,QWidget, QTableWidget, QTableWidgetItem, QMessageBox,QHeaderView,QLabel,QPushButton,QHBoxLayout,QSizePolicy
from PyQt6.QtCore import Qt
from UI.precio import Precio
from ConexionBD.conexion import Conexion
from PyQt6.QtGui import QIcon,QDoubleValidator # Importa QIcon para usar iconos
import recursoAnimacion

import recursos
class CrudPrecio(QDialog):
    def __init__(self):
        super().__init__()
        # Initialize the UI from the generated 'main_ui' class
        self.ui = Precio()
        self.ui.setupUi(self)
        self.setWindowTitle("Formulario de Precio")
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))

         # Conectar a la base de datos  
        self.con = Conexion()       
        self.initGUI() 
                    
    def initGUI(self):
           
   
        self.ui.btnGuardar.clicked.connect(self.agregar_precio)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Precio","Acciones"])
       
        # Ocultar el encabezado vertical (numeración de filas)
        self.ui.tableWidget.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical        
        # Ocultar la primera columna
        self.ui.tableWidget.setColumnHidden(0, True)  # Oculta la columna con índice 0
        self.ui.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Desactivar la selección     
        self.ui.tableWidget.setSelectionMode(QTableWidget.SelectionMode.NoSelection)      

      
         # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
         # Aplicar estilos CSS
         # Aplicar un validador para permitir solo números y un decimal
        self.ui.precio.setValidator(QDoubleValidator(0.99, 99.99, 2))  # Permite hasta 2 decimales

         # Cargar los datos
        self.cargar_datos()

         # Aplicar CSS
        self.aplicar_estilos()

       

    def agregar_precio(self):
        # Obtener los datos de entrada
       
        precio = self.ui.precio.text()

        # Validar los datos
        if  not precio:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
            return
    
        # Conectar a la base de datos
        try:
            
            # Insertar el nuevo precio
           resultado= self.con.ejecutar_sql("INSERT INTO precio (precio) VALUES (?)", (precio,))
           print(resultado)

            # Mostrar mensaje de éxito
           QMessageBox.information(self, "Éxito", "Precio agregado correctamente.")

            # Limpiar los campos           
           self.ui.precio.clear()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el precio: {e}")
        self.cargar_datos()
       

    def cargar_datos(self):
        
               # Obtener los datos de la tabla User
        usuarios= self.con.ejecutar_sql("SELECT * FROM precio ORDER BY precio ASC")
        # Configurar el número de filas
        self.ui.tableWidget.setRowCount(len(usuarios))

        # Rellenar el QTableWidget con los datos
        for row_index, row_data in enumerate(usuarios):
            for column_index, item in enumerate(row_data):
                   if column_index==1  :
                    precio_float = float(item)
                    precio_formateado = f"${precio_float:,.2f}"  # Formatear como $ 54.00
                    table_item = QTableWidgetItem( str(precio_formateado))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  
                    self.ui.tableWidget.setItem(row_index, column_index, table_item )
                   else:
                    table_item = QTableWidgetItem( str(item))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  
                    self.ui.tableWidget.setItem(row_index, column_index, table_item )
                
                

            # Crear los botones de Editar y Borrar
            btn_editar = QPushButton()
            btn_borrar = QPushButton()
              # Establecer íconos para los botones
            btn_editar.setIcon(QIcon(":/animacion/iconos/update.svg"))  # Cambia esta ruta a la de tu icono
            btn_borrar.setIcon(QIcon(":/animacion/iconos/delete.svg"))  # Cambia esta ruta a la de tu icono

           
            # Conectar las señales de los botones a sus respectivas funciones
            btn_editar.clicked.connect(lambda checked, row=row_index: self.editar_usuario(row))
            btn_borrar.clicked.connect(lambda checked, row=row_index: self.borrar_precio(row))

          # Ajustar el tamaño de los botones
            btn_editar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            btn_borrar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
           # button_layout.addWidget(btn_editar)
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
            self.ui.tableWidget.setCellWidget(row_index, 2, button_widget ) # Columna de Acciones
            #self.ui.tableWidget.setColumnWidth(6, 30)  # Cambia 150 al tamaño que desees

         # Establecer un tamaño fijo para la última columna (índice 6)
        
          # Ajustar el tamaño de las columnas
        #self.ui.tableWidget.resizeColumnsToContents()
        # Cerrar la conexión
        
        
        
    def aplicar_estilos(self):
       
        self.ui.tableWidget.setStyleSheet("""
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

    def borrar_precio(self, row):
        # Aquí puedes implementar la lógica para borrar el usuario
        #QMessageBox.information(self, "Borrar Usuario", f"Borrar usuario en la fila {row}")
        #print(self.ui.tableWidget.item(row, 0).text())
        id = int(self.ui.tableWidget.item(row, 0).text())
        #precio = float(self.ui.tableWidget.item(row, 1).text())
      
         # Crea un mensaje de confirmación
    
                
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Confirmación de Eliminación")
        msgBox.setText(f"¿Está seguro de que desea borrar el precio?")
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
            self.con.ejecutar_sql("DELETE FROM precio WHERE id_precio = ?", (id,))
            self.cargar_datos()
               

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CrudPrecio()
    ventana.show()
    sys.exit(app.exec())