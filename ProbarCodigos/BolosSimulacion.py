from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt6.QtCore import Qt
class BowlingPinsApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ubicación de los Bolos")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.create_bowling_pins()

    def create_bowling_pins(self):
        # Crear un grid layout para ubicar los bolos
        grid_layout = QGridLayout()
        # Disposición de los bolos en una matriz de 7 columnas y 4 filas
        pins = [
            (0, 0, "7"),  # Fila 0
            (0, 2, "8"),  # Fila 0
            (0, 4, "9"),  # Fila 0
            (0, 6, "10"),  # Fila 0
            
            (1, 1, "4"),  # Fila 1
            (1, 3, "5"),  # Fila 1
            (1, 5, "6"),  # Fila 1
            (2, 2, "2"),  # Fila 2
            (2, 4, "3"),  # Fila 2
            (3, 3, "1")   # Fila 3
        ]

        # Agregar los bolos a la rejilla
        for x in range(4):  # 4 filas
            for y in range(7):  # 7 columnas
                # Verificar si hay un bolo en la posición actual
                pin_label = next((pin for pin in pins if pin[0] == x and pin[1] == y), None)
                if pin_label:
                    # Si hay un bolo, crear la etiqueta con el número del bolo
                    label = QLabel(pin_label[2])
                    label.setStyleSheet("color: rgb(255, 255, 255);  background-color: rgba(200, 0, 0, 255); border-radius: 20px; padding: 20px; text-align: center;")
                
                grid_layout.addWidget(label, x, y)

        self.layout.addLayout(grid_layout)


     

if __name__ == "__main__":
    app = QApplication([])
    window = BowlingPinsApp()
    window.show()
    app.exec()
