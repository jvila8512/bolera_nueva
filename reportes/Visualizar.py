import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextBrowser
from jinja2 import Environment, FileSystemLoader
import recursos

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reporte Diario")
        self.setGeometry(100, 100, 800, 600)

        # Cargar plantilla Jinja
        env = Environment(loader=FileSystemLoader('reportes'))  # Asegúrate de que el directorio sea correcto
        template = env.get_template('plantilla.html')  # El nombre de tu plantilla HTML

        # Datos para renderizar
        data = {
            'foto_operario': ':iconos/dasboard/icon/title_icon.png',  # Cambia con la ruta correcta
            'nombre_operario': 'Juan Pérez',
            'juegos': [
                {'fecha': '2023-10-01', 'cantidad_jugadores': 10, 'tiempo': 120, 'precio': 5},
                {'fecha': '2023-10-02', 'cantidad_jugadores': 8, 'tiempo': 90, 'precio': 5},
            ],
            'confeccionado_por': 'Nombre del Confeccionista',
            'recibido_por': 'Nombre del Receptor',
        }

        # Renderizar el HTML
       # rendered_html = template.render(data)
        # Renderiza el template con los datos
        html = template.render(
            data
        )

       

        # Configuración del layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())