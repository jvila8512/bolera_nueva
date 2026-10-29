
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,QAbstractItemView,QHeaderView
from UI.resultado import ResultadoFinal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont,QColor,QBrush
from ConexionBD.juego_Operaciones import JuegoBD_operaciones


from bd_modelos.juego_bolos import JuegoBolos

class ResultadoFinalWindow(QWidget):
    def __init__(self, resultados):
        super().__init__()             
         # Initialize the UI from the generated 'main_ui' class
        self.ui = ResultadoFinal()      
        self.ui.setupUi(self)
        self.table=self.ui.tabla
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Mostrar el diálogo maximizado
        self.showMaximized()

        columnas = ['Jugador']
        columnas.append("Puntuación Total") #Agregamos la columna de puntuacion total
        self.table.setColumnCount(len(columnas))
        self.table.setHorizontalHeaderLabels(columnas)
        self.table.setRowCount(len(resultados))
        
        if len(resultados)<=  2:
           for _ in range(2):  # Agregar 2 filas
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            
            
         #Aplicar estilos en los encabezados de la fila 
         # Personalización de cada encabezado de columna
        font = QFont("Arial", 20, QFont.Weight.Bold) #Fuente Arial, tamaño 12, negritacd.

        for i in range(len(columnas)):
           
                item = QTableWidgetItem(columnas[i])               
                item.setFont(font) #Aplicando la fuente personalizada
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión
                item.setForeground(QColor(255, 255, 255)) 
                self.table.setHorizontalHeaderItem(i, item)   

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
         # Ajustar el estilo del encabezado
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { height: 55px;  background-color: #00007f; }")  # Aumentar la altura del encabezado
         # Quitar las líneas verticales
        self.table.setStyleSheet("QTableWidget { border: none; }")  # Sin bordes en la tabla
       # self.table.setShowGrid(False)  # Quitar la cuadrícula
        self.table.verticalHeader().setDefaultSectionSize(110)
         #Este es el truco para distribuir uniformemente las filas
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
         # Ocultar el encabezado vertical (numeración de filas)
        self.table.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical
         # Desactivar la selección
     
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        print(f"Resultados: {len(resultados)}") 
       
        for fila, jugador in enumerate(resultados):
                print(f"Nombre: {jugador['nombre']}, Puntuación: {jugador['puntuacion']} + {fila}")
       
                #print(resultado)
                nombre_item = QTableWidgetItem(jugador['nombre'])
                nombre_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                nombre_item.setBackground(QColor(0, 85, 255)) #Color en RGB para mas precisión           
                fontNombre = QFont()
                fontNombre.setPointSize(21)  # Tamaño de letra
                fontNombre.setBold(True) #opcional si quieres negrita              
                nombre_item.setFont(fontNombre)
                nombre_item.setForeground(QColor(255, 255, 255)) 
                self.table.setItem(fila, 0, nombre_item)  
                puntuacion = QTableWidgetItem(str(jugador['puntuacion']))
                puntuacion.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                puntuacion.setBackground(QColor(0, 85, 255)) #Color en RGB para mas precisión           
                fontNombre = QFont()
                puntuacion.setForeground(QColor(255, 255, 255)) 
                fontNombre.setPointSize(21)  # Tamaño de letra
                fontNombre.setBold(True) #opcional si quieres negrita   
                      
                puntuacion.setFont(fontNombre)
                self.table.setItem(fila, 1, puntuacion)  
        
        
        
       

       

if __name__ == "__main__":
        app = QApplication(sys.argv)
        juegoBD_operaciones=JuegoBD_operaciones()
      #obtengo los datos de la BD
        jugadores=juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(143)
       #obtener de la clase Bolos la calificacion segun los datos
        # Inicializar el juego de bolos
        juego = JuegoBolos(jugadores)
        resultados = juego.calcular_puntuacion() 

        ventana = ResultadoFinalWindow(sorted(resultados, key=lambda x: x['puntuacion'], reverse=True))
     
        ventana.show()

        sys.exit(app.exec())