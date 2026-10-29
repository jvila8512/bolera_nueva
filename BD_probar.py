from ConexionBD.conexion import Conexion
import bcrypt

class ProbarConexion:
    def __init__(self, db_name):
        self.con = Conexion(db_name)  # Asegúrate de pasar el nombre de la base de datos

        sql = """
        SELECT u.*, r.rol
        FROM usuario u
        JOIN rol r ON u.id_usuario = r.id_rol
        """
        sql2="""
        SELECT
        id_usuario, usuario, contrasena, nombre, activo, r.rol FROM usuario JOIN rol r ON usuario.id_usuario = r.id_rol 
        """
        
        sql1="INSERT INTO usuario (nombre, usuario, contrasena, id_rol, activo) VALUES (?, ?, ?, ?, ?)"
        contrasena="123"
        
          # Encriptar la contraseña
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

       # self.con.ejecutar_sql(sql1,("Javier Vila Labrada","javiervl",hashed_contrasena,1,1))
        respuesta = self.con.obtener_usuario_por_id(23)

        if isinstance(respuesta, str):  # Si es un string, es un mensaje de error
            print(respuesta)
        else:
           #for fila in respuesta:  # Imprimir cada fila de resultados
             print(respuesta)
             
             self.con.cerrar_conexion
        
# Ejemplo de uso
if __name__ == "__main__":
    db_name = './bolera.db'  # Cambia esto por el nombre de tu base de datos
    prueba = ProbarConexion(db_name)