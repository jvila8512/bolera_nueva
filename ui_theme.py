# ui_theme.py - Carga y aplicacion de QSS (tema claro/oscuro) desde config.py
# No importa PyQt en tiempo de import: aplicar_tema(app) recibe la QApplication.

import os

import config

_THEMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "themes")
_THEMES_VALIDOS = ("claro", "oscuro")


def tema_actual(theme=None):
    """Devuelve el tema normalizado: 'claro' u 'oscuro'. Cualquier otro -> 'claro'."""
    valor = theme if theme is not None else getattr(config, "UI_THEME", "claro")
    valor = str(valor).strip().lower() if valor is not None else "claro"
    return valor if valor in _THEMES_VALIDOS else "claro"


def ruta_qss(theme=None):
    return os.path.join(_THEMES_DIR, f"{tema_actual(theme)}.qss")


def cargar_qss(theme=None):
    """Devuelve el contenido QSS del tema. Fallback: cadena vacia (estilo por defecto)."""
    path = ruta_qss(theme)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def aplicar_tema(app, theme=None):
    """Aplica el QSS a la QApplication. Devuelve el QSS aplicado ('' si fallback)."""
    qss = cargar_qss(theme)
    if qss:
        app.setStyleSheet(qss)
    return qss
