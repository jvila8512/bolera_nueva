import sys
from PyQt6.QtWidgets import QWidget,QTableWidgetItem,QApplication,QTableWidget,QHeaderView,QDialog,QVBoxLayout, QLabel, QMessageBox,QFileDialog,QPushButton,QHBoxLayout,QSizePolicy

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
import recursoAnimacion
from bd_modelos.juego_bolos import JuegoBolos
 
class ResumenJuegosUser(QDialog): 
    def __init__(self,parent,sesion:Sesion,user):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        self.ui = ResumenJuegoUser()
        self.ui.setupUi(self)
        self.tabla=self.ui.tabla_juego
        self.parent=parent
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))
              # Texto de fecha
        texto_fecha = sesion.fecha
        self.usuario=user

        # Extraer la parte de la fecha (YYYY-MM-DD)
        parte_fecha = texto_fecha.split(" ")[0]

        # Convertir a QDate
        fecha_a_cargar = QDate.fromString(parte_fecha, "yyyy-MM-dd")
        # Establecer en QDateEdit
        self.ui.fechaFiltrar.setDate(fecha_a_cargar)

         # Establecer la fecha actual
       # self.ui.fechaFiltrar.setDate(QDate.currentDate())
         # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Habilitar la selección de toda la fila
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones() 
        self.juegos_user=None

        
        self.sesion=sesion
        # user: Usuario
        self.initGUI() 
       # print(f"Userrrrrr {user} Fechaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  { parte_fecha}")
        self.cargardatosJuegosUser(user,  parte_fecha)
        
        
        self.apply_styles()
                    
    def initGUI(self):
        
       self.ui.fechaFiltrar.dateChanged.connect(self.on_date_changed)
       self.ui.reposte_diario.clicked.connect(self.generar_reporte)
       self.tabla.setColumnCount(9)
       self.tabla.setHorizontalHeaderLabels(["ID", "Fecha","Tipo Juego", "Cantidad Jugadores","Precio", "Pista","Tiempo de Juego","Terminado","Acciones"])       
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
                          if column_index<8 :
                            self.tabla.setItem(row_index, column_index, table_item )
            # Botones de actualizar y borrar
            action_layout = QHBoxLayout()
            update_button = QPushButton()
            update_button.setToolTip("Descargar Anotación del Juego")
            update_button.setIcon(QIcon(":/animacion/iconos/bolera.svg"))  # Cambia esta ruta a la de tu icono          
            update_button.clicked.connect(lambda checked, r=row_index: self.update_row(r))    
            delete_button = QPushButton()
            delete_button.clicked.connect(lambda checked, r=row_index: self.delete_row(r))
            delete_button.setIcon(QIcon(":/animacion/iconos/delete.svg"))  # Cambia esta ruta a la de tu icono
             # Ajustar el tamaño de los botones
            update_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            delete_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            # Crear un layout horizontal para los botones
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)  # Espacio a la izquierda
            button_layout.addWidget(update_button)
            #button_layout.addWidget(delete_button)
            button_layout.addStretch(1)  # Espacio a la derecha
            button_layout.setContentsMargins(10, 5, 10, 20)  # (izquierda, arriba, derecha, abajo)
            action_layout.addWidget(update_button)
          #  action_layout.addWidget(delete_button)            
            # Crear un QWidget para contener el layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
              # Establecer un tamaño mínimo para el QWidget que contiene los botones
            button_widget.setMinimumHeight(40)  # Ajusta la altura mínima según sea necesario
            self.tabla.setCellWidget(row_index, 8, button_widget ) # Columna de Acciones


        total = 0
        cantidadJugadores=0
        torneos=0
        juegos_NT=0
            # Iterar sobre cada tupla en el arreglo
        
        if self.juegos_user:    
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


    def update_row(self, row):
        id_juego = int(self.tabla.item(row, 0).text())  
        fechaJuego= self.tabla.item(row, 1).text()
        juegoBD_operaciones=JuegoBD_operaciones() 

        juegoPIsta=juegoBD_operaciones.obtenerJuego(id_juego)
        jugadores=juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(id_juego)
        
        #Calculamos la puntuacion 
        juego = JuegoBolos(jugadores)
        resultados = juego.calcular_puntuacion()
        # Crear el canvas
        c = canvas.Canvas("Reporte Juego.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        w, h1 = letter

        # Definir márgenes de 2.5 cm (convertir a puntos: 1 cm = 28.35 puntos)
        margen = 0.4 * 28.35


        h=h1-23
            # Obtener la fecha actual
        fecha_actual = QDate.currentDate()
                        # Formatear la fecha como cadena
        fe=fecha_actual.toString("dd/MM/yyyy")
                        #-------------- Calcular el totol
        # Dibujar el texto
        #c.drawString(margen, h - margen, "Juegos")

        # Calcular la posición de la línea
        x1 = margen  # Comienza en el margen izquierdo
        y = h - margen - 60  # Un poco debajo del texto
        x2 = w - margen  # Termina en el margen derecho

        title = Paragraph("<para align=center><b>Hoja de Anotación</b></para>", styles['h1'])
        title.wrapOn(c, 400, 100)
        title.drawOn(c, 50, 750)
                
                # Fechas
        #fecha_reporte_str = "12/12/2025"
        fecha_emision_str = fe
        #fecha_parrafo_izquierda = Paragraph(f"Fecha: {fecha_reporte_str}", styles['Normal'])
        #fecha_parrafo_izquierda.wrapOn(c, 200, 100)
        #fecha_parrafo_izquierda.drawOn(c, 50, 650)
            
        fecha_parrafo_derecha = Paragraph(f"Fecha de Juego: {fechaJuego}", styles['Normal'])
        fecha_parrafo_derecha.wrapOn(c, 270, 100)
        fecha_parrafo_derecha.drawOn(c, 420, 760)


        # Definir la separación entre cada bloque
        separacion = 120  # Ajusta este valor según la separación deseada
        #j=1
        #for j in range(6):print(jugador)

        #for fila, resultado in enumerate(self.resultados):
                
        for j,resultado in enumerate(resultados):    
            

        # print(jugador[1]['nombre'])
            # Calcular la posición vertical para cada bloque
            offset_y = j * separacion


        # Dibujar el texto Pistas (id_juego,)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(margen + 4, h - margen - 8 - offset_y, "Pista No.")
        
            #dibujar Pistas
            c.rect(margen, h - margen - 13 - offset_y, 120, 20)  # Línea horizontal en el medio
        # c.line(x2-80, y1 + 40, x2 + 90, y1 + 40)  # Línea horizontal en el medio 
            c.setFont("Helvetica", 10)
            c.drawString(margen + 50, h - margen - 28 - offset_y, str(juegoPIsta[0][8]))
            



            # Dibujar el encabezado
            c.setFont("Helvetica-Bold", 8)
            c.drawString(margen + 2, h - margen - 45 - offset_y, "Nombre y Apellidos")
            c.setFont("Helvetica", 8)
            c.drawString(margen + 4, h - margen - 65 - offset_y, resultado['nombre'])
            c.rect(margen, h - margen - 93 - offset_y, 120, 80) # tamano del recuadro
            c.rect(margen, h - margen - 93 - offset_y, 120, 60) # tamano del recuadro







            # Dibujar el rectángulo
            x = margen + 120
            y = h - margen - 33 - offset_y
            ancho = 400
            alto = 20

            # Texto que deseas centrar
            texto = "Rondas"
            # Calcular la posición del texto para centrarlo
            texto_ancho = c.stringWidth(texto, "Helvetica", 12)  # Medir el ancho del texto
            pos_x = x + (ancho - texto_ancho) / 2  # Posición X centrada
            pos_y = y + (alto - 12) / 2  # Posición Y centrada (12 es el tamaño de la fuente)

            # Escribir el texto en el canvas
            c.setFont("Helvetica", 12)
            c.drawString(pos_x, pos_y, texto)  # Aquí no se resta offset_y
            
            c.rect(margen +120, h - margen - 33 - offset_y, 420, 20)  # Línea horizontal en el medio
            
            #for fila, resultado in enumerate(self.resultados):
        # for i, columna in enumerate(jugador['rondas']):
                        
            #  op1 = jugador['tiros']['op1']
            #   op2 = jugador['tiros']['op2']
            # Dibujar celdas
            #for i in range(10):
            puntuacion_acumulada = 0
            for i, puntuacion_ronda in enumerate(resultado['rondas']):
            # print(i)
                op1 = resultado['tiros'][i]['op1']
                op2 = resultado['tiros'][i]['op2']
                op3 = resultado['tiros'][i]['op3']
                puntuacion_acumulada += puntuacion_ronda
                op1M=""
                op2M=""
                op3M=""
                
                if i==9 :
                            #Si todos los tiros fueron 10 escribir X rgb(0, 0, 168) rgb(0, 0, 168)
                            if op1==10 and op2==10 and op3==10:
                                op1M="X"                                 
                                op2M="X"
                                op3M="X"
                               
                            else:
                            #si el primero es 10 ya tiene derecho a otro tiro adicional
                             if op1<10:
                               
                               
                                  if op1!=0:
                                      op1M=op1    
                                      
                                  else:
                                      op1M="0"
                                     

                             else:
                                op1M="X" 
                            
                            # if  self.tiroActivo==2 and self.bolosTiro1<10 and self.bolosTiro1+self.bolosTiro2==10:

                             if op2<10:
                                if op1+op2==10 and op1<10 :
                                    op2M="/" 
                                  
                                else:
                                  if op2!=0:
                                      op2M=op2 
                                      
                                  else:
                                      op2M="0" 
                                    
                             else:
                                    op2M="X" 
                                    
                            
                            
                            
                            
                            
                            
                             if op3<10: 
                                if op3!=0:
                                    op3M=op3
                                  
                                else:
                                    op3M="0"
                                   
                             else:
                                op3M="X"
                               
                else:
                          if op1 == 10:
                                op1M=""                                 
                                op2M="X"
                            
                          elif op1 == 0 and op2 == 10:
                                op1M="0"                                 
                                op2M="/"
                               
                          elif op1 == 0 and op2 == 0:
                                op1M="0"                                 
                                op1M="0"
                                
                          elif op1 + op2 == 10:
                                op1M=op1                                 
                                op2M="/"
                              
                          else:
                                op1M=op1                                 
                                op2M=op2
                               
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                #♦print(f"Op . {op1}")
                #print(f"Op2 . {op2}")
                c.setFont("Helvetica", 12)
                # Dibujar la celda para cada ronda
                x2 = margen + 120 + i * 40  # Posición de la celda
                y1 = h - margen - 93 - offset_y  # Parte superior de la celda
                
                c.line(x2-80, y1 + 40, x2 + 90, y1 + 40)  # Línea horizontal en el medio   # Línea horizontal en el medio 

            
                
                
                if  i<9 :
                    c.rect(x2, y1, 40, 60)  # Dibujar el rectángulo de la celda
                    # Dibujar divisiones horizontales
                    c.line(x2-120, y1 + 40, x2 + 90, y1 + 40)  # Línea horizontal en el medio   
                    c.line(x2-120, y1 + 20, x2 + 40, y1 + 20)  # Línea horizontal en el medio 
                    
                    c.drawString(x2 + 16, y1 + 48, str(i + 1))  # Parte superior
                    
                    # Centrar el número en la celda
                    c.setFont("Helvetica", 10)
                    c.drawString(x2 + 6, y1 + 27, str(op1M))  # Parte inferior (op1)
                    
                    
                    # Dibuja la línea vertical
                    c.line(x2 + 20, y1 + 20, x2 + 20, y1 + 40)  # Línea vertical
                    
                    
                    c.drawString(x2 + 28, y1 + 27, str(op2M))  # Parte inferior (op2)
                    c.setFont("Helvetica", 11)
                    c.drawString(x2 + 16, y1 + 6, str(puntuacion_acumulada) ) # Parte superior(Resultado OP)
                        # Dibujar el texto Pistas
                    c.setFont("Helvetica", 8)
                    c.drawString(margen + 4, h - margen - 86- offset_y, "Puntos Acumulados")
                    
                else:
                    c.rect(x2, y1, 60, 60)  # Dibujar el rectángulo de la celda
                    # Dibujar divisiones horizontales
                    c.line(x2-120, y1 + 40, x2 + 110, y1 + 40)  # Línea horizontal en el medio   
                    c.line(x2-120, y1 + 20, x2 + 60, y1 + 20)  # Línea horizontal en el medio 
                    
                    c.drawString(x2 + 16, y1 + 48, str(i + 1))  # Parte superior
                    
                    # Centrar el número en la celda
                    c.setFont("Helvetica", 10)
                    c.drawString(x2 + 6, y1 + 27, str(op1M))  # Parte inferior (op1)
                    
                    
                    # Dibuja la línea vertical
                    c.line(x2 + 20, y1 + 20, x2 + 20, y1 + 40)  # Línea vertical
                    
                    c.line(x2 + 40, y1 + 20, x2 + 40, y1 + 40)  # Línea vertical
                    
                    
                    c.drawString(x2 + 28, y1 + 27, str(op2M))  # Parte inferior (op2)
                    c.drawString(x2 + 44, y1 + 27, str(op3M))  # Parte inferior (op2)
                    c.setFont("Helvetica", 11)
                    c.drawString(x2 + 16, y1 + 6, str(puntuacion_acumulada) ) # Parte superior(Resultado OP)
                        # Dibujar el texto Pistas
                    c.setFont("Helvetica", 8)
                    c.drawString(margen + 4, h - margen - 86- offset_y, "Puntos Acumulados")



            
            # Dibujar el encabezado de "Total"
            c.drawString(margen + 14 + 15 * 36, h - margen - 45 - offset_y, "Total")
            c.rect(margen + 15 * 36, h - margen - 93 - offset_y, 50, 60)  # Dibujar el rectángulo de la celda

            # Definir las coordenadas y dimensiones del rectángulo
            x = margen + 15 * 36
            y = h - margen - 100 - offset_y
            ancho = 50
            alto = 60

            # Texto Resultado Final
            texto = f"{resultado['puntuacion']}"
            # Calcular la posición del texto para centrarlo
            texto_ancho = c.stringWidth(texto, "Helvetica-Bold", 12)  # Medir el ancho del texto
            pos_x = x + (ancho - texto_ancho) / 2  # Posición X centrada
            pos_y = y + (alto - 12) / 2  # Posición Y centrada (12 es el tamaño de la fuente)

            # Escribir el texto en el canvas
            c.setFont("Helvetica-Bold", 12)
            c.drawString(pos_x, pos_y, texto)
            
            
            c.rect(margen + 400, h - margen -109 - offset_y, 140, 16)  # Línea horizontal en el medio Nombre Competidor
            c.rect(margen + 540, h - margen -109 - offset_y, 50, 16)  # Línea horizontal en el medio
        
            c.setFont("Helvetica", 8)
            #Firma Arbitro
            c.rect(margen + 400, h - margen -125- offset_y, 140, 16)  # Línea horizontal en el medio Nombre Competidor
            
            
            c.drawString(margen + 405, h - margen - 105- offset_y, "Firma Competidor")
           
            c.rect(margen + 540, h - margen -125 - offset_y, 50, 16)  # Línea horizontal en el medio
            c.drawString(margen + 405, h - margen - 118- offset_y, "Firma Arbrito")




        # Guardar el documento


        



        #Reporte Juego.pdf


        c.save()
        if os.name== "nt":
            os.startfile("Reporte Juego.pdf") 
            

    def delete_row(self, id_sesion):
        # Eliminar la sesión
        confirmation = QMessageBox.question(self, 'Confirmar', '¿Estás seguro de que quieres borrar este Juego?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmation == QMessageBox.StandardButton.Yes:
           # self.cursor.execute("DELETE FROM sesion WHERE id_sesion = ?", (id_sesion,))
            #self.conexion.commit()
            # Actualizar la tabla
            self.cargar_datos()

         

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
             QPushButton {
          
            margin: 2px 4px;  /* Añadir margen para separar botones */
          
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #dadada;
        }
           
        """)
    def generar_reporte(self):
        
        fecha = self.ui.fechaFiltrar.date()

        # Formatear la fecha en "día/mes/año"
        fecha_formateada = fecha.toString("dd-MM-yyyy")
        print(fecha_formateada)
                # Define un nombre predeterminado para el archivo
        default_file_name = f"Reporte Diario ({fecha_formateada}).pdf"

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