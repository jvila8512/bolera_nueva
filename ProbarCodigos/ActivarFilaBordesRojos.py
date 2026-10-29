import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo de Tabla con Bordes")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.tabla = QTableWidget(self)
        self.tabla.setRowCount(4)
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Col 1", "Col 2", "Col 3", "Col 4"])  # Opcional: encabezados
        layout.addWidget(self.tabla)
        
        # Crear datos de ejemplo
        for row in range(4):
             for col in range (4):
                 item = QTableWidgetItem(f"Fila {row+1}, Col {col+1}")
                 item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                 self.tabla.setItem(row, col, item)

        boton_bordes_rojos = QPushButton("Bordes Rojos (Top/Bottom)", self)
        boton_bordes_rojos.clicked.connect(self.aplicar_bordes_rojos)
        layout.addWidget(boton_bordes_rojos)

        boton_restablecer_bordes = QPushButton("Restablecer Bordes", self)
        boton_restablecer_bordes.clicked.connect(self.restablecer_bordes)
        layout.addWidget(boton_restablecer_bordes)


        self.setCentralWidget(central_widget)


    def aplicar_bordes_rojos(self, fila_JugadorActivo):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada >= 0:
            for col in range(self.tabla.columnCount()):
                
                item = self.tabla.item(fila_seleccionada, col)
                if item:
                    item.setForeground(QColor("black")) # restablece el color del texto
                    
                    # Establece el borde superior rojo
                    self.tabla.setStyleSheet(f"""
                    QTableWidget::item {{
                        border-top: 2px solid red;
                        border-bottom: 2px solid red;
                    }}
                    QTableWidget::item:selected {{
                        border-top: 2px solid red;
                        border-bottom: 2px solid red;
                     }}
                   
                   
                    """)
                   
                    self.tabla.item(fila_seleccionada, col).setSelected(True) #selecciona la fila
    
    def restablecer_bordes(self):
        self.tabla.setStyleSheet("")

        for row in range(self.tabla.rowCount()):
             for col in range (self.tabla.columnCount()):
                 item = self.tabla.item(row, col)
                 if item:
                    item.setForeground(QColor("black")) # restablece el color del texto
        
        self.tabla.clearSelection()#deselecciona

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())