import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,QTableWidget, QTableWidgetItem, QLineEdit, QDialog, QLabel, QFormLayout, QMessageBox


class UsuarioDialog(QDialog):
    def __init__(self, usuario=None):
        super().__init__()
        self.setWindowTitle("Formulario de Usuario")
        
        self.layout = QFormLayout(self)
        
        self.nombre_input = QLineEdit()
        self.email_input = QLineEdit()
        
        self.layout.addRow(QLabel("Nombre:"), self.nombre_input)
        self.layout.addRow(QLabel("Email:"), self.email_input)
        
        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_usuario)
        self.layout.addWidget(self.boton_guardar)
        
        if usuario:
            self.nombre_input.setText(usuario[1])
            self.email_input.setText(usuario[2])
            self.usuario_id = usuario[0]
        else:
            self.usuario_id = None

    def guardar_usuario(self):
        nombre = self.nombre_input.text()
        email = self.email_input.text()
        
        if self.usuario_id:
            # Actualizar usuario
            self.actualizar_usuario(self.usuario_id, nombre, email)
        else:
            # Insertar nuevo usuario
            self.insertar_usuario(nombre, email)

    def insertar_usuario(self, nombre, email):
        conn = sqlite3.connect('mi_base_de_datos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, email) VALUES (?, ?)', (nombre, email))
        conn.commit()
        conn.close()
        self.accept()

    def actualizar_usuario(self, usuario_id, nombre, email):
        conn = sqlite3.connect('mi_base_de_datos.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET nombre=?, email=? WHERE id=?', (nombre, email, usuario_id))
        conn.commit()
        conn.close()
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD de Usuarios")
        
        self.layout = QVBoxLayout()
        
        self.boton_nuevo = QPushButton("Nuevo Usuario")
        self.boton_nuevo.clicked.connect(self.nuevo_usuario)
        
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_usuario)

        self.filtro_input = QLineEdit()
        self.filtro_input.setPlaceholderText("Buscar por nombre o email")
        
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(3)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Nombre", "Email"])
        
        self.layout.addWidget(self.filtro_input)
        self.layout.addWidget(self.boton_buscar)
        self.layout.addWidget(self.boton_nuevo)
        self.layout.addWidget(self.tabla_usuarios)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        conn = sqlite3.connect('./bolera.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario')
        usuarios = cursor.fetchall()
        conn.close()

        self.tabla_usuarios.setRowCount(len(usuarios))
        for row, usuario in enumerate(usuarios):
            for column, data in enumerate(usuario):
                self.tabla_usuarios.setItem(row, column, QTableWidgetItem(str(data)))

    def nuevo_usuario(self):
        dialog = UsuarioDialog()
        if dialog.exec():
            self.cargar_usuarios()

    def buscar_usuario(self):
        filtro = self.filtro_input.text()
        conn = sqlite3.connect('./bolera.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE nombre LIKE ? OR usuario LIKE ?', 
                       ('%' + filtro + '%', '%' + filtro + '%'))
        usuarios = cursor.fetchall()
        conn.close()

        self.tabla_usuarios.setRowCount(len(usuarios))
        for row, usuario in enumerate(usuarios):
            for column, data in enumerate(usuario):
                self.tabla_usuarios.setItem(row, column, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())