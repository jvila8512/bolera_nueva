# tests/test_config.py
# Unit tests de config.py: valores por defecto y validacion de MODO_DOS_PLC.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config  # noqa: E402


def test_config_defaults():
    assert isinstance(config.PLC_IP_PISTA1, str) and config.PLC_IP_PISTA1
    assert isinstance(config.PLC_IP_PISTA2, str) and config.PLC_IP_PISTA2
    assert config.MODO_DOS_PLC in (1, 2)
    assert isinstance(config.MODBUS_ADDR, int)
    assert config.UI_THEME in ("claro", "oscuro")


def test_validar_modo_invalido_cae_a_1():
    assert config._validar_modo(3) == 1
    assert config._validar_modo(0) == 1
    assert config._validar_modo("x") == 1
    assert config._validar_modo(None) == 1


def test_validar_modo_validos():
    assert config._validar_modo(1) == 1
    assert config._validar_modo(2) == 2
    assert config._validar_modo("2") == 2
