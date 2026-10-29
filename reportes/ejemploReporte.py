import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import recursos
from reportlab.graphics.barcode import code93
from reportlab.graphics.barcode import code39
from reportlab.graphics.barcode import usps
from reportlab.graphics.barcode import usps4s
from reportlab.graphics.barcode import ecc200datamatrix


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de PDF")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Generar PDF", self)
        self.button.setGeometry(50, 50, 200, 50)
        self.button.clicked.connect(self.generar_pdf)

    def generar_pdf(self):
                # Define un nombre predeterminado para el archivo
        default_file_name = "reporte.pdf"
            # Abre el diálogo para guardar archivo con un nombre predeterminado
        output_file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Guardar Reporte como",
                default_file_name,  # Nombre predeterminado
                "PDF files (*.pdf);;Word files (*.docx);;All Files (*)"  # Añadiendo formato Word
            )

        if  output_file_path:
            # Renderizar el contenido
            html = self.renderizar_template("Informe Generado", "Este es el contenido del informe generado con Jinja2 y xhtml2pdf.")
            # Generar el PDF
            
            
            
            
            
            
            
            if not self.crear_pdf(html,  output_file_path):
                QMessageBox.information(self, "Éxito", "PDF generado exitosamente.")
            else:
                QMessageBox.critical(self, "Error", "Error al generar el PDF.")

    def renderizar_template(self, titulo, contenido):
        
        env = Environment(loader=FileSystemLoader('reportes'))  # Asegúrate de que el directorio sea correcto
        template = env.get_template('reporteDiarioOK.html')  # El nombre de tu plantilla HTML

        # Datos para renderizar
        data = {
            'fecha': "2023-10-01",
                   'fecha_emitido': "2023-10-01",
                   'juegos': '200',
                   'total': '2402544',
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())