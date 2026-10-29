from HMI.TemperatureAnalysisWindow import TemperatureAnalysisWindow
import sys
from PyQt6.QtWidgets import QApplication


def main():
    # 1. Primero crear la aplicación QApplication
    app = QApplication(sys.argv)
    
    # 2. Luego crear tu ventana principal
    window = TemperatureAnalysisWindow()
    window.show()
    
    # 3. Ejecutar el bucle principal
    sys.exit(app.exec())

if __name__ == "__main__":
    main()  # Esto asegura el orden correcto de inicialización