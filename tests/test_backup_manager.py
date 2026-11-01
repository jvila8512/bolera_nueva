# tests/test_backup_manager.py
# Unit / integration tests de BackupManager: backup timestamped + PRAGMA integrity_check.

import os
import sqlite3
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup_manager import BackupManager  # noqa: E402


@pytest.fixture
def db_temporal():
    """Crea una BD SQLite temporal con una tabla y una fila."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE usuario (id INTEGER PRIMARY KEY, usuario TEXT)")
    conn.execute("INSERT INTO usuario (usuario) VALUES ('juan')")
    conn.commit()
    conn.close()
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_crear_backup_archivo_existe(db_temporal, tmp_path):
    bm = BackupManager(db_path=db_temporal, backup_dir=str(tmp_path / "backups"))
    path = bm.crear_backup()
    assert os.path.exists(path)
    assert os.path.getsize(path) > 0
    assert "backup_" in os.path.basename(path)


def test_backup_conserva_datos(db_temporal, tmp_path):
    bm = BackupManager(db_path=db_temporal, backup_dir=str(tmp_path / "backups"))
    path = bm.crear_backup()
    conn = sqlite3.connect(path)
    filas = conn.execute("SELECT usuario FROM usuario").fetchall()
    conn.close()
    assert filas == [("juan",)]


def test_verificar_integridad_ok(db_temporal, tmp_path):
    bm = BackupManager(db_path=db_temporal, backup_dir=str(tmp_path / "backups"))
    assert bm.verificar_integridad() is True


def test_verificar_integridad_archivo_invalido(tmp_path):
    corrupto = tmp_path / "corrupto.db"
    corrupto.write_bytes(b"esto no es una base de datos sqlite")
    bm = BackupManager(db_path=str(corrupto), backup_dir=str(tmp_path / "backups"))
    assert bm.verificar_integridad() is False


def test_backup_con_integridad(db_temporal, tmp_path):
    bm = BackupManager(db_path=db_temporal, backup_dir=str(tmp_path / "backups"))
    resultado = bm.backup_con_integridad()
    assert resultado["integridad_ok"] is True
    assert os.path.exists(resultado["path"])


def test_crear_backup_sin_bd_lanza_error(tmp_path):
    bm = BackupManager(db_path=str(tmp_path / "noexiste.db"), backup_dir=str(tmp_path / "backups"))
    with pytest.raises(FileNotFoundError):
        bm.crear_backup()
