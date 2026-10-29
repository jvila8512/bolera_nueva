# conexion.py
import sqlite3

import bcrypt

from bd_modelos.usuario import Usuario



class Conexion:
    def __init__(self, db_name="bolera.db"):
        self.db_name = db_name
        self.conexion = sqlite3.connect(self.db_name)
        self.cursor = self.conexion.cursor()        
       # self._crear_tabla()       
        

    def _crear_tabla(self):
        try:
          
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            if self.conexion:
                self.conexion.close()
    def devolverConexion(self):
        return self.conexion
    def verificar_usuario(self, usuario, contrasena):
      try:
        cursor = self.conexion.cursor()
        # Obtener el hash de la contraseña del usuario
        cursor.execute('''
            SELECT contrasena FROM usuario WHERE usuario = ? AND activo = 1
        ''', (usuario,))
        resultado = cursor.fetchone()

        if resultado is not None:
            # resultado[0] contiene el hash de la contraseña
            hashed_contrasena = resultado[0]
            # Verificar la contraseña ingresada con el hash almacenado
            if bcrypt.checkpw(contrasena.encode('utf-8'), hashed_contrasena):
                return resultado  # La contraseña es correcta
            else:
                return False  # La contraseña es incorrecta
        else:
            return False  # El usuario no existe
      except sqlite3.Error as e:
        print(f"Error al verificar el usuario: {e}")
        return False
                
    def obtener_usuario_por_id(self, usuario_id):
        sql = """
        SELECT u.*,r.rol
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        
        WHERE u.id_usuario = ?
        """
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql,(usuario_id,))
            resultados = cursor.fetchone()  # Obtiene todos los resultados
            return resultados  # Devuelve los resultados
        except sqlite3.Error as e:
            return f"Error al obtener usuarios con roles: {e}"
        finally:
            cursor.close()          
    def ejecutar_sql(self, sql, parametros=None):
        self.respuesta= None
        try:
            cursor = self.conexion.cursor()
            if parametros:
               cursor.execute(sql, parametros)
               self.respuesta= cursor.fetchall() 
            else:
              cursor.execute(sql)
              self.respuesta  =cursor.fetchall() 
            
           
            self.conexion.commit()  # Si realizas un cambio, asegúrate de guardar
            
            
            return self.respuesta  # Indica que no hubo error
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
       
    def devolverUsuario(self, usuario, contrasena): 
         # Encriptar la contraseña
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        cursor1 = self.conexion.cursor()
        cursor1.execute("""
           SELECT u.*,r.rol
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol WHERE usuario = ?  AND activo = 1
        """, (usuario,))
        respuesta = cursor1.fetchone() 
        #print(respuesta)
        userLogueado = Usuario(respuesta[0], respuesta[1], respuesta[2], respuesta[3], respuesta[4], respuesta[5], respuesta[6])
        
       
        return userLogueado
            
       
    def cerrar_conexion(self):
        self.conexion.close()