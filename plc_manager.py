# plc_manager.py - PLCManager singleton para comunicacion Modbus (M221)
# Envuelve ConexionBD/M221_Bolera.py. Una conexion por pista segun MODO_DOS_PLC.
# Las direcciones son fijas; solo varia la IP (config.py).
# No exige pymodbus en tiempo de import: el driver es inyectable (tests sin hardware).

import time

import config


def _default_driver_factory(ip):
    """Crea el driver real M221. Import perezoso para no exigir pymodbus en tests."""
    from ConexionBD.M221_Bolera import M221

    return M221(ip)


class PLCManager:
    """Singleton que gestiona conexiones Modbus y una cache de lecturas por pista.

    - modo == 1: un unico driver sirve ambas pistas (misma IP).
    - modo == 2: un driver por pista (PLC_IP_PISTA1 / PLC_IP_PISTA2).
    - Auto-reconnect con backoff exponencial ante fallos de lectura/escritura.
    - batch_read(track_id, addresses) lee un bloque y devuelve {address: value}.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        driver_factory=None,
        ip_pista1=None,
        ip_pista2=None,
        modo=None,
        addr=None,
        reconnect_attempts=3,
        backoff_base=0.05,
        cache_ttl=0.0,
    ):
        if getattr(self, "_initialized", False):
            return
        self.driver_factory = driver_factory or _default_driver_factory
        self.ip_pista1 = ip_pista1 if ip_pista1 is not None else config.PLC_IP_PISTA1
        self.ip_pista2 = ip_pista2 if ip_pista2 is not None else config.PLC_IP_PISTA2
        self.modo = config._validar_modo(modo if modo is not None else config.MODO_DOS_PLC)
        self.addr = addr if addr is not None else config.MODBUS_ADDR
        self.reconnect_attempts = max(1, int(reconnect_attempts))
        self.backoff_base = backoff_base
        self.cache_ttl = cache_ttl
        self._drivers = {}
        self._cache = {}  # (track_id, address) -> (timestamp, value)
        self._initialized = True

    # -------------------- ciclo de vida --------------------

    def _driver_key(self, track_id):
        # modo 1: un unico driver compartido; modo 2: un driver por pista.
        return 1 if self.modo == 1 else track_id

    def _ip_para(self, track_id):
        return self.ip_pista1 if track_id == 1 else self.ip_pista2

    def _conectar_pista(self, track_id):
        key = self._driver_key(track_id)
        driver = self._drivers.get(key)
        if driver is None:
            driver = self.driver_factory(self._ip_para(key))
            self._drivers[key] = driver
        try:
            if not getattr(driver, "conexion_exitosa", False):
                driver.connectar()
            return bool(getattr(driver, "conexion_exitosa", True))
        except Exception:
            return False

    def conectar(self, track_id=None):
        """Conecta la(s) pista(s). Sin argumento conecta las que use el modo actual."""
        pistas = [track_id] if track_id is not None else [1, 2] if self.modo == 2 else [1]
        ok = True
        for pista in dict.fromkeys(pistas):
            ok = self._conectar_pista(pista) and ok
        return ok

    def desconectar(self, track_id=None):
        keys = [self._driver_key(track_id)] if track_id is not None else list(self._drivers.keys())
        for key in keys:
            driver = self._drivers.get(key)
            if driver is not None:
                try:
                    driver.desconectar()
                except Exception:
                    pass
            self._drivers[key] = None
        if track_id is None:
            self._cache.clear()

    # -------------------- cache --------------------

    def _cache_get(self, track_id, address):
        entry = self._cache.get((track_id, address))
        if entry is None:
            return None
        ts, value = entry
        if self.cache_ttl and (time.time() - ts) > self.cache_ttl:
            return None
        return value

    def _cache_set(self, track_id, address, value):
        self._cache[(track_id, address)] = (time.time(), value)

    def invalidar_cache(self, track_id=None):
        if track_id is None:
            self._cache.clear()
            return
        for key in [k for k in self._cache if k[0] == track_id]:
            del self._cache[key]

    # -------------------- reconexion --------------------

    def _con_reintento(self, track_id, operacion, aceptar_false=False):
        """Ejecuta operacion() con reintentos y backoff. Reconecta entre intentos.

        Un resultado None (o False, salvo aceptar_false) se considera fallo y se
        reintenta reconectando la pista.
        """
        ultima_excepcion = None
        for intento in range(self.reconnect_attempts):
            try:
                resultado = operacion()
                if resultado is not None and (aceptar_false or resultado is not False):
                    return resultado
            except Exception as exc:  # noqa: BLE001
                ultima_excepcion = exc
            # fallo -> reconectar con backoff exponencial
            self.desconectar(track_id)
            time.sleep(self.backoff_base * (2 ** intento))
            self._conectar_pista(track_id)
        if ultima_excepcion is not None:
            raise ultima_excepcion
        return None

    # -------------------- lecturas --------------------

    def leer_mw(self, track_id, address=None, usar_cache=True):
        address = self.addr if address is None else address
        if usar_cache:
            cached = self._cache_get(track_id, address)
            if cached is not None:
                return cached
        self._conectar_pista(track_id)
        driver = self._drivers.get(self._driver_key(track_id))
        if driver is None:
            return None
        valor = self._con_reintento(track_id, lambda: driver.leer_MW(address))
        if valor is not None:
            self._cache_set(track_id, address, valor)
        return valor

    def batch_read(self, track_id, addresses=None):
        """Lee un bloque de direcciones de una pista. Devuelve {address: value}."""
        if addresses is None:
            addresses = [self.addr]
        return {address: self.leer_mw(track_id, address, usar_cache=False) for address in addresses}

    def leer_bit(self, track_id, address, bit_number):
        self._conectar_pista(track_id)
        driver = self._drivers.get(self._driver_key(track_id))
        if driver is None:
            return None
        return self._con_reintento(track_id, lambda: driver.leer_bitM241(address, bit_number))

    # -------------------- escrituras --------------------

    def escribir_mw(self, track_id, address, value):
        self._conectar_pista(track_id)
        driver = self._drivers.get(self._driver_key(track_id))
        if driver is None:
            return False
        try:
            ok = self._con_reintento(track_id, lambda: driver.escribir_MW(address, value))
        except Exception:
            return False
        if ok:
            self._cache_set(track_id, address, value)
        return bool(ok)

    def escribir_bit(self, track_id, address, bit_number, value):
        self._conectar_pista(track_id)
        driver = self._drivers.get(self._driver_key(track_id))
        if driver is None:
            return False
        try:
            ok = self._con_reintento(
                track_id, lambda: driver.escribir_bit_M241(address, bit_number, value)
            )
        except Exception:
            return False
        return bool(ok)

    # -------------------- helpers / tests --------------------

    @property
    def drivers(self):
        return self._drivers

    def driver_de_pista(self, track_id):
        return self._drivers.get(self._driver_key(track_id))

    @classmethod
    def reset_instance(cls):
        """Reinicia el singleton (util para tests)."""
        if cls._instance is not None:
            try:
                cls._instance.desconectar()
            except Exception:
                pass
        cls._instance = None


def get_plc_manager(**kwargs):
    """Acceso al singleton PLCManager."""
    return PLCManager(**kwargs)
