from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox,QDialog

from dasboard.DasBoard import MainWindow




class MainWindow1(QMainWindow):
    def __init__(self):
      
        self.dasbord= MainWindow() 
        self.dasbord.showMaximized()    
        
       
