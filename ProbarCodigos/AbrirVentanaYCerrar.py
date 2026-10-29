import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton('Abrir/Cerrar Ventana')
        self.button.clicked.connect(self.toggle_window)

        layout = QVBoxLayout()
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.sub_window = None  # Inicializamos la sub-ventana como None

    def toggle_window(self):
        if self.sub_window is None or not self.sub_window.isVisible():
            # Si la sub-ventana no existe o no es visible, la creamos y mostramos
            self.sub_window = SubWindow()
            self.sub_window.show()
        else:
            # Si la sub-ventana es visible, la cerramos
            self.sub_window.close()
            self.sub_window = None  # Restablecemos a None

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sub Ventana')
        self.setGeometry(150, 150, 200, 100)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Esta es una sub-ventana'))
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

