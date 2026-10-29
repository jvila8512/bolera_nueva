from datetime import datetime, timedelta
import sqlite3
import os
from contextlib import contextmanager
import pandas as pd

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
    
    def get_last_readings(self, limit=5):
        """Obtiene las últimas lecturas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM lecturas_temperatura 
                ORDER BY fecha_hora DESC 
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
    ## MÉTODOS BÁSICOS DE CONSULTA ##

    def get_all_data(self):
        """Obtiene todos los datos de la tabla"""
        with self._get_connection() as conn:
            return pd.read_sql("SELECT * FROM lecturas_temperatura ORDER BY fecha_hora", conn)
    
    def get_data_between_dates(self, start_date, end_date):
        """
        Obtiene datos entre dos fechas
        Args:
            start_date (str): Fecha inicial en formato 'YYYY-MM-DD'
            end_date (str): Fecha final en formato 'YYYY-MM-DD'
        """
        query = """
        SELECT * FROM lecturas_temperatura 
        WHERE fecha_hora BETWEEN ? AND ?
        ORDER BY fecha_hora
        """
        with self._get_connection() as conn:
            return pd.read_sql(query, conn, params=(start_date, end_date + " 23:59:59"))
    
    def get_last_n_records(self, n=100):
        """Obtiene los últimos N registros"""
        with self._get_connection() as conn:
            return pd.read_sql(f"SELECT * FROM lecturas_temperatura ORDER BY fecha_hora DESC LIMIT {n}", conn)

    ## MÉTODOS DE ANÁLISIS POR SENSOR ##

    def get_sensor_stats(self, sensor_num, start_date=None, end_date=None):
        """
        Obtiene estadísticas clave para un sensor específico
        Args:
            sensor_num (int): Número de sensor (1-4)
            start_date (str): Fecha inicial opcional
            end_date (str): Fecha final opcional
        """
        base_query = f"""
        SELECT 
            AVG(temp_sensor{sensor_num}) as media_temp,
            MIN(temp_sensor{sensor_num}) as min_temp,
            MAX(temp_sensor{sensor_num}) as max_temp,
            AVG(desviacion_sensor{sensor_num}) as media_desviacion,
            AVG(ABS(desviacion_sensor{sensor_num})) as desviacion_absoluta,
            SUM(CASE WHEN ABS(desviacion_sensor{sensor_num}) > histeresis_sensor{sensor_num} THEN 1 ELSE 0 END) as eventos_fuera_rango,
            COUNT(*) as total_registros
        FROM lecturas_temperatura
        """
        
        params = []
        if start_date and end_date:
            base_query += " WHERE fecha_hora BETWEEN ? AND ?"
            params.extend([start_date, end_date + " 23:59:59"])
        
        with self._get_connection() as conn:
            return pd.read_sql(base_query, conn, params=params).iloc[0].to_dict()

    def get_sensor_trend(self, sensor_num, days=7):
        """
        Obtiene tendencia diaria para un sensor
        Args:
            sensor_num (int): Número de sensor (1-4)
            days (int): Días a retroceder desde hoy
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        query = f"""
        SELECT 
            DATE(fecha_hora) as fecha,
            AVG(temp_sensor{sensor_num}) as temp_promedio,
            AVG(setpoint_sensor{sensor_num}) as setpoint_promedio,
            AVG(histeresis_sensor{sensor_num}) as histeresis_promedio
        FROM lecturas_temperatura
        WHERE fecha_hora BETWEEN ? AND ?
        GROUP BY DATE(fecha_hora)
        ORDER BY fecha
        """
        
        with self._get_connection() as conn:
            return pd.read_sql(query, conn, params=(start_date, end_date))

    ## MÉTODOS DE ANÁLISIS COMPARATIVO ##

    def compare_sensors(self, start_date=None, end_date=None):
        """Compara el comportamiento de todos los sensores"""
        base_query = """
        SELECT
            AVG(temp_sensor1) as avg_temp1, AVG(desviacion_sensor1) as avg_dev1,
            AVG(temp_sensor2) as avg_temp2, AVG(desviacion_sensor2) as avg_dev2,
            AVG(temp_sensor3) as avg_temp3, AVG(desviacion_sensor3) as avg_dev3,
            AVG(temp_sensor4) as avg_temp4, AVG(desviacion_sensor4) as avg_dev4,
            
            SUM(CASE WHEN ABS(desviacion_sensor1) > histeresis_sensor1 THEN 1 ELSE 0 END) as outliers1,
            SUM(CASE WHEN ABS(desviacion_sensor2) > histeresis_sensor2 THEN 1 ELSE 0 END) as outliers2,
            SUM(CASE WHEN ABS(desviacion_sensor3) > histeresis_sensor3 THEN 1 ELSE 0 END) as outliers3,
            SUM(CASE WHEN ABS(desviacion_sensor4) > histeresis_sensor4 THEN 1 ELSE 0 END) as outliers4
        FROM lecturas_temperatura
        """
        
        params = []
        if start_date and end_date:
            base_query += " WHERE fecha_hora BETWEEN ? AND ?"
            params.extend([start_date, end_date + " 23:59:59"])
        
        with self._get_connection() as conn:
            return pd.read_sql(base_query, conn, params=params).iloc[0].to_dict()

    ## MÉTODOS PARA TOMA DE DECISIONES ##

    def suggest_setpoint_adjustment(self, sensor_num, start_date=None, end_date=None, lookback_days=7):
        """
        Sugiere ajustes de setpoint basado en datos históricos
        
        Args:
            sensor_num (int): Número de sensor (1-4)
            start_date (str, optional): Fecha inicial en formato 'YYYY-MM-DD'
            end_date (str, optional): Fecha final en formato 'YYYY-MM-DD'
            lookback_days (int): Días a considerar si no se especifican fechas
        """
        try:
            # Obtener datos según los parámetros proporcionados
            if start_date and end_date:
                df = self.get_data_between_dates(start_date, end_date)
            else:
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
                df = self.get_data_between_dates(start_date, end_date)
            
            if df.empty:
                return {
                    'current_setpoint': 0,
                    'avg_temperature': 0,
                    'avg_deviation': 0,
                    'suggestion': "No hay datos para analizar"
                }
            
            # Obtener el último setpoint registrado
            current_setpoint = df[f'setpoint_sensor{sensor_num}'].iloc[-1]
            
            # Calcular estadísticas
            avg_temp = df[f'temp_sensor{sensor_num}'].mean()
            avg_deviation = df[f'desviacion_sensor{sensor_num}'].mean()
            
            # Generar sugerencia
            if avg_deviation > df[f'histeresis_sensor{sensor_num}'].mean():
                suggestion = f"Reducir setpoint en {abs(avg_deviation):.1f}°C"
            elif avg_deviation < -df[f'histeresis_sensor{sensor_num}'].mean():
                suggestion = f"Aumentar setpoint en {abs(avg_deviation):.1f}°C"
            else:
                suggestion = "Setpoint adecuado (dentro del rango de histéresis)"
            
            return {
                'current_setpoint': current_setpoint,
                'avg_temperature': avg_temp,
                'avg_deviation': avg_deviation,
                'suggestion': suggestion
            }
            
        except Exception as e:
            print(f"Error en suggest_setpoint_adjustment: {e}")
            return {
                'current_setpoint': 0,
                'avg_temperature': 0,
                'avg_deviation': 0,
                'suggestion': f"Error al calcular: {str(e)}"
            }
        
    def get_current_setpoint(self, sensor_num):
        """Obtiene el último setpoint registrado para un sensor"""
        query = f"""
        SELECT setpoint_sensor{sensor_num} 
        FROM lecturas_temperatura 
        ORDER BY fecha_hora DESC 
        LIMIT 1
        """
        with self._get_connection() as conn:
            return conn.execute(query).fetchone()[0]

    ## MÉTODOS PARA DETECCIÓN DE PROBLEMAS ##

    def detect_anomalies(self, sensor_num, threshold=3.0, days=3):
        """
        Detecta lecturas anómalas basadas en desviación estándar
        Args:
            sensor_num (int): Número de sensor (1-4)
            threshold (float): Umbral de desviaciones estándar
            days (int): Días a analizar
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        query = f"""
        WITH stats AS (
            SELECT 
                AVG(temp_sensor{sensor_num}) as mean,
                STDEV(temp_sensor{sensor_num}) as stdev
            FROM lecturas_temperatura
            WHERE fecha_hora BETWEEN ? AND ?
        )
        SELECT 
            fecha_hora,
            temp_sensor{sensor_num},
            setpoint_sensor{sensor_num},
            histeresis_sensor{sensor_num},
            desviacion_sensor{sensor_num},
            (temp_sensor{sensor_num} - (SELECT mean FROM stats)) / 
                NULLIF((SELECT stdev FROM stats), 0) as z_score
        FROM lecturas_temperatura
        WHERE fecha_hora BETWEEN ? AND ?
            AND ABS((temp_sensor{sensor_num} - (SELECT mean FROM stats)) / 
                   NULLIF((SELECT stdev FROM stats), 0)) > ?
        ORDER BY ABS(z_score) DESC
        """
        
        with self._get_connection() as conn:
            return pd.read_sql(query, conn, params=(start_date, end_date, start_date, end_date, threshold))

    ## MÉTODOS DE VISUALIZACIÓN ##

    def get_temperature_distribution(self, sensor_num, start_date=None, end_date=None):
        """
        Obtiene distribución de temperaturas para histograma
        Args:
            sensor_num (int): Número de sensor (1-4)
            start_date (str): Fecha inicial opcional
            end_date (str): Fecha final opcional
        """
        base_query = f"""
        SELECT 
            temp_sensor{sensor_num} as temperatura,
            setpoint_sensor{sensor_num} as setpoint,
            histeresis_sensor{sensor_num} as histeresis
        FROM lecturas_temperatura
        """
        
        params = []
        if start_date and end_date:
            base_query += " WHERE fecha_hora BETWEEN ? AND ?"
            params.extend([start_date, end_date + " 23:59:59"])
        
        with self._get_connection() as conn:
            return pd.read_sql(base_query, conn, params=params)

    def get_data_by_date_range(self, start_date, end_date, sensor_num=None):
        """
        Obtiene todos los datos dentro de un rango de fechas
        Args:
            start_date (str): Fecha inicial en formato 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS'
            end_date (str): Fecha final en formato 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS'
            sensor_num (int, optional): Número de sensor específico (1-4). Si es None, devuelve todos los sensores
        Returns:
            pandas.DataFrame: DataFrame con los datos del rango solicitado
        """
        # Construir la consulta base
        if sensor_num is None:
            select_columns = "*"
        else:
            select_columns = f"""
                id, fecha_hora,
                temp_sensor{sensor_num} as temperatura,
                setpoint_sensor{sensor_num} as setpoint,
                histeresis_sensor{sensor_num} as histeresis,
                estado_sensor{sensor_num} as estado,
                desviacion_sensor{sensor_num} as desviacion
            """
        
        query = f"""
        SELECT {select_columns}
        FROM lecturas_temperatura
        WHERE fecha_hora BETWEEN ? AND ?
        ORDER BY fecha_hora
        """
        
        # Asegurar formato de fechas
        if len(start_date) <= 10:  # Si solo tiene fecha (YYYY-MM-DD)
            start_date = f"{start_date} 00:00:00"
        if len(end_date) <= 10:    # Si solo tiene fecha (YYYY-MM-DD)
            end_date = f"{end_date} 23:59:59"
        
        try:
            with self._get_connection() as conn:
                df = pd.read_sql(query, conn, params=(start_date, end_date))
                
                # Convertir fecha_hora a datetime si existe
                if 'fecha_hora' in df.columns:
                    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
                
                return df
                
        except sqlite3.Error as e:
            print(f"Error al consultar datos: {e}")
            return pd.DataFrame()  # Devuelve DataFrame vacío en caso de error


# Ejemplo de uso
if __name__ == "__main__":
    db = DatabaseManager()
    
    # Insertar nueva lectura
    db.insert_reading(
        temps=[22.5, 23.1, 21.8, 22.9],
        setpoints=[22.0, 23.5, 21.5, 23.0],
        observaciones="Lectura de prueba"
    )
    
    # Obtener últimas lecturas
    lecturas = db.get_last_readings()
    for lectura in lecturas:
        print(f"Lectura ID: {lectura['id']}")
        print(f"Fecha: {lectura['fecha_hora']}")
        print(f"Sensor 1: {lectura['temp_sensor1']}°C (Setpoint: {lectura['setpoint_sensor1']}°C)")
        print("-" * 40)