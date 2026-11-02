# tests/test_ui_theme.py
# Unit tests de ui_theme.py: carga de QSS claro/oscuro, fallback y aplicacion offscreen.

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ui_theme  # noqa: E402


def test_tema_actual_normaliza():
    assert ui_theme.tema_actual() in ("claro", "oscuro")
    assert ui_theme.tema_actual("OSCURO") == "oscuro"
    assert ui_theme.tema_actual("xxx") == "claro"


def test_cargar_qss_claro_y_oscuro_existen_y_difieren():
    claro = ui_theme.cargar_qss("claro")
    oscuro = ui_theme.cargar_qss("oscuro")
    assert claro.strip() != ""
    assert oscuro.strip() != ""
    assert claro != oscuro


def test_fallback_si_no_existe_tema(tmp_path, monkeypatch):
    monkeypatch.setattr(ui_theme, "_THEMES_DIR", str(tmp_path))
    assert ui_theme.cargar_qss("claro") == ""


def test_aplicar_tema_con_qapplication_offscreen():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    pytest.importorskip("PyQt6")
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    qss = ui_theme.aplicar_tema(app, "oscuro")
    assert qss.strip() != ""
    assert app.styleSheet() == qss
