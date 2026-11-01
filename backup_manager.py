# backup_manager.py - BackupManager para respaldos de bolera.db
# Crea copias con timestamp y valida integridad con PRAGMA integrity_check.
# Sin acoplamiento a PLC/UI.

import os
import sqlite3
from datetime import datetime


class BackupManager:
    """Gestiona respaldos timestamped de una base SQLite y su verificacion."""

    def __init__(self, db_path="bolera.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    def crear_backup(self):
        """Crea un respaldo consistente de la BD y devuelve su ruta.

        Usa la API de backup de sqlite3 (snapshot consistente) y deja el archivo
        en backup_dir con nombre <db>_backup_<timestamp>.db.
        """
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"No se encuentra la base de datos: {self.db_path}")

        os.makedirs(self.backup_dir, exist_ok=True)
        nombre = os.path.splitext(os.path.basename(self.db_path))[0]
        backup_path = os.path.join(self.backup_dir, f"{nombre}_backup_{self._timestamp()}.db")

        origen = sqlite3.connect(self.db_path)
        destino = sqlite3.connect(backup_path)
        try:
            origen.backup(destino)
        finally:
            destino.close()
            origen.close()

        return backup_path

    def verificar_integridad(self, db_path=None):
        """Devuelve True si PRAGMA integrity_check == 'ok'; False si hay error."""
        db_path = db_path if db_path is not None else self.db_path
        if not os.path.exists(db_path):
            return False
        conexion = None
        try:
            conexion = sqlite3.connect(db_path)
            resultado = conexion.execute("PRAGMA integrity_check").fetchone()
            return bool(resultado) and resultado[0] == "ok"
        except sqlite3.DatabaseError:
            return False
        finally:
            if conexion is not None:
                conexion.close()

    def backup_con_integridad(self):
        """Crea el respaldo y verifica su integridad. Devuelve dict con path y estado."""
        path = self.crear_backup()
        return {"path": path, "integridad_ok": self.verificar_integridad(path)}
