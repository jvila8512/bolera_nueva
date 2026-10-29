import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap

class CarruselFotos(QWidget):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana
        self.setWindowTitle('Carrusel de Fotos')
       # self.showMaximized()  # Ventana maximizada
       # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Fondo transparente si necesitas
        #self.showFullScreen()  # Ventana maximizada

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Etiqueta para mostrar las imágenes
        self.label_foto = QLabel()
        self.label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_foto)

        # Botones de navegación
        self.boton_anterior = QPushButton('Anterior')
        self.boton_siguiente = QPushButton('Siguiente')
        self.boton_anterior.clicked.connect(self.mostrar_foto_anterior)
        self.boton_siguiente.clicked.connect(self.mostrar_foto_siguiente)

        # Layout para botones
        self.layout_botones = QHBoxLayout()
        self.layout_botones.addWidget(self.boton_anterior)
        self.layout_botones.addWidget(self.boton_siguiente)

        self.layout.addLayout(self.layout_botones)

        # Lista de imágenes
        self.imagenes = ['fotos/bolos1.jpg', 'fotos/bolos2.jpg', 'fotos/bolos3.jpg']  # Cambia los nombres de las imágenes por los tuyos
        self.indice_actual = 0
        self.mostrar_foto()

        # Temporizador para cambiar automáticamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_foto_siguiente)
        self.timer.start(3000)  # Cambiar cada 3 segundos

    def mostrar_foto(self):
        # Cargar y mostrar la imagen actual
        pixmap = QPixmap(self.imagenes[self.indice_actual])
        self.label_foto.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def mostrar_foto_anterior(self):
        self.indice_actual = (self.indice_actual - 1) % len(self.imagenes)
        self.mostrar_foto()

    def mostrar_foto_siguiente(self):
        self.indice_actual = (self.indice_actual + 1) % len(self.imagenes)
        self.mostrar_foto()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    carrusel = CarruselFotos()
    carrusel.show()
    sys.exit(app.exec())