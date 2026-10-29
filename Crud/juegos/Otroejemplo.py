import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QComboBox, QPushButton, QDateEdit)

class JuegoDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Juegos")
        
        self.layout = QVBoxLayout()
        
        self.fecha_combo = QDateEdit()
        self.fecha_combo.setCalendarPopup(True)
        self.layout.addWidget(self.fecha_combo)
        
        self.filtrar_btn = QPushButton("Filtrar")
        self.filtrar_btn.clicked.connect(self.filtrar_por_fecha)
        self.layout.addWidget(self.filtrar_btn)
        
        self.juegos_table = QTableWidget()
        self.juegos_table.setColumnCount(10)  # Ajusta según las columnas que necesitas
        self.layout.addWidget(self.juegos_table)

        self.setLayout(self.layout)
        
        self.conectar_db()
        self.cargar_datos()

    def conectar_db(self):
        self.conn = sqlite3.connect('bolera.db')  # Cambia el nombre del archivo
        self.cursor = self.conn.cursor()

    def cargar_datos(self):
        self.cursor.execute("SELECT * FROM juego")
        rows = self.cursor.fetchall()
        self.juegos_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.juegos_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def filtrar_por_fecha(self):
        fecha = self.fecha_combo.date().toPyDate()
        self.cursor.execute("SELECT * FROM juego WHERE fecha = ?", (fecha,))
        rows = self.cursor.fetchall()
        self.juegos_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.juegos_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = JuegoDialog()
    dialog.show()
    sys.exit(app.exec())