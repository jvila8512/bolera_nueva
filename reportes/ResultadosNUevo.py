import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import datetime


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Reportes")
        self.setGeometry(100, 100, 300, 200)

        boton_generar = QPushButton("Generar Reporte", self)
        boton_generar.clicked.connect(self.generar_reporte)
        boton_generar.setGeometry(50, 50, 200, 50)

    def generar_reporte(self):
        self.crear_pdf()
        os.startfile("reporte.pdf")  # Abre el PDF generado
        
    def crear_pdf(self):
      
        c = canvas.Canvas("D:\Reportes", pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Encabezado del reporte        
        title = Paragraph("<para align=center><b>Juego </b></para>", styles['h1'])
      
        title.wrapOn(c, 500, 100)
        title.drawOn(c, 50, 700)
        elementos = []

        # Definición de los datos de la tabla
        data = [['Nombre'] + [f'Ronda {i+1}' for i in range(10)] + ['Total']]
        
        for i in range(5):  # Cambia el rango según el número de filas que necesites
            fila = [f'Jugador {i+1}']
            for j in range(10):
                if j < 9:
                    fila.append('2\n3\n10')  # Ejemplo de datos para las rondas 1 a 9
                else:
                    fila.append('1\n2\n3')  # Datos para la ronda 10
            fila.append(f'{i * 10}')  # Total de ejemplo
            data.append(fila)

        # Crear la tabla
        tabla = Table(data, colWidths=[1.5 * inch] + [1.5 * inch] * 10 + [1.5 * inch])

        # Estilo de la tabla
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        # Dividir las celdas de las rondas
        for j in range(1, 11):  # Rondas 1 a 10
            if j < 10:
                estilo.add('LINEBELOW', (j, 0), (j, 0), 1, colors.black)  # Línea horizontal
                estilo.add('LINEABOVE', (j, 0), (j, 0), 1, colors.black)   # Línea horizontal
                estilo.add('LINEBELOW', (j, 1), (j, 1), 1, colors.black)   # Línea horizontal
                estilo.add('LINEABOVE', (j, 1), (j, 1), 1, colors.black)   # Línea horizontal
                estilo.add('LINEBELOW', (j, 2), (j, 2), 1, colors.black)   # Línea horizontal
                
                # Líneas verticales para dividir las celdas
                estilo.add('LINELEFT', (j, 1), (j, 1), 1, colors.black)  # Línea vertical
                estilo.add('LINERIGHT', (j, 1), (j, 1), 1, colors.black) # Línea vertical
                estilo.add('LINELEFT', (j, 2), (j, 2), 1, colors.black)  # Línea vertical
                estilo.add('LINERIGHT', (j, 2), (j, 2), 1, colors.black) # Línea vertical

            else:  # Para la ronda 10
                estilo.add('LINEBELOW', (j, 0), (j, 0), 1, colors.black)  # Línea horizontal
                estilo.add('LINEABOVE', (j, 0), (j, 0), 1, colors.black)   # Línea horizontal
                estilo.add('LINEBELOW', (j, 1), (j, 1), 1, colors.black)   # Línea horizontal
                estilo.add('LINEABOVE', (j, 1), (j, 1), 1, colors.black)   # Línea horizontal
                estilo.add('LINEBELOW', (j, 2), (j, 2), 1, colors.black)   # Línea horizontal
                estilo.add('LINEABOVE', (j, 2), (j, 2), 1, colors.black)   # Línea horizontal
                
                # Líneas verticales para dividir las celdas de la ronda 10
                estilo.add('LINELEFT', (j, 1), (j, 1), 1, colors.black)  # Línea vertical
                estilo.add('LINELEFT', (j, 2), (j, 2), 1, colors.black)  # Línea vertical
                estilo.add('LINERIGHT', (j, 1), (j, 1), 1, colors.black) # Línea vertical
                estilo.add('LINERIGHT', (j, 2), (j, 2), 1, colors.black) # Línea vertical

        tabla.setStyle(estilo)
        elementos.append(tabla)
        c.save()
        
    def crear_reporte(self, file_path, fecha_reporte, fecha_emision,jugadores,total):
        c = canvas.Canvas(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Encabezado del reporte        
        title = Paragraph("<para align=center><b>Juego </b></para>", styles['h1'])
      
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
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())