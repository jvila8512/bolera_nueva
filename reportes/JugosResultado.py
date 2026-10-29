import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QFileDialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer

class MiAplicacion(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Generar Reporte en PDF")
        self.setGeometry(100, 100, 300, 150)

        # Crear un botón para generar el reporte
        self.boton_generar = QPushButton("Generar Reporte PDF", self)
        self.boton_generar.clicked.connect(self.generar_reporte)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.boton_generar)
        self.setLayout(layout)

    def generar_reporte(self):
        # Diálogo para seleccionar la ubicación y nombre del archivo
      
        pdf_file, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte PDF", "", "PDF Files (*.pdf);;All Files (*)")

        if not pdf_file:  # Si el usuario cancela, no hacer nada
            return

        # Datos de ejemplo: nombres de jugadores
        jugadores = ["Jugador 1", "Jugador 2", "Jugador 3", "Jugador 4", "Jugador 5"]
        
        # Crear el PDF
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        # Lista para almacenar los elementos de la tabla
        elementos = []

        for jugador in jugadores:
            # Crear la tabla para cada jugador
            data = [["Jugador", "Ronda 1", "", "", "Ronda 2", "", "", "Ronda 3", "", "", "Ronda 4", "", "", "Ronda 5", "", "", "Ronda 6", "", "", "Ronda 7", "", "", "Ronda 8", "", "", "Ronda 9", "", "", "Ronda 10", "", "", "Total"]]
            ronda_data = [jugador]

            # Agregar datos de rondas (ejemplo)
            for ronda in range(1, 11):
                ronda_data.append(f"R{ronda}1")  # Primer cuadro de la ronda
                ronda_data.append(f"R{ronda}2")  # Segundo cuadro de la ronda
                ronda_data.append(f"R{ronda}3")  # Tercer cuadro de la ronda (que ocupa el espacio de los dos anteriores)

            ronda_data.append("Total")  # Columna total
            data.append(ronda_data)

            # Crear la tabla
            tabla = Table(data)
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            # Agregar la tabla a los elementos
            elementos.append(tabla)

            # Agregar un salto de página después de cada tabla, excepto la última
            if jugador != jugadores[-1]:
                elementos.append(Spacer(1, 12))  # Espacio entre tablas

        # Construir el PDF
        doc.build(elementos)

        # Mensaje de éxito
        QMessageBox.information(self, "Éxito", "Reporte PDF generado con éxito.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiAplicacion()
    ventana.show()
    sys.exit(app.exec())