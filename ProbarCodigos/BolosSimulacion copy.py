import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear tabla
        self.table = QTableWidget(5, 3)  # 5 filas, 3 columnas
        self.table.setHorizontalHeaderLabels(["Columna 1", "Columna 2", "Columna 3"])
        for i in range(5):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"Fila {i + 1}, Columna {j + 1}"))

        # Crear botón
        self.button = QPushButton("Resaltar celda (0, 0)")
        self.button.clicked.connect(self.highlight_cell_0_0)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def highlight_cell_0_0(self):
        """
        Resalta los bordes de la celda en fila 0, columna 0 con color rojo.
        """
        # Restablecer el estilo de todas las celdas
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QBrush(QColor("white")))  # Fondo blanco
                    item.setForeground(QBrush(QColor("black")))  # Texto negro

        # Resaltar la celda específica (0, 0)
        item = self.table.item(0, 0)
        if item:
            item.setBackground(QBrush(QColor("white")))  # Fondo blanco
            item.setForeground(QBrush(QColor("black")))  # Texto negro
            # Aplicar un estilo CSS con bordes rojos
            self.table.setStyleSheet("""
                QTableWidget::item {
                    border: none;  /* Eliminar bordes predeterminados */
                }
                QTableWidget::item:selected {
                    border: 2px solid red; /* Bordes rojos para la celda resaltada */
                }
            """)


# Crear y ejecutar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
