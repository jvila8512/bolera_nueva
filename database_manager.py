# database_manager.py - DatabaseManager CRUD sobre bolera.db
# Tablas canonicas: usuario y rol. Unifica duplicados usuario/usuarios y rol/roles.
# Depende de config.py (solo para ruta de BD; sin acoplamiento a PLC/UI).

import sqlite3
import os


class DatabaseManager:
    """Gestor de CRUD sobre SQLite (bolera.db).

    Expone tablas canonicas:
      - rol(id_rol, rol)
      - usuario(id_usuario, usuario, contrasena, activo, id_rol, nombre)
    """

    def __init__(self, db_path="bolera.db"):
        self.db_path = db_path
        self.conexion = sqlite3.connect(self.db_path)

    def _connect(self):
        return self.conexion

    def inicializar(self):
        """Crea las tablas canonicas si no existen."""
        conn = self._connect()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rol (
                id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
                rol VARCHAR(100)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario VARCHAR(100),
                contrasena VARCHAR(100),
                activo BOOLEAN,
                id_rol INTEGER REFERENCES rol(id_rol) ON DELETE NO ACTION ON UPDATE NO ACTION,
                nombre VARCHAR
            )
            """
        )
        conn.commit()

    def cerrar(self):
        """Cierra la conexion a la base de datos."""
        if self.conexion:
            self.conexion.close()

    # -------------------- Rol CRUD --------------------

    def crear_rol(self, nombre):
        conn = self._connect()
        cur = conn.execute("INSERT INTO rol (rol) VALUES (?)", (nombre,))
        conn.commit()
        return cur.lastrowid

    def obtener_rol(self, id_rol):
        conn = self._connect()
        cur = conn.execute("SELECT id_rol, rol FROM rol WHERE id_rol = ?", (id_rol,))
        return cur.fetchone()

    def listar_roles(self):
        conn = self._connect()
        cur = conn.execute("SELECT id_rol, rol FROM rol")
        return cur.fetchall()

    def actualizar_rol(self, id_rol, nombre):
        conn = self._connect()
        conn.execute("UPDATE rol SET rol = ? WHERE id_rol = ?", (nombre, id_rol))
        conn.commit()

    def eliminar_rol(self, id_rol):
        conn = self._connect()
        conn.execute("DELETE FROM rol WHERE id_rol = ?", (id_rol,))
        conn.commit()

    # -------------------- Usuario CRUD --------------------

    def crear_usuario(self, usuario, contrasena, activo, id_rol, nombre):
        conn = self._connect()
        cur = conn.execute(
            """
            INSERT INTO usuario (usuario, contrasena, activo, id_rol, nombre)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario, contrasena, activo, id_rol, nombre),
        )
        conn.commit()
        return cur.lastrowid

    def obtener_usuario(self, id_usuario):
        conn = self._connect()
        cur = conn.execute(
            """
            SELECT u.id_usuario, u.usuario, u.contrasena, u.activo,
                   u.id_rol, u.nombre, r.rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = ?
            """,
            (id_usuario,),
        )
        return cur.fetchone()

    def listar_usuarios(self):
        conn = self._connect()
        cur = conn.execute(
            """
            SELECT u.id_usuario, u.usuario, u.contrasena, u.activo,
                   u.id_rol, u.nombre, r.rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            """
        )
        return cur.fetchall()

    def actualizar_usuario(self, id_usuario, usuario, contrasena, activo, id_rol, nombre):
        conn = self._connect()
        conn.execute(
            """
            UPDATE usuario
            SET usuario = ?, contrasena = ?, activo = ?, id_rol = ?, nombre = ?
            WHERE id_usuario = ?
            """,
            (usuario, contrasena, activo, id_rol, nombre, id_usuario),
        )
        conn.commit()

    def eliminar_usuario(self, id_usuario):
        conn = self._connect()
        conn.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        conn.commit()

    def verificar_usuario(self, usuario, contrasena):
        conn = self._connect()
        cur = conn.execute(
            """
            SELECT 1 FROM usuario
            WHERE usuario = ? AND contrasena = ? AND activo = 1
            """,
            (usuario, contrasena),
        )
        return cur.fetchone() is not None

    def tabla_existe(self, nombre_tabla):
        conn = self._connect()
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (nombre_tabla,),
        )
        return cur.fetchone() is not None
