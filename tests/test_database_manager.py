# tests/test_database_manager.py
# Unit tests: DatabaseManager CRUD + migration
# - sqlite in-memory (fast, isolated)
# - bolera.db copy (real schema validation)

import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_manager import DatabaseManager  # noqa: E402


# -------------------- Fixtures --------------------


@pytest.fixture
def db_mem():
    """DatabaseManager sobre sqlite en memoria (nuevo por test)."""
    db = DatabaseManager(":memory:")
    db.inicializar()
    yield db
    db.cerrar()


@pytest.fixture
def db_bolera_copy():
    """DatabaseManager sobre una copia de bolera.db (isolada, se borra al final)."""
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bolera.db")
    fd, dst = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    shutil.copy2(src, dst)
    db = DatabaseManager(dst)
    db.inicializar()
    yield db
    db.cerrar()
    os.remove(dst)


# -------------------- Rol CRUD --------------------


def test_crear_obtener_listar_rol(db_mem):
    rid = db_mem.crear_rol("admin")
    assert rid is not None and rid > 0

    rol = db_mem.obtener_rol(rid)
    assert rol is not None
    assert rol[1] == "admin"

    roles = db_mem.listar_roles()
    assert len(roles) == 1
    assert roles[0][1] == "admin"


def test_actualizar_rol(db_mem):
    rid = db_mem.crear_rol("operario")
    db_mem.actualizar_rol(rid, "operador")
    rol = db_mem.obtener_rol(rid)
    assert rol[1] == "operador"


def test_eliminar_rol(db_mem):
    rid = db_mem.crear_rol("invitado")
    db_mem.eliminar_rol(rid)
    assert db_mem.obtener_rol(rid) is None
    assert db_mem.listar_roles() == []


# -------------------- Usuario CRUD --------------------


def test_crear_obtener_listar_usuario(db_mem):
    rid = db_mem.crear_rol("admin")
    uid = db_mem.crear_usuario("juan", "hash123", 1, rid, "Juan Perez")
    assert uid is not None and uid > 0

    usuario = db_mem.obtener_usuario(uid)
    assert usuario is not None
    assert usuario[1] == "juan"
    assert usuario[2] == "hash123"
    assert usuario[3] == 1  # activo
    assert usuario[4] == rid  # id_rol
    assert usuario[5] == "Juan Perez"  # nombre
    assert usuario[6] == "admin"  # rol (join)

    usuarios = db_mem.listar_usuarios()
    assert len(usuarios) == 1
    assert usuarios[0][1] == "juan"


def test_actualizar_usuario(db_mem):
    rid = db_mem.crear_rol("admin")
    uid = db_mem.crear_usuario("juan", "hash123", 1, rid, "Juan Perez")
    db_mem.actualizar_usuario(uid, "juan", "hash456", 0, rid, "Juan Modificado")
    usuario = db_mem.obtener_usuario(uid)
    assert usuario[2] == "hash456"
    assert usuario[3] == 0  # inactivo
    assert usuario[5] == "Juan Modificado"


def test_eliminar_usuario(db_mem):
    rid = db_mem.crear_rol("admin")
    uid = db_mem.crear_usuario("juan", "hash123", 1, rid, "Juan Perez")
    db_mem.eliminar_usuario(uid)
    assert db_mem.obtener_usuario(uid) is None


def test_verificar_usuario(db_mem):
    rid = db_mem.crear_rol("admin")
    db_mem.crear_usuario("juan", "hash123", 1, rid, "Juan Perez")
    assert db_mem.verificar_usuario("juan", "hash123") is True
    assert db_mem.verificar_usuario("juan", "wrong") is False
    assert db_mem.verificar_usuario("inexistente", "hash123") is False


# -------------------- Migracion --------------------


def test_migrar_elimina_tablas_duplicadas(db_mem):
    conn = db_mem._connect()
    conn.execute("CREATE TABLE roles (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
    conn.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "nombre TEXT NOT NULL, email TEXT UNIQUE NOT NULL, rol_id INTEGER)"
    )
    conn.execute("INSERT INTO roles (nombre) VALUES ('supervisor')")
    conn.execute("INSERT INTO usuarios (nombre, email, rol_id) VALUES ('pedro', 'pedro@x.com', 2)")
    conn.commit()

    assert db_mem.tabla_existe("roles") is True
    assert db_mem.tabla_existe("usuarios") is True

    backup_path = db_mem.migrar_unificar_tablas(backup_dir="backups_test")
    assert os.path.exists(backup_path)

    assert db_mem.tabla_existe("roles") is False
    assert db_mem.tabla_existe("usuarios") is False
    assert db_mem.tabla_existe("rol") is True
    assert db_mem.tabla_existe("usuario") is True

    shutil.rmtree("backups_test", ignore_errors=True)


