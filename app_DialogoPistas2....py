import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog,QApplication,QWidget,QHeaderView, QTableWidgetItem,QSizePolicy, QTableWidget, QPushButton, QLineEdit, QCheckBox,  QHBoxLayout, QMessageBox
from ConexionBD.conexion import Conexion
from ConexionBD.juego_Operaciones import JuegoBD_operaciones
from app_pista1Resultado import Pista1Resultado
from app_pista2Resultado import Pista2Resultado
from bd_modelos.usuario import Usuario
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
from PyQt6.QtCore import Qt,QDateTime,pyqtSignal
from dasboard import DasBoard
from bd_modelos import Sesion


import recursos
     
from UI.pistasDialog2 import Pistas_Dialog

 
          
import recursos 
           
class AdminPistas2(QDialog):
     enviar_datos1 = pyqtSignal(int, str) # Señal para enviar datos
     def __init__(self, parent,user:Usuario,dasBoard: DasBoard,sesion:Sesion):
        super().__init__()
         
         # Initialize the UI from the generated 'main_ui' class
        self.ui = Pistas_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))        
       
        self.setWindowTitle("Gestión Pista 2")
        # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones()
         # Conectar a la base de datos  
        self.con = Conexion()  
        self.UserLogueado = user
        self.Sesion= sesion
        # Referencia a mi ventana app_Gestion de pistas para poder cerrar mi Resultados
        self.appGestionPistas=parent
        
       # colocar los jugadores
        #self.ui.combo_CanJugadores.addItem("1", 1)
        #self.ui.combo_CanJugadores.addItem("2", 2)
        #self.ui.combo_CanJugadores.addItem("3", 3) 
        #self.ui.combo_CanJugadores.addItem("4", 4) 
        #self.ui.combo_CanJugadores.addItem("5", 5) 
        #self.ui.combo_CanJugadores.addItem("6", 6) 
        
        self.dasBodar=dasBoard
           # Recuperar los Tipo de Juego
        tipo_juego = self.con.ejecutar_sql("SELECT * FROM tipo_juego")
          # Llenar el QComboBox
        
        for tipo in tipo_juego :
            self.ui.combo_TipoJuego.addItem(tipo[1], tipo[0])  # Agregamos el nombre y el ID como datos del item
          
             # Recuperar los Precio de Juego
        precio = self.con.ejecutar_sql("SELECT * FROM precio")
          # Llenar el QComboBox
        
        for tipo in precio :
            nombre_precio = str(tipo[1]) # El precio se convierte a cadena
            self.ui.combo_Precio.addItem(nombre_precio, tipo[0])  # Agregamos el nombre y el ID como datos del item  
       
        # Recuperar los Tiempo de Juego
        tiempoJuego = self.con.ejecutar_sql("SELECT * FROM tiempo_juego")
          # Llenar el QComboBox
        
        for tipo in  tiempoJuego :
           # tiempo = str(tipo[1])+" minutos"   # El tiempo se convierte a cadena
            tiempo = str(tipo[1])   # El tiempo se convierte a cadena
            self.ui.combo_TiempoJuego.addItem(tiempo, tipo[0])  # Agregamos el nombre y el ID como datos del item  
            
        
        self.pagar()
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        
        
        self.ui.tablaJugadores.setHorizontalHeaderLabels([ "Nombre", "Menor de Edad", "Acciones"])  
          # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.ui.tablaJugadores.horizontalHeader().setStretchLastSection(True)
        self.ui.tablaJugadores.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Habilitar la selección de toda la fila
        self.ui.tablaJugadores.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.ui.tablaJugadores.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
          # Contador de jugadores
        self.contadorJugadores = 0
        self.listaJugadores = []  # Lista para almacenar los registros
        self.current_index = 0 #variable para guardar el índice actual.
        self.initGUI() 
          # Apply styles
        self.apply_styles()
                    
     def initGUI(self):
       self.ui.btn_addJugador.clicked.connect(self.adicionarJugador)
       self.ui.comenzar.clicked.connect(self.Jugar)
       self.ui.btn_Cancelar_juego.clicked.connect(self.close)
        # Conectar la señal de cambio de jugadores
       self.ui.combo_CanJugadores.currentIndexChanged.connect(self.opcion_seleccionada)
       self.ui.combo_Precio.currentIndexChanged.connect(self.pagar)
       self.ui.combo_TipoJuego.currentIndexChanged.connect(self.cambiarTipoJuego)

    
     def cambiarTipoJuego(self):
        # Obtener el texto de la opción seleccionada
       tipoJuego = self.ui.combo_TipoJuego.currentText()     
      
       if(tipoJuego == "Torneo"):
          self.ui.pagar_Cant_jugadores.setText(" 0")
          self.ui.pagar_precio.setText("0")
          self.ui.pagar_Total.setText("0")
       else:
          self.pagar()  

     def pagar(self):
        tipo_juego= self.ui.combo_TipoJuego.currentText()
        id_tipo_juego=  self.ui.combo_TipoJuego.currentData() # Obtener el ID del rol seleccionado
        precio=self.ui.combo_Precio.currentText()
        id_tiempo= self.ui.combo_TiempoJuego.currentData()
        canJugadoresCombo=int(self.ui.combo_CanJugadores.currentText())
       
        if(tipo_juego == "Normal"):
          preciocon=float(precio)*canJugadoresCombo
          self.ui.pagar_Cant_jugadores.setText(""+str(canJugadoresCombo))
          self.ui.pagar_precio.setText(""+precio)
          self.ui.pagar_Total.setText("= "+str(preciocon))
        
      
       
     def opcion_seleccionada(self, index):
        # Obtener el texto de la opción seleccionada
       canJudadores = int(self.ui.combo_CanJugadores.currentText())
      
    
       if(canJudadores < len(self.listaJugadores)):
         self.ui.combo_CanJugadores.setCurrentIndex(len(self.listaJugadores)-1)
         msgBox = QMessageBox(self)
         msgBox.setWindowTitle("Confirmación")         
         msgBox.setText(f"Cantidad de Jugadores menor a los que estan registrados. Debe selecionar un opción válida. ¿Desea borrar la lista de jugadores?")
         msgBox.setIcon(QMessageBox.Icon.Question)
         msgBox.setStandardButtons( QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)          
                # Obtén el botón "Yes"
         boton_si = msgBox.button(QMessageBox.StandardButton.Yes)
         # Cambia el texto del botón a "Sí"
         boton_si.setText("Sí")
        
        
     
        # Obtén el botón "No"
         #boton_no = msgBox.button(QMessageBox.StandardButton.No)
        # Deja el texto del botón "No" como está (opcional)
        # boton_no.setText("No")       
    
        # Muestra el mensaje y obtiene la respuesta
         respuesta = msgBox.exec()
        
        # Si el usuario confirma (clickea en 'Yes')
         if respuesta == QMessageBox.StandardButton.Yes:
           self.listaJugadores.clear()
           self.update_table()
           
         
              
       else:
          if(canJudadores == len(self.listaJugadores)):
               self.ui.groupBox_2.setEnabled(False)
          else:
             self.ui.groupBox_2.setEnabled(True)
             self.pagar()
              
       
     def update_table(self):
        self.ui.tablaJugadores.setRowCount(len(self.listaJugadores))
        for row, (name, is_minor) in enumerate(self.listaJugadores):
            op=  QTableWidgetItem("Sí" if is_minor else "No")
            op.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  
             
            self.ui.tablaJugadores.setItem(row, 0, QTableWidgetItem(name))
            self.ui.tablaJugadores.setItem(row, 1,op)
          
          
             
              # Crear los botones de Editar y Borrar
            edit_button = QPushButton()
            delete_button = QPushButton()
              # Establecer íconos para los botones
            edit_button.setIcon(QIcon(":animacion/iconos/update.svg"))  # Cambia esta ruta a la de tu icono
            delete_button.setIcon(QIcon(":animacion/iconos/delete.svg"))  # Cambia esta ruta a la de tu icono
            
           
            edit_button.clicked.connect(lambda checked, row=row: self.edit_entry(row))
           

          
            delete_button.clicked.connect(lambda checked, row=row: self.delete_entry(row))
          
            
              # Ajustar el tamaño de los botones
            delete_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            edit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

           # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
           # button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.addStretch(1)  # Espacio a la derecha
              # Establecer el alineamiento del layout al centro
            # button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Establecer márgenes para el layout de los botones
            button_layout.setContentsMargins(10, 2, 10, 20)  # (izquierda, arriba, derecha, abajo)
        # Crear un QWidget para contener el layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
              # Establecer un tamaño mínimo para el QWidget que contiene los botones
            button_widget.setMinimumHeight(50)  # Ajusta la altura mínima según sea necesario
        # Añadir los botones a la tabla en la columna de acciones            
            
            
            self.ui.tablaJugadores.setCellWidget(row, 2,button_widget)
            self.actualizarEncabezadosVerticales()  
          
     def adicionarJugador(self): 
          canJudadores = int(self.ui.combo_CanJugadores.currentText())        
        
           # Incrementamos el contador de jugadores
          self.contadorJugadores += 1 
          name = self.ui.lineEdit.text().strip()
          is_menor = self.ui.checkBox.isChecked()
        
          if name:
            
            self.listaJugadores.append((name, is_menor))           
            
           
            self.update_table()
                 
   
           
           
      
        
            if(canJudadores == len(self.listaJugadores)):
                  self.ui.groupBox_2.setEnabled(False)
            else:
                  self.ui.groupBox_2.setEnabled(True)
            self.ui.lineEdit.clear()
            self.ui.checkBox.setChecked(False)
          else:
              QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un nombre.")
              
              
     def actualizarEncabezadosVerticales(self):
        # Creamos una lista de encabezados
        jugadores = [f'Jugador {i+1}' for i in range(self.contadorJugadores)]
        self.ui.tablaJugadores.setVerticalHeaderLabels(jugadores)  
        
     def Jugar(self):

           # Obtener información sobre las pantallas para validacion de enviar video al TV 1
          screen_count = QApplication.screens()

          # Comprobar que hay suficientes pantallas conectadas.
          if len(screen_count) < 3:
                # Crear un mensaje de diálogo
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Información")
                msg_box.setText("Revise la salida de video del Televisor 2.")
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.exec()
                return

          tipo_juego= self.ui.combo_TipoJuego.currentText()
          id_tipo_juego=  self.ui.combo_TipoJuego.currentData() # Obtener el ID del rol seleccionado
          id_precio=self.ui.combo_Precio.currentData()
          id_tiempo= self.ui.combo_TiempoJuego.currentData()   
          tiempoSegundos=int(self.ui.combo_TiempoJuego.currentText())
          canJugadoresCombo=int(self.ui.combo_CanJugadores.currentText())
          cantidadSegundos=tiempoSegundos*canJugadoresCombo*60
    
          if not self.listaJugadores:  # Verifica si el arreglo está vacío
              msgBox = QMessageBox(self)
              msgBox.setWindowTitle("Información")         
              msgBox.setText("Debe llenar la lista de jugadores.")
              msgBox.setIcon(QMessageBox.Icon.Information)
              msgBox.exec()
          else: 
              # Obtener la fecha y hora actual
              current_datetime = QDateTime.currentDateTime()
              datetime_str = current_datetime.toString("yyyy-MM-dd HH:mm:ss")       
            
            # Insertamos el juego
              parametros=(id_tiempo,datetime_str, self.Sesion.id_sesion,id_precio,id_tipo_juego,1,len(self.listaJugadores),1,cantidadSegundos)
              ultimo_id = self.juegoBD_operaciones.insertarJuego(parametros, self.listaJugadores,1)
                
               # Obtener la segunda pantalla Cambiaraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa a 2
              tercera_pantalla = screen_count[2]
              # self.sub_window11=CarruselFotos()cf
              #cantidadSegundos
              # Mostrar el diálogo cantidadSegundos
              self.pista1=Pista2Resultado(self,ultimo_id,cantidadSegundos,tercera_pantalla,  self.appGestionPistas)
              # Calcular la posición de la segunda pantalla
              screen_geometry = tercera_pantalla.geometry()
              self.pista1.setGeometry(screen_geometry.x() + 100, screen_geometry.y() + 100, 300, 100)
              #asignamos la referencia a la ventana principal para que cdo se cierre tambien se cierre
              self.pista1.showFullScreen()
              self.dasBodar.ventana_ResultadosPista2=self.pista1    
              self.appGestionPistas.ventana_ResultadosPista2=self.pista1  
              dato2 = "123" #Reemplaza con tu lógica para obtener dato2
              self.enviar_datos1.emit(ultimo_id, dato2)  # Emitir la señal con los datos
              self.close()  # Cierra la ventana secundaria
        
        
       
       
       
          
     def delete_entry(self, row):
        del self.listaJugadores[row]
        self.update_table()
        self.contadorJugadores=self.contadorJugadores-1
        if(self.contadorJugadores== self.listaJugadores.__len__):
                self.ui.groupBox_2.setEnabled(False)
        else:
                self.ui.groupBox_2.setEnabled(True)
       
                
                
     def apply_styles(self): 
       
           # CSS para la tabla
           self.ui.tablaJugadores.setStyleSheet("""
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

          