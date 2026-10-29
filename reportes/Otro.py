import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import QUrl

from jinja2 import Environment, FileSystemLoader


class ReportePDF(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de Reportes PDF")

        # Datos para el reporte
        self.data = {
            "titulo": "Reporte de Ejemplo",
            "fecha": "2024-10-27",
            "items": [
                {"nombre": "Item 1", "cantidad": 10, "precio": 100},
                {"nombre": "Item 2", "cantidad": 5, "precio": 50},
            ],
        }

        # Botón para generar el reporte
        generar_boton = QPushButton("Generar Reporte")
        generar_boton.clicked.connect(self.generar_reporte)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(generar_boton)
        self.setLayout(layout)

    def generar_reporte(self):
        # Cargar la plantilla Jinja2
        env = Environment(loader=FileSystemLoader('.'))  # Cargar desde el directorio actualtemplate = env.get_template('reporte.html')

        # Renderizar la plantilla con los datos
        html_output = template.render(data=self.data)

       

        # Mostrar el PDF (opcional, requiere un visor de PDF integrado o externo)

        # Opción 1: usar QWebEngineView (si tienes Qt WebEngine integrado)
        viewer = QWebEngineView()
        viewer.load(QUrl.fromLocalFile("reporte.pdf")) #este método no funciona para pdfs
        viewer.show()

        #Opción 2: Abrir con el visor de PDF por defecto del sistema
        import os
        os.startfile('reporte.pdf')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportePDF()
    window.show()
    sys.exit(app.exec())