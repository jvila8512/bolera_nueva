import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
class AdminPistas(QDialog):
    def __init__(self):
        super().__init__()
        # Cargar la UI desde el archivo .ui
        uic.loadUi("UI/pistasDialog.ui", self)
        self.show() 