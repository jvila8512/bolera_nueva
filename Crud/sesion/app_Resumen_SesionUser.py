import sys
from PyQt6.QtWidgets import QTableWidgetItem,QApplication,QTableWidget,QHeaderView,QDialog,QVBoxLayout, QLabel, QMessageBox,QFileDialog

from Crud.juegos.resumenUser import ResumenJuegoUser
from ConexionBD.conexion import Conexion
from bd_modelos.usuario import Usuario
from ConexionBD.juego_Operaciones import JuegoBD_operaciones
from PyQt6.QtCore import Qt,QDate
from bd_modelos.usuario import Usuario
from bd_modelos.Sesion import Sesion
from PyQt6.QtGui import QIcon  # Importa QIcon para usar iconos
import recursos
from pyreportjasper import PyReportJasper
import datetime
import os
import json
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import datetime

 
class ResumenSesionUser(QDialog): 
    def __init__(self,parent,id_sesion,user,fecha):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        
        print(f"ID {id_sesion} USer>: {user} Fecha {fecha}")
        
        self.ui = ResumenJuegoUser()
        self.ui.setupUi(self)
        self.tabla=self.ui.tabla_juego
        self.parent=parent
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))
        self.id_sesion=id_sesion
        
                # Texto de fecha
        texto_fecha = fecha
        self.usuario=user

        # Extraer la parte de la fecha (YYYY-MM-DD)
        parte_fecha = texto_fecha.split(" ")[0]

        # Convertir a QDate
        fecha_a_cargar = QDate.fromString(parte_fecha, "yyyy-MM-dd")
        # Establecer en QDateEdit
        self.ui.fechaFiltrar.setDate(fecha_a_cargar)

         # Establecer la fecha actual
        #self.ui.fechaFiltrar.setDate(QDate.currentDate())
         # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Habilitar la selección de toda la fila
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones() 
        self.juegos_user=None

  
        
        # user: Usuario
        self.initGUI() 
        print(f"Fecha para cargar { parte_fecha}")
        self.cargardatosJuegosUser( user,parte_fecha)
        
        self.ui.label.setText(F"Información del Usuario:  {user}")
        self.apply_styles()
                    
    def initGUI(self):
       self.ui.fechaFiltrar.dateChanged.connect(self.on_date_changed)
       self.ui.reposte_diario.clicked.connect(self.generar_reporte)
       self.tabla.setColumnCount(8)
       self.tabla.setHorizontalHeaderLabels(["ID", "Fecha","Tipo Juego", "Cantidad Jugadores","Precio", "Pista","Tiempo de Juego","Terminado"])       
        # Ocultar el encabezado vertical (numeración de filas)
       self.tabla.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical        
        # Ocultar la primera columna
       self.tabla.setColumnHidden(0, True)  # Oculta la columna con índice 0
       #poner los label en susa datos iniciales 
       self.ui.label_11.setText(f"Total: $ 0 ")
       self.ui.label_4.setText("0")
       self.ui.label_6.setText("0")
       self.ui.juego_NT.setText("0")   
    def cargardatosJuegosUser(self,user,fecha):
       
        parametros=(fecha,user)
        self.juegos_user=   self.juegoBD_operaciones.obtenerJuegosporFechaSesionUsuario(parametros)
        print(self.juegos_user)
        self.tabla.setRowCount(len(self.juegos_user))
        
         # Rellenar el QTableWidget con los datos
        for row_index, row_data in enumerate(self.juegos_user):
            bandera=False
            for column_index, item in enumerate(row_data):
                   
                   table_item = QTableWidgetItem(str(item))                   
                   table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                   
                   if column_index == 2 and item == "Torneo": 
                       bandera=True
                   if column_index == 4 and bandera:                      
                        table_item_4 = QTableWidgetItem("-----")
                        table_item_4.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.tabla.setItem(row_index, column_index, table_item_4)
                     
                   else:
                      if column_index == 7 :
                             
                                if item == 1:
                                    item_estado = QLabel("Terminado")                           
                                    item_estado.setStyleSheet("QLabel { color: green; text-align: center;}")
                                    item_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.tabla.setCellWidget(row_index, column_index, item_estado)
                                else:
                                    item_estado = QLabel("----")
                                    item_estado.setStyleSheet("QLabel { color: red;text-align: center; }")
                                    item_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.tabla.setCellWidget(row_index, column_index, item_estado)
                   
                      else:
                            self.tabla.setItem(row_index, column_index, table_item )


        total = 0
        cantidadJugadores=0
        torneos=0
        juegos_NT=0
            # Iterar sobre cada tupla en el arreglo
        for item in self.juegos_user:
            if item[2] == 'Normal':
                if item[7] != 0:
                    cantidadJugadores += item[3]
                    total += item[3] * item[4]
                
            else:
                torneos+= item[3]  
            if item[7] == 0:
                   juegos_NT += item[3]    
                         
        self.ui.label_11.setText(f"Total: $ {total}")
        self.ui.label_4.setText(f"{cantidadJugadores}")
        self.ui.label_6.setText(f"{torneos}") 
        self.ui.juego_NT.setText(f"{juegos_NT}")




    def on_date_changed(self, date):
        self.cargardatosJuegosUser(self.usuario,date.toString("yyyy-MM-dd"))
       
 
    




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
        default_file_name = "Reporte Diario.pdf"

            # Abre el diálogo para guardar archivo con un nombre predeterminado
        output_file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Guardar Reporte como",
                default_file_name,  # Nombre predeterminado
                "PDF files (*.pdf);;Word files (*.docx);;All Files (*)"  # Añadiendo formato Word
            )
        
        
        
        
        
        if output_file_path :
            try:
                    # Obtener la fecha actual
                fecha_actual = QDate.currentDate()
                # Formatear la fecha como cadena
                fe=fecha_actual.toString("dd/MM/yyyy")
                #-------------- Calcular el totol
                total = 0
                cantidadJugadores=0
                torneos=0
                juegos_NT=0
                    # Iterar sobre cada tupla en el arreglo
                for item in self.juegos_user:
                    if item[2] == 'Normal':
                            if item[7] != 0:
                                cantidadJugadores += item[3]
                                total += item[3] * item[4]
                            
                    else:
                                torneos+= item[3]  
                    if item[7] == 0:
                        juegos_NT += item[3] 
                           
                    self.crear_reporte( output_file_path, self.ui.fechaFiltrar.date().toString("dd/MM/yyyy"), fe, cantidadJugadores,total)
                QMessageBox.information(self, "Éxito", "Reporte generado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al generar el reporte: {str(e)}")
        else:
            print("No se seleccionó ninguna ubicación para guardar")
        
        
        
        
    def crear_reporte(self, file_path, fecha_reporte, fecha_emision,jugadores,total):
        c = canvas.Canvas(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Encabezado del reporte
        
        title = Paragraph("<para align=center><b>Reporte Diario</b></para>", styles['h1'])
      
        title.wrapOn(c, 500, 100)
        title.drawOn(c, 50, 700)
        
         # Fechas
        fecha_reporte_str = fecha_reporte
        fecha_emision_str = fecha_emision
        fecha_parrafo_izquierda = Paragraph(f"Fecha: {fecha_reporte_str}", styles['Normal'])
        fecha_parrafo_izquierda.wrapOn(c, 200, 100)
        fecha_parrafo_izquierda.drawOn(c, 50, 650)
       
        fecha_parrafo_derecha = Paragraph(f"Fecha de Emisión: {fecha_emision_str}", styles['Normal'])
        fecha_parrafo_derecha.wrapOn(c, 200, 100)
        fecha_parrafo_derecha.drawOn(c, 420, 650)

        self.ancho, self.alto = letter       

        # Datos para la tabla (ejemplo)
        data = [
            ["Juegos", "Total"],
            [str(jugadores), str(total)],
          
        ]
        
        table = Table(data,(self.ancho-100)/2)
       # tabla = Table(convertirDatos, colWidths=(self.ancho-100)/len(self.cabecera), hAlign="CENTER")
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
             ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        table.wrapOn(c, 100, 100)
        table.drawOn(c, 50, 550)
        
          # Pie de firmas
        instructor_firma = Paragraph(f"Instructor: ___________", styles['Normal'])
        instructor_firma.wrapOn(c, 200, 100)
        instructor_firma.drawOn(c, 50, 400)
        
        admin_firma = Paragraph(f"Administrador: ___________", styles['Normal'])
        admin_firma.wrapOn(c, 200, 100)
        admin_firma.drawOn(c, 420, 400)


        c.save()  
            
            
            
            
            
         
          
       
      
       


    
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