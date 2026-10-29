import sys
from PyQt6.QtWidgets import QTableWidgetItem,QApplication,QTableWidget,QHeaderView,QDialog,QVBoxLayout, QLabel, QMessageBox,QFileDialog

from Crud.juegos.resumenUser import ResumenJuegoUser
from ConexionBD.conexion import Conexion
from bd_modelos.usuario import Usuario
from ConexionBD.juego_Operaciones import JuegoBD_operaciones
from PyQt6.QtCore import Qt,QDate
from bd_modelos.usuario import Usuario
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
import recursos
from pyreportjasper import PyReportJasper
import datetime
import os
import json
import tempfile
#from jinja2 import Environment, FileSystemLoader
#from xhtml2pdf import pisa
#from reportlab.graphics.barcode import code93
#from reportlab.graphics.barcode import code39
#from reportlab.graphics.barcode import usps
#from reportlab.graphics.barcode import usps4s
#from reportlab.graphics.barcode import ecc200datamatrix

 
class ResumenJuegosUser(QDialog): 
    def __init__(self,parent,user:Usuario):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        self.ui = ResumenJuegoUser()
        self.ui.setupUi(self)
        self.tabla=self.ui.tabla_juego
        self.parent=parent
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))

         # Establecer la fecha actual
        self.ui.fechaFiltrar.setDate(QDate.currentDate())
         # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Habilitar la selección de toda la fila
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones() 

        self.UserLogueado = user
        # user: Usuario
        self.initGUI() 
        self.cargardatosJuegosUser(self.UserLogueado.id_usuario,QDate.currentDate().toString("yyyy-MM-dd"))
        self.update_total()
        self.apply_styles()
                    
    def initGUI(self):
       self.ui.fechaFiltrar.dateChanged.connect(self.on_date_changed)
       self.ui.reposte_diario.clicked.connect(self.generar_reporte)
       self.tabla.setColumnCount(7)
       self.tabla.setHorizontalHeaderLabels(["ID", "Fecha","Tipo Juego", "Cantidad Jugadores","Precio", "Pista","Tiempo de Juego"])       
        # Ocultar el encabezado vertical (numeración de filas)
       self.tabla.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical        
        # Ocultar la primera columna
       self.tabla.setColumnHidden(0, True)  # Oculta la columna con índice 0
       #poner los label en susa datos iniciales 
       self.ui.label_7.setText(f"Total: $ 0 ")
       self.ui.label_4.setText("0")
       self.ui.label_6.setText("0")   
    def cargardatosJuegosUser(self,id_usuario,fecha):
        parametros=(id_usuario,fecha)
        juegos_user=   self.juegoBD_operaciones.obtenerJuegosUserporFecha(parametros)
        self.tabla.setRowCount(len(juegos_user))
        
         # Rellenar el QTableWidget con los datos
        for row_index, row_data in enumerate(juegos_user):
            for column_index, item in enumerate(row_data):
                   table_item = QTableWidgetItem(str(item))
                   table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  
                   self.tabla.setItem(row_index, column_index, table_item )

    def on_date_changed(self, date):
        self.cargardatosJuegosUser(23,date.toString("yyyy-MM-dd"))
        self.update_total()
 
 
    def update_total(self):
        total = 0
        cantidadJugadores=0
        torneos=0
        for row in range(self.tabla.rowCount()):
           
            ss=self.tabla.item(row, 2)
            
            if ss.text() == 'Normal':
                cantidadJugadores+=int(self.tabla.item(row,3).text())
                
            else:
               torneos=torneos+1
               
            # Obtener el precio y convertirlo a entero
            item = self.tabla.item(row, 4)

            cantJUgadores=self.tabla.item(row,3)
            if ss.text() == 'Normal':
              if item:
                price = float(item.text())
                jugadores=int(cantJUgadores.text())
                total += price*jugadores
        self.ui.label_7.setText(f"Total: $ {total}")
        self.ui.label_4.setText(f"{cantidadJugadores}")
        self.ui.label_6.setText(f"{torneos}")  





    def apply_styles(self): 
       # Desactivar la edición para toda la tabla
           self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

            # Desactivar la selección
           self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
           self.tabla.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
           # CSS para la tabla
           self.tabla.setStyleSheet("""
           QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #ccc;
                background-color: #f9f9f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 1px;
            }
            QHeaderView::section {
                background-color: #0078d7;
                color: white;
                padding: 1px;
                font-weight: bold;
            }
           
        """)
    def generar_reporte(self):
                # Define un nombre predeterminado para el archivo
        default_file_name = "reporteDiario.pdf"

            # Abre el diálogo para guardar archivo con un nombre predeterminado
        output_file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Guardar Reporte como",
                default_file_name,  # Nombre predeterminado
                "PDF files (*.pdf);;Word files (*.docx);;All Files (*)"  # Añadiendo formato Word
            )
        
        if  output_file_path:
            # Renderizar el contenido
            html = self.renderizar_template()
            # Generar el PDF
            
            
            
            
            
            
            
        if not self.crear_pdf(html,  output_file_path):
                QMessageBox.information(self, "Éxito", "PDF generado exitosamente.")
        else:
                QMessageBox.critical(self, "Error", "Error al generar el PDF.")
    
          
       
      
       


    def renderizar_template(self):
        
        env = Environment(loader=FileSystemLoader('Crud'))  # Asegúrate de que el directorio sea correcto
        template = env.get_template('reporteDiarioOK.html')  # El nombre de tu plantilla HTML
        # Obtener la fecha actual
        fecha_actual = QDate.currentDate()
        # Formatear la fecha como cadena
        fecha_actual.toString("dd/MM/yyyy")
        # Datos para renderizar
        
        #-------------- Calcular el totol
        total = 0
        cantidadJugadores=0
        torneos=0
        for row in range(self.tabla.rowCount()):
           
            ss=self.tabla.item(row, 2)
            
            if ss.text() == 'Normal':
                cantidadJugadores+=int(self.tabla.item(row,3).text())
                
            else:
               torneos=torneos+1
               
            # Obtener el precio y convertirlo a entero
            item = self.tabla.item(row, 4)

            cantJUgadores=self.tabla.item(row,3)
            if ss.text() == 'Normal':
              if item:
                price = float(item.text())
                jugadores=int(cantJUgadores.text())
                total += price*jugadores
        self.ui.label_7.setText(f"Total: $ {total}")
        self.ui.label_4.setText(f"{cantidadJugadores}")
        self.ui.label_6.setText(f"{torneos}")  

        #-------------
        
        data = {
            'fecha': self.ui.fechaFiltrar.date().toString("dd/MM/yyyy"),
                   'fecha_emitido':    fecha_actual.toString("dd/MM/yyyy"),
                   'juegos': cantidadJugadores,
                   'total': total,
        
        }

       
        
     
        return template.render(data)

    def crear_pdf(self, html, nombre_archivo):
        try:
            with open(nombre_archivo, 'w+b') as archivo_pdf:
                pisa_status = pisa.CreatePDF(html, dest=archivo_pdf)
                return pisa_status.err
        except Exception as e:
            print("Ocurrió un error al generar el PDF:", e)
            return True
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
    window =ResumenJuegosUser()
    window.show()
    sys.exit(app.exec())