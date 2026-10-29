
import sqlite3

def mostrar_resultados_tiros(id_juego):
   
    try:
        conn = sqlite3.connect('./bolera.db')  # Reemplaza 'base_de_datos.db' si es necesario
        cursor = conn.cursor()

        cursor.execute("""
            SELECT j.nombre, t.numero_tiro, t.op1, t.op2, t.op3
            FROM jugadores j
            INNER JOIN tiros t ON j.id_jugadores = t.id_jugador
            WHERE j.id_juego = ?
            ORDER BY j.id_jugadores, t.numero_tiro
        """, (id_juego,))

        resultados = cursor.fetchall()

        jugador_actual = None
        tiros_jugador = []

        for fila in resultados:
            nombre, numero_tiro, op1, op2, op3 = fila
            if nombre != jugador_actual:
                # Nuevo jugador, imprimimos los tiros del jugador anterior
                if jugador_actual is not None:
                    imprimir_tiros_jugador(jugador_actual, tiros_jugador)

                jugador_actual = nombre
                tiros_jugador = []
            tiros_jugador.append( (numero_tiro, op1, op2, op3) )

        # Imprimimos los tiros del último jugador

        if jugador_actual is not None:
            imprimir_tiros_jugador(jugador_actual, tiros_jugador)

        conn.close()

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")

def imprimir_tiros_jugador(nombre_jugador, tiros):
    """Imprime los tiros de un jugador de forma formateada."""
    print(f"\nJugador: {nombre_jugador}")
    for numero_tiro, op1, op2, op3 in tiros:
        print(f"  Tiro {numero_tiro}: Op1={op1}, Op2={op2}, Op3={op3}")



if __name__ == "__main__":
    id_juego_a_mostrar = 7  # Reemplaza con el ID del juego que quieres mostrar
    mostrar_resultados_tiros(id_juego_a_mostrar)



