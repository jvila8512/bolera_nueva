class JuegoBolos:
    def __init__(self, jugadores):
        self.jugadores = jugadores

    def calcular_puntuacion(self):
        resultados = []
        for jugador in self.jugadores:
            nombre = jugador['nombre']
            tiros = jugador['tiros']
            puntuacion_total = 0
            puntuacion_ronda = []

            for i in range(len(tiros)):
                op1 = tiros[i]['op1']
                op2 = tiros[i]['op2']
                op3 = tiros[i]['op3']

                if i == 9:  # Ronda 10: Manejo especial
                    puntuacion_ronda.append(op1 + op2 + op3) # Suma los tres tiros de la ronda 10
                elif op1 == 10:  # Strike
                    puntuacion_ronda.append(10)
                    if i < len(tiros) - 1: 
                        next_op1 = tiros[i+1]['op1']
                        next_op2 = tiros[i+1]['op2']
                        if i < len(tiros)-2:
                            next_next_op1 = tiros[i+2]['op1']
                        else:
                            next_next_op1 = 0 # No hay siguiente siguiente tiro
                        puntuacion_ronda[-1] += next_op1 + next_op2 #Agrega puntos de los siguientes 2 tiros
                        if next_op1 == 10:
                            puntuacion_ronda[-1] += next_next_op1
                            
                elif op1 + op2 == 10:  # Spare
                    puntuacion_ronda.append(10 + tiros[i + 1]['op1'])
                else:
                    puntuacion_ronda.append(op1 + op2)

            puntuacion_total = sum(puntuacion_ronda)
            resultados.append({
                'nombre': nombre,
                'puntuacion': puntuacion_total,
                'rondas': puntuacion_ronda,
                'tiros': tiros
            })
        return resultados

    def mostrar_resultados(self):
        resultados = self.calcular_puntuacion()
        for resultado in resultados:
            print(f"Jugador: {resultado['nombre']}")
            puntuacion_acumulada = 0
            for i, puntuacion_ronda in enumerate(resultado['rondas']):
                op1 = resultado['tiros'][i]['op1']
                op2 = resultado['tiros'][i]['op2']
                puntuacion_acumulada += puntuacion_ronda  #Acumula la puntuación
                if i < 9:
                    print(f"  Ronda {i + 1}: {op1} y {op2} = {puntuacion_acumulada}")
                else:  # Ronda 10
                    op3 = resultado['tiros'][i]['op3']
                    print(f"  Ronda {i + 1}: {op1}, {op2}, y {op3} = {puntuacion_acumulada}")
            print(f"  Puntuación Total: {puntuacion_acumulada}\n")
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

juego = JuegoBolos(jugadores)
juego.mostrar_resultados()