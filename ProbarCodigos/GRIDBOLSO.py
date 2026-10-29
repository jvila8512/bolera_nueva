import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize, QMargins

class MyFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(1)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bolos con Imágenes")
        
        main_layout = QVBoxLayout(self)  # Layout principal

        # QFrame con altura fija
        fixed_height_frame = QFrame()
        fixed_height_frame.setFixedHeight(60)
        fixed_height_frame.setFrameShape(QFrame.Shape.StyledPanel)
        fixed_height_frame.setFrameShadow(QFrame.Shadow.Raised)
        fixed_height_frame.setLineWidth(1)
        main_layout.addWidget(fixed_height_frame)

        # Layout dentro del frame con altura fija
        fixed_height_layout = QVBoxLayout(fixed_height_frame)

        # QFrame que contiene el grid de los bolos.
        self.bolos_frame = MyFrame()
        fixed_height_layout.addWidget(self.bolos_frame)


        self.create_bowling_pins()

    def create_bowling_pins(self):
    
        # Crear los labels (Puedes cargarlos desde tu ui)
        self.bolo1 = QLabel()
        self.bolo2 = QLabel()
        self.bolo3 = QLabel()
        self.bolo4 = QLabel()
        self.bolo5 = QLabel()
        self.bolo6 = QLabel()
        self.bolo7 = QLabel()
        self.bolo8 = QLabel()
        self.bolo9 = QLabel()
        self.bolo10 = QLabel()

        # Lista de QLabel
        self.bolosMostrar = [
            self.bolo1,
            self.bolo2,
            self.bolo3,
            self.bolo4,
            self.bolo5,
            self.bolo6,
            self.bolo7,
            self.bolo8,
            self.bolo9,
            self.bolo10
        ]

        # Crear un QGridLayout
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(QMargins(0,0,0,0))
        grid_layout.setSpacing(0)

        # Disposición de los bolos en una matriz de 4 filas y 7 columnas
        pins = [
            (0, 0, "7"),  # Fila 0
            (0, 2, "8"),  # Fila 0
            (0, 4, "9"),  # Fila 0
            (0, 6, "10"),  # Fila 0
            (1, 1, "4"),  # Fila 1
            (1, 3, "5"),  # Fila 1
            (1, 5, "6"),  # Fila 1            (2, 2, "2"),  # Fila 2
            (2, 4, "3"),  # Fila 2
            (3, 3, "1")   # Fila 3
        ]

        # Agregar los bolos a la rejilla
        for x in range(4):  # 4 filas
            for y in range(7):  # 7 columnas
                # Verificar si hay un bolo en la posición actual
                pin_label = next((pin for pin in pins if pin[0] == x and pin[1] == y), None)
                if pin_label:
                    # Obtener el número del bolo
                    bolo_numero = pin_label[2]
                    # Obtener el QLabel correspondiente
                    label =  self.bolosMostrar[int(bolo_numero) - 1]  # Convertir a índice (0-9)
                    
                    # Cargar imagen y escalarla
                    pixmap = QPixmap(f"imagen_{bolo_numero}.png")
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(QSize(50, 50),
                                                     Qt.AspectRatioMode.KeepAspectRatio)
                        label.setPixmap(scaled_pixmap)
                    else:
                        label.setText(f"Image {bolo_numero} not found.")


                    # Configurar el size policy
                    label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                    grid_layout.addWidget(label, x, y)

        # Establecer el layout en el QFrame correspondiente
        self.bolos_frame.setLayout(grid_layout)
        self.bolos_frame.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum) # Hacer que se ajuste a su contenido

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear archivos de imagen ficticios para pruebas
    from PyQt6.QtGui import QColor, QPainter, QImage
    from PyQt6.QtCore import QRect

    for i in range(1, 11):
        image = QImage(100, 100, QImage.Format.Format_RGB32)
        image.fill(QColor(200 + i * 20, 100 + i*20, 100))

        painter = QPainter(image)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(QRect(20,20,80,80), Qt.AlignmentFlag.AlignCenter, f"Imagen {i}")
        painter.end()

        image.save(f"imagen_{i}.png")
    

    main_window = MyWidget()
    main_window.show()

    sys.exit(app.exec())