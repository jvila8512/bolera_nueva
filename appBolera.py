from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox,QDialog

import AppLogin

class LoginApp(QMainWindow):
    def __init__(self):
        self.app=QApplication([])
        self.login= AppLogin.LoginWindow()
        self.app.exec()
       
