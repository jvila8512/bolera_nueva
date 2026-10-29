import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
class GestionPistas(QDialog):
    def __init__(self):
        super().__init__()
        # Cargar la UI desde el archivo .ui
        uic.loadUi("UI/pistasAdmin.ui", self)
        self.show() 