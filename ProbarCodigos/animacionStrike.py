import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import QTimer, Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QLabel con Animación CSS")
        self.setGeometry(100, 100, 300, 200)  # Ajusta el tamaño si necesitas

        self.label = QLabel("STrike", self)
        self.label.setStyleSheet("""
            QLabel {
                color: red;
                animation: blink 1s linear infinite; /* Animación de parpadeo */
            }

            @keyframes blink {
                0% { opacity: 1; }
                50% { opacity: 0; }
                100% { opacity: 1; }
            }
        """)

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centra el texto
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())