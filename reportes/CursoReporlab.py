from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def crear_pdf(nombre_archivo, datos):
    # Convertir 2.5 cm a puntos (1 cm = 28.35 puntos)
    margen = 2.5 * 28.35
    ancho, alto = letter

    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    
    # Títulos de las columnas
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, alto - margen, "Nombre")

    for i in range(10):
        c.drawString(margen + 100 + i * 70, alto - margen, f"Ronda {i + 1}")

    c.drawString(margen + 100 + 10 * 70, alto - margen, "Total")

    # Dibujar la tabla
    y = alto - margen - 30
    c.setFont("Helvetica", 10)

    for jugador in datos:
        c.drawString(margen, y, "jugador['nombre']")

        for i in range(10):
            # Divisiones de las rondas
            c.rect(margen + 100 + i * 70, y - 10, 70, 40)  # Dibujar el rectángulo de la celda
            c.drawString(margen + 100 + i * 70 + 10, y + 5, str(jugador['rondas'][i]))  # Parte superior

            # Parte inferior izquierda y derecha
            c.drawString(margen + 100 + i * 70 + 10, y - 15, str(jugador['tiros'][i]['op1']))  # Parte inferior izquierda
            c.drawString(margen + 100 + i * 70 + 40, y - 15, str(jugador['tiros'][i]['op2']))  # Parte inferior derecha

            # Para la ronda 10
            if i == 9:
                c.drawString(margen + 100 + i * 70 + 10, y - 15, str(jugador['tiros'][i]['op1']))  # Parte inferior izquierda
                c.drawString(margen + 100 + i * 70 + 40, y - 15, str(jugador['tiros'][i]['op2']))  # Parte inferior central
                c.drawString(margen + 100 + i * 70 + 60, y - 15, str(jugador['tiros'][i]['op3']))  # Parte inferior derecha

        c.drawString(margen + 100 + 10 * 70, y, str(jugador['puntuacion']))  # Total
        y -= 50  # Espaciado entre filas

    c.save()

# Ejemplo de datos
datos = [{
    'nombre': 'Jugador 1',
    'puntuacion': 0,
    'rondas': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'tiros': [
        {'numero_tiro': 1, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 2, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 3, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 4, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 5, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 6, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 7, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 8, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 9, 'op1': 0, 'op2': 0, 'op3': 0},
        {'numero_tiro': 10, 'op1': 0, 'op2': 0, 'op3': 0},
    ]
}]

# Crear el PDF
crear_pdf("reporte.pdf", datos)