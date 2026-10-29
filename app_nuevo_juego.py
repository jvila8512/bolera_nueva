
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog




class NuevoJuego(QDialog):
    def __init__(self):
        super().__init__()
        # Cargar la UI desde el archivo .ui
        uic.loadUi("UI/nuevo_juego.ui", self)      
        self.show()       
      
