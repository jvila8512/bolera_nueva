import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget

from app_AdminPistas import AdminPistas

class Abrir(QWidget):
    def __init__(self):
        super().__init__()
        # Cargar la UI desde el archivo .ui
        uic.loadUi("UI/Abrir.ui", self) 
        self.initGUI()   
                    
    def initGUI(self):
        self.abrir.clicked.connect(self.abrirAdminPistas)
    def abrirAdminPistas(self):
        self.dasboard=AdminPistas()