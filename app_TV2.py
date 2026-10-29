import sys
from PyQt6.QtWidgets import  QApplication,QDialog
from PyQt6.QtCore import Qt

from UI.tv2 import TV2




class AnimacionTV2(QDialog):
     def __init__(self):
        super().__init__()         
        # Initialize the UI from the generated 'main_ui' class
        self.ui = TV2()      
        self.ui.setupUi(self)  
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Mostrar el diálogo maximizado
        self.showMaximized()  
              
 #if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # window =AnimacionStrike()
    # window.show()
    # sys.exit(app.exec())