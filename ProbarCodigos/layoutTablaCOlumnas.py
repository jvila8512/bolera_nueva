
import sys
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Crear la tabla
        self.table = QTableWidget(4, 3)  # 4 filas y 3 columnas

        # Crear una lista de encabezados
        jugadores = [f'Jugador {i + 1}' for i in range(4)]

        # Cambiar el tipo de letra y el tamaño para los encabezados de la tabla
        font = QFont("Arial", 16)  # Cambia "Arial" y 16 por el tipo y tamaño que desees
        self.table.verticalHeader().setFont(font)

        # Establecer los encabezados verticales
        self.table.setVerticalHeaderLabels(jugadores)

        # Aplicar estilo CSS al encabezado vertical
        self.table.verticalHeader().setStyleSheet("""
            QHeaderView::section {
                font-size: 16px;  /* Tamaño de fuente */
                text-align: center;  /* Centrar texto */
                background-color: lightgray;  /* Color de fondo (opcional) */
                padding: 10px;  /* Espacio interno */
            }
        """)

        # Establecer un tamaño fijo para las filas
        row_height = 120  # Altura fija para las filas
        self.table.setRowHeight(0, row_height)
        self.table.setRowHeight(1, row_height)
        self.table.setRowHeight(2, row_height)
        self.table.setRowHeight(3, row_height)

        # Establecer un tamaño fijo para el encabezado vertical
        self.table.verticalHeader().setFixedHeight(row_height)  # Esto establece la altura del encabezado vertical

        # Agregar algunos datos de ejemplo
        for i in range(4):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f'Dato {i + 1},{j + 1}'))

        # Crear un layout horizontal para los labels
        label_layout = QHBoxLayout()

        # Crear y añadir QLabel para cada jugador
        for jugador in jugadores:
            label = QLabel(jugador)
            label.setFont(font)
            label_layout.addWidget(label)

        # Configurar el layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(label_layout)  # Agregar los labels al layout principal
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())