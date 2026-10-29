
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLineEdit, QCheckBox, 
    QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class CRUDApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CRUD Local")
        self.setGeometry(100, 100, 450, 300)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Jugador", "Nombre", "Menor de Edad", "Acciones"])
        
        self.layout.addWidget(self.table)

        self.name_input = QLineEdit(self)
        self.layout.addWidget(self.name_input)

        self.age_checkbox = QCheckBox("Menor de Edad", self)
        self.layout.addWidget(self.age_checkbox)

        self.btn_add = QPushButton("Agregar", self)
        self.btn_add.clicked.connect(self.add_entry)
        self.layout.addWidget(self.btn_add)

        self.setLayout(self.layout)

        # Apply styles
        self.apply_styles()

    def apply_styles(self):
        # CSS para la tabla
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #333;
                font-family: Arial, sans-serif;
                font-size: 14px;
                background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)

        # CSS para los botones
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

    def add_entry(self):
        name = self.name_input.text().strip()
        is_minor = self.age_checkbox.isChecked()
        
        if name:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            player_label = f"Jugador {row_position + 1}"
            self.table.setItem(row_position, 0, QTableWidgetItem(player_label))
            self.table.setItem(row_position, 1, QTableWidgetItem(name))
            self.table.setItem(row_position, 2, QTableWidgetItem("Sí" if is_minor else "No"))
            
            # Agregar botones de editar y eliminar en un layout horizontal
            action_layout = QHBoxLayout()
            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda checked, row=row_position: self.edit_entry(row))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(lambda checked, row=row_position: self.delete_entry(row))
            action_layout.addWidget(delete_button)

            # Crear un widget contenedor para el layout de acciones
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row_position, 3, action_widget)

            self.name_input.clear()
            self.age_checkbox.setChecked(False)
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un nombre.")

    def edit_entry(self, row):
        # Obtener el nombre actual y el estado de menor de edad
        name_item = self.table.item(row, 1)
        is_minor_item = self.table.item(row, 2)
      # Poner el nombre y el estado en los inputs
        self.name_input.setText(name_item.text())
        self.age_checkbox.setChecked(is_minor_item.text() == "Sí")

        # Actualizar el botón para modificar la fila
        self.btn_add.clicked.disconnect()  # Desconectar el actual
        self.btn_add.clicked.connect(lambda: self.save_entry(row))  # Guardar cambios

    def save_entry(self, row):
        name = self.name_input.text().strip()
        is_minor = self.age_checkbox.isChecked()
        
        if name:
            self.table.item(row, 1).setText(name)
            self.table.item(row, 2).setText("Sí" if is_minor else "No")
            self.name_input.clear()
            self.age_checkbox.setChecked(False)
            
            # Volver a conectar el botón agregar
            self.btn_add.clicked.disconnect()
            self.btn_add.clicked.connect(self.add_entry)
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un nombre.")

    def delete_entry(self, row):
        self.table.removeRow(row)
        for r in range(row, self.table.rowCount()):
            player_item = self.table.item(r, 0)
            if player_item:
                player_item.setText(f"Jugador {r + 1}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec())    