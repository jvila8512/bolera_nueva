import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt,QDate
from pyreportjasper import PyReportJasper
import datetime
import os
from ConexionBD.juego_Operaciones import JuegoBD_operaciones
import json

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reporte con PyReportJasper")
        self.setGeometry(200, 200, 400, 200)  # (x, y, ancho, alto)

        layout = QVBoxLayout()
       # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones()
        parametros=(23,"2024-12-27" )  # Año, mes, día
        self.juegos_user=  self.juegoBD_operaciones.obtenerJuegosUserporFecha(parametros)
        datos= self.convertir_a_json(self.juegos_user)
        print( datos)
       

        self.label = QLabel("Presiona el botón para generar el reporte")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        boton_generar = QPushButton("Generar Reporte")
        boton_generar.clicked.connect(self.generar_reporte)
        layout.addWidget(boton_generar)

        self.setLayout(layout)

    def generar_reporte(self):
       

        self.label.setText("Reportes generados (PDF y Word)")
        
    def convertir_a_json(self,datos):
    
        if not datos:
            return None

        # Definimos los nombres de las columnas
        columnas = ['id', 'fecha', 'tipo', 'cantidad', 'precio', 'estado', 'nivel', 'valor', 'usuario']

        # Creamos una lista de diccionarios
        lista_de_diccionarios = []
        for fila in datos:
            diccionario_fila = dict(zip(columnas, fila))  # Usamos zip para crear un diccionario a partir de columnas y fila
            lista_de_diccionarios.append(diccionario_fila)

        # Convertimos la lista de diccionarios a JSON
        try:
            json_string = json.dumps(lista_de_diccionarios, indent=4, ensure_ascii=False) # indent para formato bonito, ensure_ascii para caracteres especiales
            return json_string
        except TypeError as e:
            print(f"Error al convertir a JSON: {e}")
            return None
        
                
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())
