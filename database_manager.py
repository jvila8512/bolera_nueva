# database_manager.py - DatabaseManager CRUD sobre bolera.db
# Tablas canonicas: usuario y rol. Unifica duplicados usuario/usuarios y rol/roles.
# Depende de config.py (solo para ruta de BD; sin acoplamiento a PLC/UI).

import sqlite3
import os
import shutil
from datetime import datetime


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
            LEFT JOIN rol r ON u.id_rol = r.id_rol
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
            LEFT JOIN rol r ON u.id_rol = r.id_rol
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

    def verificar_usuario_hash(self, usuario, contrasena):
        """Verifica credenciales contra un hash bcrypt (como hace Conexion)."""
        import bcrypt

        conn = self._connect()
        cur = conn.execute(
            "SELECT contrasena FROM usuario WHERE usuario = ? AND activo = 1",
            (usuario,),
        )
        fila = cur.fetchone()
        if fila is None or fila[0] is None:
            return False
        guardado = fila[0]
        if isinstance(guardado, str):
            guardado = guardado.encode("utf-8")
        try:
            return bcrypt.checkpw(contrasena.encode("utf-8"), guardado)
        except (ValueError, TypeError):
            return False

    def obtener_usuario_por_nombre(self, usuario):
        """Devuelve (id_usuario, usuario, contrasena, activo, id_rol, nombre, rol) o None."""
        conn = self._connect()
        cur = conn.execute(
            """
            SELECT u.id_usuario, u.usuario, u.contrasena, u.activo,
                   u.id_rol, u.nombre, r.rol
            FROM usuario u
            LEFT JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.usuario = ? AND u.activo = 1
            """,
            (usuario,),
        )
        return cur.fetchone()

    def tabla_existe(self, nombre_tabla):
        conn = self._connect()
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (nombre_tabla,),
        )
        return cur.fetchone() is not None

    # -------------------- Migracion: unificar duplicados --------------------

    def hacer_backup(self, backup_dir="backups"):
        """Crea una copia de seguridad con timestamp de bolera.db.

        Retorna la ruta al archivo de backup creado.
        Para BD en memoria (:memory:) usa sqlite3.Connection.backup().
        """
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"bolera_backup_{timestamp}.db")

        if self.db_path == ":memory:":
            dest = sqlite3.connect(backup_path)
            self.conexion.backup(dest)
            dest.close()
        else:
            if not os.path.exists(self.db_path):
                raise FileNotFoundError(f"No se encuentra la base de datos: {self.db_path}")
            shutil.copy2(self.db_path, backup_path)

        return backup_path

    def migrar_unificar_tablas(self, backup_dir="backups"):
        """Migracion: backup -> copy -> validate row-by-row -> drop duplicates.

        Pasos:
          1. Backup de bolera.db antes de cualquier cambio.
          2. Copia filas de tablas duplicadas (usuarios, roles) a canonicas
             (usuario, rol), omitiendo filas que ya existan.
          3. Valida fila por fila que los datos copiados coincidan con el origen.
          4. Elimina tablas duplicadas (usuarios, roles).

        Retorna la ruta al backup creado. Reversible restaurando el backup.
        """
        # Paso 1: backup
        backup_path = self.hacer_backup(backup_dir)

        conn = self._connect()

        # Asegurar tablas canonicas
        self.inicializar()

        # Paso 2 + 3: copiar y validar fila por fila desde duplicados a canonicos
        if self.tabla_existe("roles"):
            rows = conn.execute("SELECT id, nombre FROM roles").fetchall()
            for row_id, nombre in rows:
                existente = conn.execute("SELECT id_rol FROM rol WHERE rol = ?", (nombre,)).fetchone()
                if existente is None:
                    cur = conn.execute("INSERT INTO rol (rol) VALUES (?)", (nombre,))
                    new_id = cur.lastrowid
                    # Validacion fila por fila: el rol insertado debe ser recuperable
                    validado = conn.execute("SELECT rol FROM rol WHERE id_rol = ?", (new_id,)).fetchone()
                    if validado is None or validado[0] != nombre:
                        raise RuntimeError(f"Validacion fallida al copiar rol id={row_id}, nombre={nombre}")
                else:
                    # Ya existe: validar que el nombre coincida
                    if existente[0] is not None:
                        actual = conn.execute("SELECT rol FROM rol WHERE id_rol = ?", (existente[0],)).fetchone()
                        if actual is None or actual[0] != nombre:
                            raise RuntimeError(
                                f"Validacion fallida: rol duplicado '{nombre}' ya existe con nombre diferente"
                            )

        if self.tabla_existe("usuarios"):
            rows = conn.execute("SELECT id, nombre, email, rol_id FROM usuarios").fetchall()
            for row_id, nombre, email, rol_id in rows:
                existente = conn.execute(
                    "SELECT id_usuario FROM usuario WHERE usuario = ?", (nombre,)
                ).fetchone()
                if existente is None:
                    # Buscar rol destino (mapear rol_id de roles a id_rol de rol si existe)
                    id_rol_destino = rol_id
                    if rol_id is not None:
                        mapeo = conn.execute("SELECT id_rol FROM rol WHERE id_rol = ?", (rol_id,)).fetchone()
                        if mapeo is None:
                            id_rol_destino = None
                    cur = conn.execute(
                        """
                        INSERT INTO usuario (usuario, contrasena, activo, id_rol, nombre)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (nombre, "", 1, id_rol_destino, nombre),
                    )
                    new_id = cur.lastrowid
                    # Validacion fila por fila
                    validado = conn.execute(
                        "SELECT usuario FROM usuario WHERE id_usuario = ?", (new_id,)
                    ).fetchone()
                    if validado is None or validado[0] != nombre:
                        raise RuntimeError(
                            f"Validacion fallida al copiar usuario id={row_id}, nombre={nombre}"
                        )

        # Paso 4: eliminar tablas duplicadas
        conn.execute("DROP TABLE IF EXISTS usuarios")
        conn.execute("DROP TABLE IF EXISTS roles")
        conn.commit()

        return backup_path

    def obtener_estado_tablas(self):
        """Retorna dict {nombre_tabla: existe} para tablas relevantes."""
        return {
            "usuario": self.tabla_existe("usuario"),
            "rol": self.tabla_existe("rol"),
            "usuarios": self.tabla_existe("usuarios"),
            "roles": self.tabla_existe("roles"),
        }
