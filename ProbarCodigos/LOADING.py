import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Cargando...")
        self.setModal(True)
        self.setFixedSize(300, 100)  # Tamaño fijo del diálogo
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Esperando comunicación de...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregamos un estilo moderno al diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
        """)
        
        layout.addWidget(self.label)
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    loading_dialog = LoadingDialog()
    loading_dialog.show()

    # Simular espera
    import time
    time.sleep(5)

    loading_dialog.close()
    
    sys.exit(app.exec())