def test_migrar_copia_datos_nuevos_de_duplicados(db_mem):
    conn = db_mem._connect()
    conn.execute("CREATE TABLE roles (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
    conn.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "nombre TEXT NOT NULL, email TEXT UNIQUE NOT NULL, rol_id INTEGER)"
    )
    conn.execute("INSERT INTO roles (nombre) VALUES ('supervisor')")
    conn.execute("INSERT INTO usuarios (nombre, email, rol_id) VALUES ('pedro', 'pedro@x.com', 2)")
    conn.commit()

    db_mem.migrar_unificar_tablas(backup_dir="backups_test")

    roles = db_mem.listar_roles()
    assert any(r[1] == "supervisor" for r in roles), "supervisor debio migrarse"

    usuarios = db_mem.listar_usuarios()
    assert any(u[1] == "pedro" for u in usuarios), "pedro debio migrarse"

    shutil.rmtree("backups_test", ignore_errors=True)


def test_migrar_no_duplica_datos_ya_canónicos(db_mem):
    rid = db_mem.crear_rol("admin")
    db_mem.crear_usuario("juan", "hash123", 1, rid, "Juan Perez")

    conn = db_mem._connect()
    conn.execute("CREATE TABLE roles (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
    conn.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "nombre TEXT NOT NULL, email TEXT UNIQUE NOT NULL, rol_id INTEGER)"
    )
    conn.execute("INSERT INTO roles (nombre) VALUES ('admin')")
    conn.execute("INSERT INTO usuarios (nombre, email, rol_id) VALUES ('juan', 'juan@dup.com', 1)")
    conn.commit()

    db_mem.migrar_unificar_tablas(backup_dir="backups_test")

    roles = db_mem.listar_roles()
    admin_count = sum(1 for r in roles if r[1] == "admin")
    assert admin_count == 1, "admin no debe duplicarse"

    usuarios = db_mem.listar_usuarios()
    juan_count = sum(1 for u in usuarios if u[1] == "juan")
    assert juan_count == 1, "juan no debe duplicarse"

    shutil.rmtree("backups_test", ignore_errors=True)


def test_migrar_crea_backup(db_mem):
    conn = db_mem._connect()
    conn.execute("CREATE TABLE roles (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)")
    conn.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "nombre TEXT NOT NULL, email TEXT UNIQUE NOT NULL, rol_id INTEGER)"
    )
    conn.commit()

    backup_path = db_mem.migrar_unificar_tablas(backup_dir="backups_test")
    assert os.path.exists(backup_path)
    assert os.path.getsize(backup_path) > 0

    shutil.rmtree("backups_test", ignore_errors=True)


def test_estado_tablas(db_bolera_copy):
    estado = db_bolera_copy.obtener_estado_tablas()
    assert estado["usuario"] is True
    assert estado["rol"] is True


def test_migrar_sobre_bolera_db_real(db_bolera_copy):
    """Migracion sobre copia real de bolera.db: duplicados se eliminan, canonicos se preservan."""
    estado_antes = db_bolera_copy.obtener_estado_tablas()
    assert estado_antes["usuarios"] is True
    assert estado_antes["roles"] is True

    conn = db_bolera_copy._connect()
    usuarios_antes = conn.execute("SELECT COUNT(*) FROM usuario").fetchone()[0]
    roles_antes = conn.execute("SELECT COUNT(*) FROM rol").fetchone()[0]

    backup_path = db_bolera_copy.migrar_unificar_tablas(backup_dir="backups_test")
    assert os.path.exists(backup_path)

    estado_despues = db_bolera_copy.obtener_estado_tablas()
    assert estado_despues["usuarios"] is False
    assert estado_despues["roles"] is False

    usuarios_despues = conn.execute("SELECT COUNT(*) FROM usuario").fetchone()[0]
    roles_despues = conn.execute("SELECT COUNT(*) FROM rol").fetchone()[0]
    assert usuarios_despues == usuarios_antes
    assert roles_despues == roles_antes

    shutil.rmtree("backups_test", ignore_errors=True)
