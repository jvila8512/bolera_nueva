

import sqlite3
from ConexionBD.conexion import Conexion


class JuegoBD_operaciones:
    def __init__(self):
        
        # Conectar a la base de datos  
        self.con = Conexion('./bolera.db')  
        self.conexion = self.con.devolverConexion()
        self.cursor = self.conexion.cursor()        
     
    def obtenerDeJuegoJugadoresTiros(self,id_juego):
         
      try: 
          self.cursor.execute("""  SELECT j.nombre, t.numero_tiro, t.op1, t.op2, t.op3
            FROM jugadores j
            INNER JOIN tiros t ON j.id_jugadores = t.id_jugador
            WHERE j.id_juego = ?
            ORDER BY j.id_jugadores, t.numero_tiro""", (id_juego,))
          resultados=self.cursor.fetchall()
          jugadores = []
          jugador_actual = None
          datos_jugador = {'nombre': None, 'tiros': []}


          for fila in resultados:
               nombre, numero_tiro, op1, op2, op3 = fila
               if nombre != jugador_actual:
                    # Nuevo jugador
                    if jugador_actual is not None:
                         jugadores.append(datos_jugador)
                    jugador_actual = nombre
                    datos_jugador = {'nombre': nombre, 'tiros': []}

               datos_jugador['tiros'].append({
                    'numero_tiro': numero_tiro,
                    'op1': op1,
                    'op2': op2,
                    'op3': op3
               })

          # Agregar el último jugador
          jugadores.append(datos_jugador)       
         
          return jugadores
      except sqlite3.Error as e:
        mensaje=f"Error al acceder a la base de datos: {e}"
        return mensaje
              
         
    def insertarJuego(self,  parametros,listaJugadores):
      
       try:
      
        resp=self.cursor.execute("INSERT INTO juego (id_tiempo,fecha,id_usuario,id_precio,id_tipo_juego,activo,cant_jugadores,pista) VALUES (?,?,?,?,?,?,?,?)",parametros)
        ultimo_id = self.cursor.lastrowid
        #self.conexion.commit()
        # Inserta cada jugador en la tabla
        for jugador in listaJugadores:
            name = jugador[0]
            is_menor = jugador[1]    
            self.cursor.execute("INSERT INTO jugadores (nombre, op_menor, id_juego) VALUES (?, ?, ?)", (name, is_menor, ultimo_id))
            ultimo_idJugador = self.cursor.lastrowid
            for i in range(10):
               self.cursor.execute("INSERT INTO tiros (numero_tiro,op1,op2,op3, id_jugador) VALUES (?,?, ?, ?,?)", (i+1,0, 0,0,ultimo_idJugador))
        
        
        # Confirmar los cambios y cerrar la conexión
        self.conexion.commit()
        self.cursor.close()
        self.conexion.close()
        return ultimo_id
       except sqlite3.OperationalError as e:
            return f"Error de operación: {e}"
       except sqlite3.IntegrityError as e:
           return f"Error de integridad: {e}"
       except sqlite3.ProgrammingError as e:
            return f"Error de programación: {e}"
       except sqlite3.DatabaseError as e:
            return f"Error en la base de datos: {e}"
       except sqlite3.DataError as e:
            return f"Error de datos: {e}"
       except sqlite3.NotSupportedError as e:
            return f"Error no soportado: {e}"
       except sqlite3.InterfaceError as e:
            return f"Error de interfaz: {e}"
       except sqlite3.InternalError as e:
            return f"Error interno: {e}"
       except Exception as e:
            return f"Error inesperado: {e}"