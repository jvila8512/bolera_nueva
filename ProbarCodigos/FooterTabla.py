from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.table_widget = QTableWidget(5, 3)  # 5 filas, 3 columnas
        self.set_data()
        self.add_column_footer()
        
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def set_data(self):
        # Añadiendo datos a la tabla
        for row in range(5):
            for column in range(3):
                self.table_widget.setItem(row, column, QTableWidgetItem(f"{row * 10 + column}"))

    def add_column_footer(self):
        # Calculando la suma de cada columna y añadiéndola como fila de pie de columna
        row_count = self.table_widget.rowCount()
        column_count = self.table_widget.columnCount()
        
        footer_row = row_count  # Row where the footer will be added

        self.table_widget.insertRow(footer_row)  # Insertar una nueva fila

        for column in range(column_count):
            total = 0
            for row in range(row_count):
                item = self.table_widget.item(row, column)
                if item is not None:
                    total += int(item.text())  # Sumar los valores

            # Añadiendo la suma total en la nueva fila
            self.table_widget.setItem(footer_row, column, QTableWidgetItem(f"Total: {total}"))

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()