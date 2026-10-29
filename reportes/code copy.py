from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtCore import Qt,QDate

import datetime

# Crear el canvas
c = canvas.Canvas("hola-mundo.pdf", pagesize=letter)
styles = getSampleStyleSheet()
w, h1 = letter

# Definir márgenes de 2.5 cm (convertir a puntos: 1 cm = 28.35 puntos)
margen = 0.7 * 28.35


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
       
fecha_parrafo_derecha = Paragraph(f"Fecha de Juego: {fecha_emision_str}", styles['Normal'])
fecha_parrafo_derecha.wrapOn(c, 270, 100)
fecha_parrafo_derecha.drawOn(c, 420, 760)


# Definir la separación entre cada bloque
separacion = 120  # Ajusta este valor según la separación deseada

for j in range(6):

     # Calcular la posición vertical para cada bloque
    offset_y = j * separacion


   # Dibujar el texto Pistas
    c.setFont("Helvetica-Bold", 8)
    c.drawString(margen + 4, h - margen - 8 - offset_y, "Pista No.")
  
     #dibujar Pistas
    c.rect(margen, h - margen - 13 - offset_y, 120, 20)  # Línea horizontal en el medio
   # c.line(x2-80, y1 + 40, x2 + 90, y1 + 40)  # Línea horizontal en el medio 




    # Dibujar el encabezado
    c.setFont("Helvetica-Bold", 8)
    c.drawString(margen + 2, h - margen - 45 - offset_y, "Nombre y Apellidos")
    
    c.setFont("Helvetica", 8)
    c.drawString(margen + 4, h - margen - 65 - offset_y, "Javier Vila Labrada")
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
    
    c.rect(margen +120, h - margen - 33 - offset_y, 400, 20)  # Línea horizontal en el medio
    
    
    # Dibujar celdas
    for i in range(10):
        c.setFont("Helvetica", 12)
        # Dibujar la celda para cada ronda
        x2 = margen + 120 + i * 40  # Posición de la celda
        y1 = h - margen - 93 - offset_y  # Parte superior de la celda
        
        c.line(x2-80, y1 + 40, x2 + 90, y1 + 40)  # Línea horizontal en el medio   # Línea horizontal en el medio 

        c.rect(x2, y1, 40, 60)  # Dibujar el rectángulo de la celda
        
        
        
        # Dibujar divisiones horizontales
        c.line(x2-120, y1 + 40, x2 + 90, y1 + 40)  # Línea horizontal en el medio   
        c.line(x2-120, y1 + 20, x2 + 40, y1 + 20)  # Línea horizontal en el medio 
        
        c.drawString(x2 + 16, y1 + 48, str(i + 1))  # Parte superior
        
        # Centrar el número en la celda
        c.setFont("Helvetica", 10)
        c.drawString(x2 + 6, y1 + 27, "8")  # Parte inferior (op1)
        
        
        # Dibuja la línea vertical
        c.line(x2 + 20, y1 + 20, x2 + 20, y1 + 36)  # Línea vertical
        
        
        c.drawString(x2 + 28, y1 + 27, "/")  # Parte inferior (op2)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x2 + 16, y1 + 6, str(i + 1))  # Parte superior(Resultado OP)
            # Dibujar el texto Pistas
        c.setFont("Helvetica", 8)
        c.drawString(margen + 4, h - margen - 86- offset_y, "Puntos Acumulados")



      # Dibujar el encabezado de "Total"
    c.drawString(margen + 14 + 15 * 34.7, h - margen - 45 - offset_y, "Total")
    c.rect(margen + 15 * 34.7, h - margen - 93 - offset_y, 50, 60)  # Dibujar el rectángulo de la celda

    # Definir las coordenadas y dimensiones del rectángulo
    x = margen + 15 * 34.7
    y = h - margen - 100 - offset_y
    ancho = 50
    alto = 60

    # Texto Resultado Final
    texto = "300"
    # Calcular la posición del texto para centrarlo
    texto_ancho = c.stringWidth(texto, "Helvetica", 12)  # Medir el ancho del texto
    pos_x = x + (ancho - texto_ancho) / 2  # Posición X centrada
    pos_y = y + (alto - 12) / 2  # Posición Y centrada (12 es el tamaño de la fuente)

    # Escribir el texto en el canvas
    c.setFont("Helvetica", 12)
    c.drawString(pos_x, pos_y, texto)
    c.rect(margen + 400, h - margen -109 - offset_y, 120, 16)  # Línea horizontal en el medio Nombre Competidor
    c.rect(margen + 520, h - margen -109 - offset_y, 50, 16)  # Línea horizontal en el medio
   
    c.setFont("Helvetica", 8)
    #Firma Arbitro
    c.rect(margen + 400, h - margen -125- offset_y, 120, 16)  # Línea horizontal en el medio Nombre Competidor
    
    
    c.drawString(margen + 405, h - margen - 105- offset_y, "Firma Competidor")
    
    c.rect(margen + 520, h - margen -125 - offset_y, 50, 16)  # Línea horizontal en el medio
    c.drawString(margen + 405, h - margen - 118- offset_y, "Firma Arbitro")




# Guardar el documento


 






c.save()