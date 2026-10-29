import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QDateEdit, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import QDate

class SesionCRUD(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user  # Guardar el usuario si es necesario
        self.initUI()
        self.create_connection()
        self.load_data()

    def initUI(self):
        self.setWindowTitle("CRUD de Sesiones")
        layout = QVBoxLayout()

        # Filtros
        self.id_usuario_filter = QLineEdit(self)
        self.activa_filter = QLineEdit(self)
        self.fecha_filter = QDateEdit(self)
        self.fecha_filter.setDate(QDate.currentDate())
        
        layout.addWidget(QLabel("ID Usuario:"))
        layout.addWidget(self.id_usuario_filter)
        
        layout.addWidget(QLabel("Activa (1/0):"))
        layout.addWidget(self.activa_filter)

        layout.addWidget(QLabel("Fecha:"))
        layout.addWidget(self.fecha_filter)

        # Botón de buscar
        search_button = QPushButton("Buscar", self)
        search_button.clicked.connect(self.load_data)
        layout.addWidget(search_button)

        # Tabla
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Sesion", "ID Usuario", "Activa", "Fecha", "Acciones"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def create_connection(self):
        self.conn = sqlite3.connect('/bolera.db')  # Cambia el nombre de la base de datos según sea necesario
        self.cursor = self.conn.cursor()
      
        
        self.cursor.execute("INSERT INTO sesion (id_usuario,activa,fecha) VALUES (?,?,?)",(7,1,"2025-2-13,"))
        self.conn.commit()
        
        # Crear tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesion (
                id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                activa INTEGER,
                fecha TEXT
            )
        ''')
        self.conn.commit()

    def load_data(self):
        # Obtener filtros
        id_usuario = self.id_usuario_filter.text()
        activa = self.activa_filter.text()
        fecha = self.fecha_filter.date().toString("yyyy-MM-dd")

        query = "SELECT * FROM sesion  "
        params = []

      

        self.cursor.execute(query, params)
        
        rows = self.cursor.fetchall()

        self.table.setRowCount(0)
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            for column, data in enumerate(row[:-1]):  # Excluyendo el último campo para las acciones
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

            # Botón para activar/desactivar
            activa_button = QPushButton("Activar" if row[2] == 0 else "Desactivar")
            activa_button.clicked.connect(lambda checked, r=row: self.toggle_activa(r[0], row_position))
            self.table.setCellWidget(row_position, 2, activa_button)  # Columna de 'Activa'

            # Botones de actualizar y borrar
            action_layout = QHBoxLayout()
            update_button = QPushButton("Actualizar")
            update_button.clicked.connect(lambda checked, r=row: self.update_row(r))    
            delete_button = QPushButton("Borrar")
            delete_button.clicked.connect(lambda checked, r=row: self.delete_row(r[0]))

            action_layout.addWidget(update_button)
            action_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row_position, 4, action_widget)  # Columna de 'Acciones'

    def toggle_activa(self, id_sesion, row_position):
        # Cambiar el estado de 'activa'
        self.cursor.execute("SELECT activa FROM sesion WHERE id_sesion = ?", (id_sesion,))
        activa_value = self.cursor.fetchone()[0]
        
        new_value = 1 if activa_value == 0 else 0
        self.cursor.execute("UPDATE sesion SET activa = ? WHERE id_sesion = ?", (new_value, id_sesion))
        self.conn.commit()
        
        # Actualizar la tabla
        self.load_data()

    def update_row(self, row):
        # Aquí puedes implementar la lógica para actualizar la fila seleccionada
        print(f"Actualizar fila: {row}")

    def delete_row(self, id_sesion):
        # Eliminar la sesión
        confirmation = QMessageBox.question(self, 'Confirmar', '¿Estás seguro de que quieres borrar esta sesión?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmation == QMessageBox.StandardButton.Yes:
            self.cursor.execute("DELETE FROM sesion WHERE id_sesion = ?", (id_sesion,))
            self.conn.commit()
            self.load_data()

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SesionCRUD(None)  # Pasar el usuario si es necesario
    window.show()
    sys.exit(app.exec())
