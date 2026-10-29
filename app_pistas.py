import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *

from app_AdminPistas import AdminPistas




class AppPistas1(QDialog):
    def __init__(self):
        super().__init__()
        # Cargar la UI desde el archivo .ui
        self.pista=uic.loadUi("UI/pistas.ui", self)   
        self.pista.initGUI()   
                    
    def initGUI(self):
        self.pushButton.clicked.connect(self.abrirAdminPistas)
    def abrirAdminPistas(self):
        self.dasboard=AdminPistas()
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana principal
    window = AppPistas1()
    window.show()
    
    sys.exit(app.exec())