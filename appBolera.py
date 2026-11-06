from PyQt6.QtWidgets import QApplication, QMainWindow
import recursos_rc  # registers :/iconos/ and :/imagenes/ from recursos.qrc
import bolos_rc     # registers :/bolo/ and :/animaciones/ from bolos.qrc

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
    """Punto de entrada: crea la QApplication global e inicia el loop.

    El login conserva su diseno propio (UI/Login.py); NO se aplica QSS a nivel
    global para no pisar ese diseno. El tema puede aplicarse por ventana.
    """
    app = QApplication.instance() or QApplication(argv or [])
    window = LoginApp(app)
    # Mantener referencia viva: si no, el GC destruye el wrapper y Qt cierra la ventana.
    app._login_window = window
    return app.exec()
