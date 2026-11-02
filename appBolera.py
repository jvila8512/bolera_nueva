from PyQt6.QtWidgets import QApplication, QMainWindow

import AppLogin


class LoginApp(QMainWindow):
    """Ventana raiz del login. Ya NO crea su propia QApplication.

    La QApplication es global y se crea en Ejecutar.py (main). Si se instancia
    sin app (compatibilidad), reutiliza la instancia existente o crea una.
    """

    def __init__(self, app=None):
        super().__init__()
        self.app = app or QApplication.instance() or QApplication([])
        self.login = AppLogin.LoginWindow()


def main(argv=None):
    """Punto de entrada: crea la QApplication global, aplica tema e inicia el loop."""
    app = QApplication.instance() or QApplication(argv or [])
    try:
        from ui_theme import aplicar_tema

        aplicar_tema(app)
    except Exception:
        # Fallback: si el tema falla, se usa el estilo por defecto de Qt.
        pass
    window = LoginApp(app)
    # Mantener referencia viva: si no, el GC destruye el wrapper y Qt cierra la ventana.
    app._login_window = window
    return app.exec()
