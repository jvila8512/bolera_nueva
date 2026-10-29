import sys
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QLabel,QHeaderView,QSizePolicy
from PyQt6.QtCore import Qt
class MyTable(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.table.setRowCount(10) 
        self.table.setColumnCount(11)  # 10 columnas
        
                # Ajustar el estilo del encabezado
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { height: 40px; }")  # Aumentar la altura del encabezado
        self.table.setHorizontalHeaderLabels(["1", "2", "3","4", "5","6","7","8", "9", "10", "Total"])
        # Quitar las líneas verticales
        self.table.setStyleSheet("QTableWidget { border: none; }")  # Sin bordes en la tabla
        self.table.setShowGrid(True)  # Quitar la cuadrícula

        
        for row in range(2):      
          for col in range(10):
            # Solo una fila
            # Crear un widget para la celda
            cell_widget = QWidget()
            
            
                # Crear el layout vertical
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
            main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

            # Crear un layout horizontal para los dos labels de arriba
            top_layout = QHBoxLayout()
            top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
            top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

          # Crear los dos labels de arriba
            label1 = QLabel("10")
            label1.setStyleSheet("background-color: lightgray;font-size: 25px;")  # Color de fondo para visualizar mejor
            label2 = QLabel("X")
           
            label2.setStyleSheet("background-color: lightgray;font-size: 25px;")  # Color de fondo para visualizar mejor
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
            cell_widget.setFixedSize(111, 150)  # Ancho 150, Alto 100

            # Añadir el widget a la celda de la tabla
            self.table.setCellWidget(row, col, cell_widget)
          
             # La columna 11 (índice 10) se deja vacía o se puede rellenar como desees
           # self.table.setItem(0, 10, QTableWidgetItem("Columna 11 vacía"))  # Columna 11
          # Ajustar el tamaño de las columnas al contenido
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            # La columna 11 (índice 10) se deja vacía o se puede rellenar como desees
          self.table.setItem(row, 10, QTableWidgetItem("Columna 11 vacía"))  # Columna 11
        for row in range(10):
             self.table.setRowHeight(row, 180)  # Ajusta este valor según necesites
        self.table.resizeRowToContents(row)
         # Aumentar la altura de la fila para crear separación
         # Establecer la tabla en el layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
         # Ajustar la altura de la fila al contenido
       
          # Habilitar la selección de toda la fila
       # self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
       # self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setWindowTitle("Tabla con Layouts en Celdas")
        self.resize(800, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyTable()
    window.show()
    sys.exit(app.exec())