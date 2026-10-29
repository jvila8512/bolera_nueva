import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize
class TableDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Establecer el título y tamaño del diálogo
        self.setWindowTitle("Tabla en Diálogo")
        self.setFixedSize(400, 300)

        # Establecer un layout vertical
        layout = QVBoxLayout()

        # Crear una tabla (QTableWidget)
        self.table = QTableWidget(5, 3)  # 5 filas y 3 columnas
        self.table.setHorizontalHeaderLabels(["Columna 1", "Columna 2", "Columna 3"])

        # Rellenar la tabla con datos de ejemplo
        for row in range(5):
            for column in range(3):
                item = QTableWidgetItem(f"Item {row}, {column}")
                self.table.setItem(row, column, item)

        # Añadir la tabla al layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    dialog = TableDialog()
    dialog.exec()