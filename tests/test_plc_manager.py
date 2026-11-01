# tests/test_plc_manager.py
# Unit tests de PLCManager: singleton, modos 1|2, cache, batch_read y reconexion.
# Usa un FakeDriver inyectado: no requiere pymodbus ni hardware PLC.

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plc_manager import PLCManager  # noqa: E402


# -------------------- Fake driver --------------------


class FakeDriver:
    def __init__(self, ip, fail_times=0, values=None):
        self.ip = ip
        self.conexion_exitosa = True
        self.connect_calls = 0
        self.disconnect_calls = 0
        self.read_calls = 0
        self.write_calls = 0
        self.fail_times = fail_times
        self.values = dict(values or {})

    def connectar(self):
        self.connect_calls += 1
        self.conexion_exitosa = True
        return True

    def desconectar(self):
        self.disconnect_calls += 1
        self.conexion_exitosa = False

    def leer_MW(self, address):
        self.read_calls += 1
        if self.read_calls <= self.fail_times:
            return None
        return self.values.get(address, 0)

    def escribir_MW(self, address, value):
        self.write_calls += 1
        self.values[address] = value
        return True

    def escribir_bit_M241(self, address, bit_number, value):
        self.values[(address, bit_number)] = value
        return True

    def leer_bitM241(self, address, bit_number):
        return self.values.get((address, bit_number), 0)


class DriverRegistry:
    """Factory de FakeDriver que registra las instancias creadas."""

    def __init__(self, fail_times=0, values=None):
        self.fail_times = fail_times
        self.values = values
        self.created = []

    def __call__(self, ip):
        # Solo el primer driver falla; los reconectados funcionan (simula recuperacion).
        fail = self.fail_times if not self.created else 0
        driver = FakeDriver(ip, fail_times=fail, values=self.values)
        self.created.append(driver)
        return driver


@pytest.fixture(autouse=True)
def reset_singleton():
    PLCManager.reset_instance()
    yield
    PLCManager.reset_instance()


# -------------------- Singleton --------------------


def test_singleton_devuelve_misma_instancia():
    reg = DriverRegistry()
    a = PLCManager(driver_factory=reg)
    b = PLCManager()
    assert a is b


# -------------------- Modos --------------------


def test_modo_1_un_driver_para_ambas_pistas():
    reg = DriverRegistry()
    pm = PLCManager(driver_factory=reg, modo=1, ip_pista1="10.0.0.1", ip_pista2="10.0.0.2")
    pm.conectar()
    assert len(pm.drivers) == 1
    assert pm.driver_de_pista(1) is pm.driver_de_pista(2)
    assert pm.driver_de_pista(1).ip == "10.0.0.1"


def test_modo_2_un_driver_por_pista():
    reg = DriverRegistry()
    pm = PLCManager(driver_factory=reg, modo=2, ip_pista1="10.0.0.1", ip_pista2="10.0.0.2")
    pm.conectar()
    assert len(pm.drivers) == 2
    assert pm.driver_de_pista(1) is not pm.driver_de_pista(2)
    assert pm.driver_de_pista(1).ip == "10.0.0.1"
    assert pm.driver_de_pista(2).ip == "10.0.0.2"


def test_modo_invalido_cae_a_1():
    reg = DriverRegistry()
    pm = PLCManager(driver_factory=reg, modo=3)
    assert pm.modo == 1


# -------------------- Cache y batch --------------------


def test_cache_evita_segunda_lectura():
    reg = DriverRegistry(values={20001: 42})
    pm = PLCManager(driver_factory=reg, modo=1)
    pm.conectar()
    primero = pm.leer_mw(1, 20001)
    segundo = pm.leer_mw(1, 20001)
    assert primero == 42
    assert segundo == 42
    assert pm.driver_de_pista(1).read_calls == 1


def test_invalidar_cache_fuerza_nueva_lectura():
    reg = DriverRegistry(values={20001: 7})
    pm = PLCManager(driver_factory=reg, modo=1)
    pm.conectar()
    pm.leer_mw(1, 20001)
    pm.invalidar_cache()
    pm.leer_mw(1, 20001)
    assert pm.driver_de_pista(1).read_calls == 2


def test_batch_read_devuelve_diccionario():
    reg = DriverRegistry(values={20001: 1, 20002: 2})
    pm = PLCManager(driver_factory=reg, modo=1)
    pm.conectar()
    lote = pm.batch_read(1, [20001, 20002])
    assert lote == {20001: 1, 20002: 2}


# -------------------- Reconexion --------------------


def test_reconecta_tras_fallo_y_devuelve_valor():
    # El primer read devuelve None (fallo); tras reconectar, el segundo devuelve el valor.
    reg = DriverRegistry(fail_times=1, values={20001: 99})
    pm = PLCManager(driver_factory=reg, modo=1, reconnect_attempts=3, backoff_base=0.0)
    pm.conectar()
    valor = pm.leer_mw(1, 20001)
    assert valor == 99
    # El driver original (el que fallo) fue desconectado antes de reconectar.
    assert reg.created[0].disconnect_calls >= 1


def test_escritura_actualiza_cache():
    reg = DriverRegistry(values={20001: 0})
    pm = PLCManager(driver_factory=reg, modo=1)
    pm.conectar()
    assert pm.escribir_mw(1, 20001, 55) is True
    # tras escribir, la cache tiene 55 y no vuelve a leer del driver
    assert pm.leer_mw(1, 20001) == 55
