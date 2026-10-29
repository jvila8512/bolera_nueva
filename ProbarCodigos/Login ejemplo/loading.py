import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QMovie

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        # Crear el widget central y el layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Campo de usuario
        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Campo de contraseña
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Botón de entrar
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.show_loading)
        layout.addWidget(self.login_button)

        # Contenedor para el loading (GIF + texto)
        self.loading_container = QWidget()
        self.loading_container.setVisible(False)  # Ocultar inicialmente
        loading_layout = QHBoxLayout(self.loading_container)

        # Label para el texto "Conectando..."
        self.loading_text = QLabel("Conectando...")
        loading_layout.addWidget(self.loading_text)

        # Label para mostrar el GIF de carga
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(self.loading_label)

        # Cargar el GIF animado
        self.movie = QMovie("loading.gif")  # Asegúrate de tener un archivo GIF en la misma carpeta
        self.loading_label.setMovie(self.movie)

        # Añadir el contenedor de loading al layout principal
        layout.addWidget(self.loading_container)

    def show_loading(self):
        # Ocultar los elementos de login
        self.username_label.setVisible(False)
        self.username_input.setVisible(False)
        self.password_label.setVisible(False)
        self.password_input.setVisible(False)
        self.login_button.setVisible(False)

        # Mostrar el contenedor de loading (GIF + texto)
        self.loading_container.setVisible(True)
        self.movie.start()  # Iniciar la animación del GIF

        # Simular un proceso de carga (por ejemplo, una operación que toma tiempo)
        QTimer.singleShot(5000, self.finish_loading)  # Simular 5 segundos de carga

    def finish_loading(self):
        # Detener el GIF y ocultar el loading
        self.movie.stop()
        self.loading_container.setVisible(False)

        # Restaurar la interfaz de login
        self.username_label.setVisible(True)
        self.username_input.setVisible(True)
        self.password_label.setVisible(True)
        self.password_input.setVisible(True)
        self.login_button.setVisible(True)
        print("Conexión completada")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())