
import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QTimer

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_data(self):
        query = """
        SELECT j.nombre FROM jugadores j
        JOIN tiros t ON j.id = t.id_jugadores
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

class ScoreDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resultados de Tiros")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.update_table)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        # Configurar la base de datos
        self.db = Database("./bolera.db")
        
        # Actualizar la tabla cada 5 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(5000)  # 5000 ms = 5 segundos

        # Inicializar la tabla
        self.update_table()

    def update_table(self):
        data = self.db.get_data()
        if data:
            self.table.setRowCount(len(data))
            self.table.setColumnCount(11)  # 1 para el nombre y 10 para los tiros
            self.table.setHorizontalHeaderLabels(["Jugador", "Tiro 1", "Tiro 2", "Tiro 3", "Tiro 4", "Tiro 5",
                                                   "Tiro 6", "Tiro 7", "Tiro 8", "Tiro 9", "Tiro 10"])

            for i, row in enumerate(data):
                self.table.setItem(i, 0, QTableWidgetItem(row[0]))  # Nombre del jugador
                for j in range(10):
                    self.table.setItem(i, j + 1, QTableWidgetItem(str(row[j + 1])))  # Tiros

        self.table.resizeColumnsToContents()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ScoreDialog()
    dialog.show()
    sys.exit(app.exec())