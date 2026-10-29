
import sqlite3
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_path="./temp.db"):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Inicializa la base de datos y crea tablas si no existen"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Crear tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lecturas_temperatura (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                    
                    temp_sensor1 REAL NOT NULL,
                    setpoint_sensor1 REAL NOT NULL,
                    histeresis_sensor1 REAL NOT NULL,
                    estado_sensor1 INTEGER,
                    desviacion_sensor1 REAL,
                    
                    temp_sensor2 REAL NOT NULL,
                    setpoint_sensor2 REAL NOT NULL,
                    histeresis_sensor2 REAL NOT NULL,
                    estado_sensor2 INTEGER,
                    desviacion_sensor2 REAL,
                    
                    temp_sensor3 REAL NOT NULL,
                    setpoint_sensor3 REAL NOT NULL,
                    histeresis_sensor3 REAL NOT NULL,
                    estado_sensor3 INTEGER,
                    desviacion_sensor3 REAL,
                    
                    temp_sensor4 REAL NOT NULL,
                    setpoint_sensor4 REAL NOT NULL,
                    histeresis_sensor4 REAL NOT NULL,
                    estado_sensor4 INTEGER,
                    desviacion_sensor4 REAL,
                    
                    observaciones TEXT
                );
            """)
            
            # Crear triggers para cálculo automático de desviaciones
            cursor.executescript("""
                CREATE TRIGGER IF NOT EXISTS calcular_desviaciones_insert
                AFTER INSERT ON lecturas_temperatura
                BEGIN
                    UPDATE lecturas_temperatura 
                    SET 
                        desviacion_sensor1 = temp_sensor1 - setpoint_sensor1,
                        desviacion_sensor2 = temp_sensor2 - setpoint_sensor2,
                        desviacion_sensor3 = temp_sensor3 - setpoint_sensor3,
                        desviacion_sensor4 = temp_sensor4 - setpoint_sensor4
                    WHERE id = NEW.id;
                END;
                
                CREATE TRIGGER IF NOT EXISTS calcular_desviaciones_update
                AFTER UPDATE OF temp_sensor1, temp_sensor2, temp_sensor3, temp_sensor4,
                                setpoint_sensor1, setpoint_sensor2, setpoint_sensor3, setpoint_sensor4
                ON lecturas_temperatura
                BEGIN
                    UPDATE lecturas_temperatura 
                    SET 
                        desviacion_sensor1 = temp_sensor1 - setpoint_sensor1,
                        desviacion_sensor2 = temp_sensor2 - setpoint_sensor2,
                        desviacion_sensor3 = temp_sensor3 - setpoint_sensor3,
                        desviacion_sensor4 = temp_sensor4 - setpoint_sensor4
                    WHERE id = NEW.id;
                END;
            """)
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Manejador de contexto para conexiones a la base de datos"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acceso a columnas por nombre
            yield conn
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            raise
        finally:
            if conn:
                conn.close()
    def insert_reading(self, temps, setpoints, hysteresis, observaciones=None):
        """Inserta una nueva lectura con cálculo de histéresis"""
        estados = []
        for temp, sp, hyst in zip(temps, setpoints, hysteresis):
            # Calcular estado según histéresis
            if temp > sp + hyst:
                estado = 1  # Arriba del rango
            elif temp < sp - hyst:
                estado = 0  # Abajo del rango
            else:
                estado = 2  # Dentro del rango de histéresis
            estados.append(estado)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lecturas_temperatura (
                    temp_sensor1, setpoint_sensor1, histeresis_sensor1, estado_sensor1, desviacion_sensor1,
                    temp_sensor2, setpoint_sensor2, histeresis_sensor2, estado_sensor2, desviacion_sensor2,
                    temp_sensor3, setpoint_sensor3, histeresis_sensor3, estado_sensor3, desviacion_sensor3,
                    temp_sensor4, setpoint_sensor4, histeresis_sensor4, estado_sensor4, desviacion_sensor4,
                    observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                temps[0], setpoints[0], hysteresis[0], estados[0], temps[0]-setpoints[0],
                temps[1], setpoints[1], hysteresis[1], estados[1], temps[1]-setpoints[1],
                temps[2], setpoints[2], hysteresis[2], estados[2], temps[2]-setpoints[2],
                temps[3], setpoints[3], hysteresis[3], estados[3], temps[3]-setpoints[3],
                observaciones
            ))
            conn.commit()            
    
    def insert_reading1(self, temps, setpoints, observaciones=None):
        """Inserta una nueva lectura de temperatura"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lecturas_temperatura (
                    temp_sensor1, setpoint_sensor1,
                    temp_sensor2, setpoint_sensor2,
                    temp_sensor3, setpoint_sensor3,
                    temp_sensor4, setpoint_sensor4,
                    observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                temps[0], setpoints[0],
                temps[1], setpoints[1],
                temps[2], setpoints[2],
                temps[3], setpoints[3],
                observaciones
            ))
            conn.commit()
            return cursor.lastrowid
    
   
    