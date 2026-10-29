import sys
import sqlite3
from PyQt6 import QtWidgets, QtGui, QtCore

class JuegoDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Juegos")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QtWidgets.QVBoxLayout()

        # Combo box para seleccionar fecha
        self.fecha_combo = QtWidgets.QComboBox()
        self.fecha_combo.currentIndexChanged.connect(self.filtrar_por_fecha)
        self.layout.addWidget(self.fecha_combo)

        # Tabla para mostrar los juegos
        self.tabla_juegos = QtWidgets.QTableWidget()
        self.tabla_juegos.setColumnCount(7)  # Ajusta el número de columnas según sea necesario
        self.tabla_juegos.setHorizontalHeaderLabels(["ID", "Fecha", "Usuario", "Precio", "Tipo", "Jugadores", "Activo"])
        self.layout.addWidget(self.tabla_juegos)

        # Botones de paginación
        self.boton_anterior = QtWidgets.QPushButton("Anterior")
        self.boton_siguiente = QtWidgets.QPushButton("Siguiente")
        self.boton_anterior.clicked.connect(self.pagina_anterior)
        self.boton_siguiente.clicked.connect(self.pagina_siguiente)

        self.layout.addWidget(self.boton_anterior)
        self.layout.addWidget(self.boton_siguiente)

        self.setLayout(self.layout)

        self.conexion = sqlite3.connect('bolera.db')
        self.cargar_fechas()
        
        # Inicialización de variables de paginación
        self.pagina_actual = 0
        self.registros_por_pagina = 10  # Asegúrate de que esta línea esté aquí
        self.cargar_juegos()

    def cargar_fechas(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT DISTINCT fecha FROM juego ORDER BY fecha")
        fechas = cursor.fetchall()
        for fecha in fechas:
            self.fecha_combo.addItem(fecha[0])
        cursor.close()

    def filtrar_por_fecha(self):
        self.pagina_actual = 0
        self.cargar_juegos()

    def cargar_juegos(self):
        fecha_seleccionada = self.fecha_combo.currentText()
        cursor = self.conexion.cursor()
        
        if fecha_seleccionada:
            cursor.execute("SELECT * FROM juego WHERE fecha = ? LIMIT ?, ?", 
                           (fecha_seleccionada, self.pagina_actual * 10, 10))
        else:
            cursor.execute("SELECT * FROM juego LIMIT ?, ?", 
                           (self.pagina_actual * 10, 10))

        juegos = cursor.fetchall()
        self.tabla_juegos.setRowCount(0)
        for juego in juegos:
            row_position = self.tabla_juegos.rowCount()
            self.tabla_juegos.insertRow(row_position)
            for column, data in enumerate(juego):
                self.tabla_juegos.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()

    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.cargar_juegos()

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.cargar_juegos()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialogo = JuegoDialog()
    dialogo.exec()