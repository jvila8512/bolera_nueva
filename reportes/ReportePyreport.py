import json
import sys
import tempfile
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox,QFileDialog
from PyQt6.QtCore import Qt,QDate
from pyreportjasper import PyReportJasper
import datetime
import os
from ConexionBD.juego_Operaciones import JuegoBD_operaciones

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reporte con PyReportJasper")
        self.setGeometry(200, 200, 400, 200)  # (x, y, ancho, alto)

        layout = QVBoxLayout()
       # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones()
        parametros=(23,"2025-01-08" )  # Año, mes, día
        juegos_user=   self.juegoBD_operaciones.obtenerJuegosUserporFecha(parametros)
        #self.datos= self.preparar_datos_reporte(juegos_user)
        print(juegos_user)
       

        self.label = QLabel("Presiona el botón para generar el reporte")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        boton_generar = QPushButton("Generar Reporte")
        boton_generar.clicked.connect(self.generar_reporte)
        layout.addWidget(boton_generar)

        self.setLayout(layout)

    def generar_reporte(self):
                # Define un nombre predeterminado para el archivo
        default_file_name = "reporte.pdf"

            # Abre el diálogo para guardar archivo con un nombre predeterminado
        output_file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Guardar Reporte como",
                default_file_name,  # Nombre predeterminado
                "PDF files (*.pdf);;Word files (*.docx);;All Files (*)"  # Añadiendo formato Word
            )
        
       
                
        # Obtenemos el directorio actual donde se está ejecutando el script
        directorio_actual = sys.path[0] #Esto es muy importante para evitar problemas con la ruta del .jasper
         # Verifica que el archivo .jasper existe
       
        
          
        #Genera el reporte en pdf
        ruta_jasper = "diarioJuegos.jasper"  # Reemplaza con la ruta a tu .jasper
        REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'diarioJuegos.jasper')
        #RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
       # print(REPORTS_DIR)
       # print(RESOURCES_DIR)
        if not os.path.exists(REPORTS_DIR):
            QMessageBox.critical(self, "Error", f"No se encontró el archivo .jasper en: {ruta_jasper}")
            return  # Sale de la función si el archivo no existe
        #  os.path.join("reportes", "reporte.docx"),
        
       # RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
        #REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
        
        input_file = self.obtener_ruta_relativa("reporteDiario.jrxml") #os.path.join(REPORTS_DIR, 'diarioJuegos.jasper')
        output_file = os.path.dirname(os.path.abspath(__file__))  # La ruta de salida para el Word
        parametros=(23,"2025-01-08" )  # Año, mes, día
        juegos_user=   self.juegoBD_operaciones.obtenerJuegosUserporFecha(parametros)
        self.datos= self.preparar_datos_reporte(juegos_user)
        
        json_data = json.dumps(juegos_user)
            # Crear archivo temporal
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json', newline='') as temp_file:
            json.dump(self.datos, temp_file)
            temp_file_path = temp_file.name




        print(  self.datos)
        parametrosreporte={
                "administrador": "Javier Vila Labrada",
                "fecha":"10-10-2025",
                "operario":"Vlady Gongora carreras"


        }
        
        conn = {
            'driver': 'json',
            'data_file': temp_file_path,
            'json_query': 'datos.user'
        }
        pyreportjasper = PyReportJasper()
        pyreportjasper.config(
            input_file,
            output_file=output_file_path,
            output_formats=["pdf"],
            db_connection=conn,
            parameters=parametrosreporte
        )

       
      
        print('Result is the file below.')
        print(output_file_path + '.pdf')
            # Procesa el informe y guarda el PDF
        if output_file_path:
            result = pyreportjasper.process_report()

            
        else:
            print("No se seleccionó ninguna ubicación para guardar")
        
                
        
        #Genera el reporte en word
       # jasper.process(
          #  ruta_jasper,  # La ruta al .jasper compilado
           # f"{directorio_actual}/reporte.docx",  # La ruta de salida para el Word
           # parameters=parametros, # Parámetros que le mandamos
         # format_list=["docx"],  # Formato del reporte
       # )

        self.label.setText("Reportes generados (PDF y Word)")
        
    def preparar_datos_reporte(self,datos):
    
        if not datos:
         return {"datos": {"user": []}}

        campos = ['id', 'fecha', 'tipojuego', 'cantidadjugadores', 'precio', 'pista', 'tiempo' ,'juegoactivo','user']
        data_list = []
        
        for fila in datos:
            fila_dict = {}
            for i, valor in enumerate(fila):
                fila_dict[campos[i]] = valor
            data_list.append(fila_dict)

        return {"datos": {"user": data_list}}
    def obtener_ruta_relativa(self,nombre_archivo):
        try:
            directorio_script = os.path.dirname(os.path.abspath(__file__))
            ruta_relativa = os.path.join(directorio_script, nombre_archivo)
            return ruta_relativa
        except:
            return None
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())
