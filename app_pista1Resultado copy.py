import sys
from PyQt6.QtWidgets import QApplication,QDialog, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QLabel,QHeaderView,QSizePolicy,QTableWidget

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from UI.pista1Resultado import Pista1_Resultad
from ConexionBD.juego_Operaciones import JuegoBD_operaciones


class Pista1Resultado(QDialog):
     def __init__(self, id_juego):
        super().__init__()         
         # Initialize the UI from the generated 'main_ui' class
        self.ui = Pista1_Resultad()      
        self.ui.setupUi(self)    
        self.id_juego=id_juego
        # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones()    
        self.table=self.ui.tabla_resultado
       
        self.table.setColumnCount(11)  # 11 columnas        
        # Ajustar el estilo del encabezado
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { height: 40px; }")  # Aumentar la altura del encabezado
        self.table.setHorizontalHeaderLabels(["1", "2", "3","4", "5","6","7","8", "9", "10", "Total"])
        # Quitar las líneas verticales
        #self.table.setStyleSheet("QTableWidget { border: none; }")  # Sin bordes en la tabla
        #self.table.setShowGrid(False)  # Quitar la cuadrícula
        # Configurar el diálogo para que no tenga bordes
        # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
      
         # Ajustar la altura de la fila al contenido
         # Mostrar el diálogo maximizado
        self.showMaximized()
        self.mostrarDatosTabla()
        # Aplicar estilo CSS para mostrar solo las líneas de las columnas
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;  /* Sin borde alrededor de la tabla */
            }
            QTableWidget::item {
           
                border: none;  /* Sin borde alrededor de los elementos */
            
                 border-right: 1px solid black;  
                 border-bottom: 1px solid black;        
            }
            QHeaderView::section {
                border: 1px solid transparent;  /* Borde para las secciones del encabezado */
            }
            QTableWidget::verticalHeader {
                border: 1px solid red;  /* Sin borde en el encabezado vertical */
            }
            QTableWidget::horizontalHeader {
                border: 1px solid green;  /* Borde para el encabezado horizontal */
            }
            QTableWidget::item:selected {
                background-color: lightblue;  /* Color de fondo para elementos seleccionados */
            }
        """)
        
     
     
     
     
     def mostrarDatosTabla(self):
         datos=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego)
         self.table.setRowCount(len(datos)) 
         if datos:
           for jugador in datos:
            # print(f"Jugador: {jugador['nombre']}")
             for tiro in jugador['tiros']:
               print(f"  Tiro {tiro['numero_tiro']}: Op1={tiro['op1']}, Op2={tiro['op2']}, Op3={tiro['op3']}")
         else:
          print("No se pudieron obtener los datos de los jugadores.")
        
         for row in range(6): 
              
          for col in range(10):
            # Solo una fila
            # Crear un widget para la celda
            cell_widget = QWidget()        
            
            # Crear el layout vertical
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 2, 0)  # (izquierda, arriba, derecha, abajo)
            main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

            # Crear un layout horizontal para los dos labels de arriba
            top_layout = QHBoxLayout()
            top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
            top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

          # Crear los dos labels de arriba
            label1 = QLabel("10")
            label1.setStyleSheet("background-color: lightgray;font-size: 25px;")  # Color de fondo para visualizar mejor
            label2 = QLabel("X")
           
            label2.setStyleSheet("background-color: #FFFFFF;font-size: 25px;")  # Color de fondo para visualizar mejor
            #label2.setStyleSheet("background-color: lightgray;")  # Color de fondo para visualizar mejor
            label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Añadir un poco de espacio entre los labels
            top_layout.addWidget(label1)
            top_layout.addSpacing(0)  # Espacio de 20 píxeles
            top_layout.addWidget(label2)

            # Añadir el layout horizontal al layout principal
            main_layout.addLayout(top_layout)

            # Crear el label de abajo que ocupa el espacio de los dos de arriba
            label3 = QLabel("200")
            label3.setStyleSheet("background-color: lightgray; lightgray;font-size: 30px;")  # Color de fondo para visualizar mejor
            label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
           
            main_layout.addWidget(label3)  
            
            
          

            # Establecer el layout en el widget de la celda
            cell_widget.setLayout(main_layout)
             # Establecer un tamaño fijo para el widget de la celda
            cell_widget.setFixedSize(100, 132)  # Ancho 150, Alto 100

            # Añadir el widget a la celda de la tabla
            self.table.setCellWidget(row, col, cell_widget)
          
             # La columna 11 (índice 10) se deja vacía o se puede rellenar como desees
           # self.table.setItem(0, 10, QTableWidgetItem("Columna 11 vacía"))  # Columna 11
          # Ajustar el tamaño de las columnas al contenido
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            # La columna 11 (índice 10) se deja vacía o se puede rellenar como desees
          self.table.setItem(row, 10, QTableWidgetItem("Columna 11 vacía"))  # Columna 11
       
           
        
            # self.table.verticalHeader().setSectionResizeMode(row, QHeaderView.ResizeMode.ResizeToContents)  # Opción para ajustar automáticamente
# Ajusta este valor según necesites
         self.table.resizeRowToContents(row)
        
          # Crear una lista de encabezados
         jugadores = [f'Jugador {i+1}' for i in range(6)]
        
         # Cambiar el tipo de letra y el tamaño para los encabezados de la tabla
         font = QFont("Arial", 24)  # Cambia "Arial" y 16 por el tipo y tamaño que desees
         self.table.verticalHeader().setFont(font)
         self.table.setVerticalHeaderLabels(jugadores)
         
        
        #self.table.verticalHeader().setFixedSize(100, 120)
         # Establecer un tamaño fijo para el encabezado vertical
         # Esto establece la altura del encabezado vertical

        #self.table.verticalHeader().setDefaultSectionSize(97)  # Establecer la altura fija
        # Establecer los encabezados verticales
       
        
         # Aplicar estilo CSS al encabezado vertical
         self.table.verticalHeader().setStyleSheet("QHeaderView::section {"
                                                      "font-size: 24px;"  # Tamaño de fuente
                                                      "text-align: center;"  # Centrar texto
                                                      "background-color: lightgray;"  # Color de fondo (opcional)
                                                      " border: none; "
                                                      "}")
         
        
         for row in range(6):
               
               self.table.setRowHeight(row, 125)
              # self.table.verticalHeader().setDefaultSectionSize(200)
               #self.table.verticalHeader().setSectionResizeMode(row, QHeaderView.ResizeMode.ResizeToContents)  # Opción para ajustar automáticamente
               # Establecer un tamaño fijo para cada sección del encabezado vertical
      
           
          

        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window =Pista1Resultado(7)
    window.show()
    sys.exit(app.exec())