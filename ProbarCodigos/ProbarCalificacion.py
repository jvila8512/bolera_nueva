import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt

# Datos de ejemplo para múltiples jugadores
jugadores = [
    {
        'nombre': 'Jugador 1',
        'tiros': [
            {'numero_tiro': 1, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 2, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 3, 'op1': 3, 'op2': 5},   # Spare
            {'numero_tiro': 4, 'op1': 2, 'op2': 6},   # Normal
            {'numero_tiro': 5, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 6, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 7, 'op1': 4, 'op2': 5},   # Normal
            {'numero_tiro': 8, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 9, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 10, 'op1': 10, 'op2': 0}   # Strike
        ]
    },
    {
        'nombre': 'Jugador 2',
        'tiros': [
            {'numero_tiro': 1, 'op1': 7, 'op2': 3},   # Spare
            {'numero_tiro': 2, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 3, 'op1': 2, 'op2': 8},   # Spare
            {'numero_tiro': 4, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 5, 'op1': 5, 'op2': 5},   # Spare
            {'numero_tiro': 6, 'op1': 4, 'op2': 4},   # Normal
            {'numero_tiro': 7, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 8, 'op1': 3, 'op2': 7},   # Normal
            {'numero_tiro': 9, 'op1': 10, 'op2': 0},  # Strike
            {'numero_tiro': 10, 'op1': 10, 'op2': 0}   # Strike
        ]
    }
]

def calcular_puntuacion(tiros):
    puntuacion_total = 0
    resultados = []

    for i in range(len(tiros)):
        tiro = tiros[i]
        if tiro['op1'] == 10:  # Strike
            total_tiro = 10
            if i + 1 < len(tiros):
                total_tiro += tiros[i + 1]['op1']  # Sumar el siguiente tiro
                if i + 1 < len(tiros) and tiros[i + 1]['op1'] == 10 and i + 2 < len(tiros):
                    total_tiro += tiros[i + 2]['op1']  # Sumar el segundo tiro si el primero es otro strike
                else:
                    total_tiro += tiros[i + 1]['op2']  # Sumar el segundo tiro
            resultado = f"{tiro['op1']} - {tiro['op2']} = {total_tiro}"
        elif tiro['op1'] + tiro['op2'] == 10:  # Spare
            total_tiro = 10
            if i + 1 < len(tiros):
                total_tiro += tiros[i + 1]['op1']  # Sumar el siguiente tiro
            resultado = f"{tiro['op1']} - {tiro['op2']} = {total_tiro}"
        else:  # Tiro normal
            total_tiro = tiro['op1'] + tiro['op2']
            resultado = f"{tiro['op1']} - {tiro['op2']} = {total_tiro}"

        puntuacion_total += total_tiro
        resultados.append(resultado)

    return puntuacion_total, resultados

class ScoreDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resultados de Puntuación")
        self.setGeometry(100, 100, 800, 400)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.refresh_button = QPushButton("Calcular Puntuación")
        self.refresh_button.clicked.connect(self.mostrar_resultados)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        # Aplicar estilo CSS moderno
        self.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: transparent;
            }
            QTableWidget::item {
                border: 1px solid #ccc;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.8);
            }
            QHeaderView::section {
                background-color: #4CAF50; /* Color de fondo del encabezado */
                color: white; /* Color del texto del encabezado */
                padding: 10px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def mostrar_resultados(self):
        # Configurar la tabla
        self.table.setRowCount(len(jugadores))
        self.table.setColumnCount(12)  # 10 tiros + 1 para la puntuación + 1 para resultados
        self.table.setHorizontalHeaderLabels(["Jugador", "Tiro 1", "Tiro 2", "Tiro 3", "Tiro 4", "Tiro 5",
                                               "Tiro 6", "Tiro 7", "Tiro 8", "Tiro 9", "Tiro 10", "Puntuación"])

        for i, jugador in enumerate(jugadores):
            self.table.setItem(i, 0, QTableWidgetItem(jugador['nombre']))  # Nombre del jugador
            puntuacion_total, resultados = calcular_puntuacion(jugador['tiros'])

            for j in range(len(jugador['tiros'])):
                tiro = jugador['tiros'][j]
                # Mostrar el resultado del tiro
                self.table.setItem(i, j + 1, QTableWidgetItem(f"{tiro['op1']} - {tiro['op2']}"))

            # Mostrar puntuación total en la última columna
            self.table.setItem(i, 11, QTableWidgetItem(str(puntuacion_total)))

        self.table.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ScoreDialog()
    dialog.show()
    sys.exit(app.exec())