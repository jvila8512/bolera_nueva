from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog
from PyQt6.QtCore import QTimer

class CustomDialog(QDialog):
    def __init__(self, message, dialog_type="warning", parent=None):
        super().__init__(parent)
        self.setWindowTitle(dialog_type.capitalize())

        layout = QVBoxLayout()

        label = QLabel(message)
        layout.addWidget(label)

        self.setLayout(layout)

        # Cierra el diálogo después de 3 segundos
        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(3000)  # 3000 milisegundos = 3 segundos

if __name__ == "__main__":
    app = QApplication([])

    # Ejemplo de uso
    error_message = "¡Ups! Algo salió mal. Verifica tus datos."
    error_dialog = CustomDialog(error_message, "error")
    error_dialog.exec()

    warning_message = "Ten cuidado, esto puede ser peligroso."
    warning_dialog = CustomDialog(warning_message, "warning")
    warning_dialog.exec()
    
    