import sys
from PyQt6.QtWidgets import  QApplication,QDialog
from PyQt6.QtCore import Qt

from UI.tv1 import TV1




class AnimacionTV1(QDialog):
     def __init__(self):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        self.ui = TV1()      
        self.ui.setupUi(self)  
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Mostrar el diálogo maximizado
        self.showMaximized()  
              
 #if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # window =AnimacionStrike()
    # window.show()
    # sys.exit(app.exec())