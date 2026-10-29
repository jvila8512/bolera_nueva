import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,QHeaderView,QAbstractItemView
from PyQt6.QtCore import Qt

from ProbarCodigos.EjemploTelegramProbarCalificacion import JuegoBolos



class MainWindow(QMainWindow):
    def __init__(self, jugadores):
        super().__init__()
        self.setWindowTitle("Resultados de Bolos")

        # Inicializar el juego de bolos
        self.juego = JuegoBolos(jugadores)
        self.resultados = self.juego.calcular_puntuacion()


        #Crear la tabla
        self.tabla = QTableWidget()
        self.setCentralWidget(self.tabla)

        # Configurar la tabla
        self.configurar_tabla()
        self.llenar_tabla()


    def configurar_tabla(self):
        columnas = ['Nombre']
        columnas.extend([f'Ronda {i+1}' for i in range(10)])
        columnas.append("Puntuación Total") #Agregamos la columna de puntuacion total
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)
        self.tabla.setRowCount(len(self.resultados))
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setVisible(True)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)


    def llenar_tabla(self):
        
        for fila, resultado in enumerate(self.resultados):
            nombre_item = QTableWidgetItem(resultado['nombre'])
            self.tabla.setItem(fila, 0, nombre_item)

            puntuacion_acumulada = 0
            for columna, puntuacion_ronda in enumerate(resultado['rondas']):
                op1 = resultado['tiros'][columna]['op1']
                op2 = resultado['tiros'][columna]['op2']
                puntuacion_acumulada += puntuacion_ronda
                if columna < 9:
                    texto = f"{op1}-{op2}={puntuacion_acumulada}"
                else:
                    op3 = resultado['tiros'][columna]['op3']
                    texto = f"{op1}-{op2}-{op3}={puntuacion_acumulada}"
                item = QTableWidgetItem(texto)
                self.tabla.setItem(fila, columna + 1, item)

            # Agregar la puntuación total a la última columna
            total_item = QTableWidgetItem(str(puntuacion_acumulada))
            self.tabla.setItem(fila, 11, total_item) # 11 porque tenemos 10 rondas + nombre


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #Aquí debes colocar tus datos de jugadores, como en el ejemplo anterior.
    jugadores = [
    {
        'nombre': 'Jugador 1',
        'tiros': [
            {'numero_tiro': 1, 'op1': 7, 'op2': 2,'op3':0},  # Strike
            {'numero_tiro': 2, 'op1': 0, 'op2': 10,'op3':0},  # 7 y 2
            {'numero_tiro': 3, 'op1': 8, 'op2':2,'op3':0},  #Spare
            {'numero_tiro': 4, 'op1': 1, 'op2': 2,'op3':0},  #Spare
            {'numero_tiro': 5, 'op1': 1, 'op2': 6,'op3':0},  #Strike
            {'numero_tiro': 6, 'op1': 7, 'op2': 1,'op3':0},  #Strike
            {'numero_tiro': 7, 'op1': 7, 'op2':3,'op3':0},  #Strike 
            {'numero_tiro': 8, 'op1': 8, 'op2':2,'op3':0},  #0
            {'numero_tiro': 9, 'op1': 8, 'op2': 1,'op3':0},  #8 y 2
            {'numero_tiro': 10, 'op1': 10, 'op2': 7,'op3':1},  #Spare + 5
        ]
    },
    {
        'nombre': 'Jugador 2',
        'tiros': [
            {'numero_tiro': 1, 'op1': 10, 'op2': 0,'op3':0},  # Strike
            {'numero_tiro': 2, 'op1': 0, 'op2': 0,'op3':0},  # 7 y 2
            {'numero_tiro': 3, 'op1': 0, 'op2':0,'op3':0},  #Spare
            {'numero_tiro': 4, 'op1': 0, 'op2': 0,'op3':0},  #Spare
            {'numero_tiro': 5, 'op1': 0, 'op2': 0,'op3':0},  #Strike
            {'numero_tiro': 6, 'op1': 0, 'op2': 0,'op3':0},  #Strike
            {'numero_tiro': 7, 'op1': 0, 'op2': 0,'op3':0},  #Strike 
            {'numero_tiro': 8, 'op1': 0, 'op2': 0,'op3':0},  #0
            {'numero_tiro': 9, 'op1': 0, 'op2': 0,'op3':0},  #8 y 2
            {'numero_tiro': 10, 'op1': 0, 'op2': 0,'op3':0},  #Spare + 5
        ]
    }
   
]
    window = MainWindow(jugadores)
    window.show()
    sys.exit(app.exec())