# config.py - Configuracion centralizada para el sistema de bolera
# Unica fuente de verdad: IPs por pista, MODO_DOS_PLC, direcciones Modbus fijas, tema UI.
# No depende de hardware PLC (requisito CM-1).

# --- Direccion IP del PLC por pista (requisito CM-2) ---
# IP del automata que controla la Pista 1
PLC_IP_PISTA1 = "192.168.1.10"
# IP del automata que controla la Pista 2
PLC_IP_PISTA2 = "192.168.1.11"

# --- Modo de operacion PLC (requisito CM-3) ---
# 1 = un PLC controla ambas pistas (misma IP para pista1 y pista2)
# 2 = un PLC por pista (IPs independientes)
# Cualquier valor fuera de {1, 2} se resuelve a 1 por defecto.
MODO_DOS_PLC = 1

# --- Direcciones Modbus fijas (requisito CM-4) ---
# Direccion base del area de registros del automata (independiente del modelo)
MODBUS_ADDR = 20001

# --- Tema de UI (requisito CM-5) ---
# "claro" | "oscuro"
UI_THEME = "claro"
THEME_DEFAULT = UI_THEME

# --- Conexion PLC: parametros comunes ---
PLC_Puerto = 502
PLC_TIMEOUT = 3          # segundos
PLC_RETRY_MAX = 3
PLC_RETRY_DELAY = 2      # segundos
POLLING_ACTIVO = 500     # ms con juego activo
POLLING_INACTIVO = 2000  # ms sin juego

# IP unica cuando MODO_DOS_PLC == 1 (un PLC para ambas pistas).
PLC_IP = PLC_IP_PISTA1

# --- Base de datos ---
DB_NAME = "bolera.db"
DB_BACKUP_DIR = "backups"
DB_BACKUP_DIAS = 7
DB_BACKUP_SESIONES = 30

# --- Aplicacion / ventana ---
APP_NAME = "Control Automático de la Bolera"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def _validar_modo(valor):
    """Devuelve el modo valido (1 o 2). Cualquier otro valor se resuelve a 1 por defecto."""
    try:
        modo = int(valor)
    except (TypeError, ValueError):
        return 1
    return modo if modo in (1, 2) else 1


# Validar MODO_DOS_PLC al cargar el modulo (escenario: modo invalido -> default 1)
MODO_DOS_PLC = _validar_modo(MODO_DOS_PLC)
