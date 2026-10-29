


import sys
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QMutex,QDate
from PyQt6.QtGui import QColor, QPalette, QIcon
from PyQt6.QtWidgets import  QDialog,QWidget, QMessageBox, QApplication,QMainWindow
from HMI.BD import DatabaseManager
from PyQt6.QtWidgets import QWidget,QTableWidgetItem,QTabWidget,QFormLayout,QTableWidget,QHeaderView,QDialog,QVBoxLayout, QLabel, QMessageBox,QFileDialog,QPushButton,QHBoxLayout,QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from HMI.DatosTempetarura import DatosTemperatura
from contextlib import contextmanager
import pandas as pd
from PyQt6.QtCore import Qt
import fotos


class TemperatureAnalysisWindow(QDialog):      
       
    def __init__(self):
        super().__init__()        
        # Initialize the UI from the generated 'main_ui' class
        self.ui = DatosTemperatura()
        self.ui.setupUi(self)
        self.setWindowTitle("Analisis de datos")    
        self.setWindowIcon(QIcon(":/control/Imagenes/histeresis.png"))

         # Inicializa el DatabaseManager
        self.db_manager = DatabaseManager("./temperaturasPe.db")
     
        self.tabla=self.ui.tabla_usuarios
        self.btn1=self.ui.btn1
        self.btn2=self.ui.btn2
        self.btn3=self.ui.btn3
        self.fechaInicio=self.ui.dateEdit_2
        self.fechaFin=self.ui.dateEdit
        self.btnFiltro= self.ui.pushButton
         # Configuración de la tabla
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) 
        self.tabla.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #ccc;
                background-color: #f9f9f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 1px;
            }
            QHeaderView::section {
                background-color: #0078d7;
                color: white;
                padding: 1px;
                font-weight: bold;
            }
            QPushButton {
          
            margin: 2px 4px;  /* Añadir margen para separar botones */
          
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #dadada;
        }
        """)

         
        # Ocultar el encabezado vertical (numeración de filas)
        self.tabla.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical
 
        
        # Inicialización
        self.initGUI()
        self.load_initial_data()
    def initGUI(self):      
              
       #Botones de Configuracion
       self.ui.btn1.clicked.connect(self.trend_analysis)
       self.ui.btn2.clicked.connect(self.statistical_analysis)
       self.ui.btn3.clicked.connect(self.show_temperature_distribution)
       self.ui.pushButton.clicked.connect(self.filter_data)
       self.ui.btn_suggest.clicked.connect(self.suggest_adjustments)
       self.ui.btn_stats.clicked.connect(self.show_advanced_stats)
       self.ui.btn_compare.clicked.connect(self.compare_sensors)
        # Configurar fechas por defecto (últimos 7 días)
       self.ui.dateEdit_2.setDate(QDate.currentDate().addDays(-7))
       self.ui.dateEdit.setDate(QDate.currentDate())
    def load_initial_data(self):
            """Carga todos los datos iniciales en la tabla"""
       
            # Obtener todos los datos
            df = self.db_manager.get_all_data()
            print(df)
            
            # Configurar tabla
            self.setup_table(df)
            
       
    def setup_table(self, df):
        """Configura la tabla con nombres de columnas mejorados"""
        if df.empty:
            return
        
        # Mapeo de columnas originales a nombres amigables
        column_mapping = {
            # Formato: 'columna_original': 'Nombre a mostrar'
            'fecha_hora': 'Fecha y Hora',
            'temp_sensor1': 'Temp. Sensor1 ',
            'setpoint_sensor1': 'Setpoint1',
            'histeresis_sensor1': 'Histeresis1',
            'temp_sensor2': 'Temp. Sensor2',
            'setpoint_sensor2': 'Setpoint2',
            'histeresis_sensor2': 'Histeresis2',
            'temp_sensor3': 'Temp. Sensor3',
            'setpoint_sensor3': 'Setpoint3',
            'histeresis_sensor3': 'Histeresis3',
            'temp_sensor4': 'Temp. Sensor4',
            'setpoint_sensor4': 'Setpoint4',
            'histeresis_sensor4': 'Histeresis4'
        }
        
        # Columnas originales que queremos mostrar (en el orden deseado)
        original_columns = [
            'fecha_hora',
            'temp_sensor1', 'setpoint_sensor1', 'histeresis_sensor1',
            'temp_sensor2', 'setpoint_sensor2', 'histeresis_sensor2',
            'temp_sensor3', 'setpoint_sensor3', 'histeresis_sensor3',
            'temp_sensor4', 'setpoint_sensor4', 'histeresis_sensor4'
        ]
        
        # Filtrar columnas existentes
        available_columns = [col for col in original_columns if col in df.columns]
        filtered_df = df[available_columns].copy()
        
        # Convertir fecha si existe
        if 'fecha_hora' in filtered_df.columns:
            filtered_df['fecha_hora'] = pd.to_datetime(filtered_df['fecha_hora'])
        
        # Limpiar tabla
        self.tabla.setRowCount(0)
        self.tabla.setColumnCount(len(filtered_df.columns))
        
        # Configurar encabezados con nombres amigables
        friendly_headers = [column_mapping[col] for col in filtered_df.columns]
        self.tabla.setHorizontalHeaderLabels(friendly_headers)
        
        # Llenar tabla con datos
        for row_idx, row in filtered_df.iterrows():
            self.tabla.insertRow(row_idx)
            for col_idx, (col_name, value) in enumerate(row.items()):
                item = QTableWidgetItem()
                
                # Formatear según el tipo de dato
                if pd.api.types.is_datetime64_any_dtype(filtered_df[col_name].dtype):
                    item.setText(value.strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(value) else 'N/A')
                elif pd.api.types.is_numeric_dtype(filtered_df[col_name].dtype):
                    item.setText(f"{value:.2f}" if not pd.isna(value) else "N/A")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setText(str(value))
                
                self.tabla.setItem(row_idx, col_idx, item)
        
        # Ajustar columnas automáticamente
        self.tabla.resizeColumnsToContents()
        
        # Configuración especial para columnas de temperatura
        self.configure_temperature_columns(friendly_headers)

    def configure_temperature_columns(self, headers):
        """Configura propiedades especiales para columnas de temperatura"""
        temperature_keywords = ['Temp.', 'Setpoint', 'Histeresis']
        
        for col_idx, header in enumerate(headers):
            if any(keyword in header for keyword in temperature_keywords):
                # Ajustar ancho mínimo para columnas de temperatura
                self.tabla.horizontalHeader().setMinimumSectionSize(100)
                
                # Centrar encabezados
                header_item = self.tabla.horizontalHeaderItem(col_idx)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def filter_data(self):
        """Filtra datos por rango de fechas"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            # Obtener datos filtrados
            df = self.db_manager.get_data_between_dates(start_date, end_date)
            
            if df.empty:
                QMessageBox.information(self, "Información", "No hay datos en el rango seleccionado")
                return
                
            # Mostrar en tabla
            self.setup_table(df)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al filtrar datos: {str(e)}")
    
    def trend_analysis(self):
        """Análisis de tendencias mostrando solo fechas de inicio/fin"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            # Obtener datos para análisis
            df = self.db_manager.get_data_between_dates(start_date, end_date)
            
            if df.empty:
                QMessageBox.warning(self, "Advertencia", "No hay datos para analizar")
                return
            
            # Convertir fecha_hora a datetime si no lo está
            df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
            
            # Crear gráfico de tendencia
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Graficar datos
            ax.plot(df['fecha_hora'], df['temp_sensor1'], label='Temperatura Sensor 1')
            ax.plot(df['fecha_hora'], df['setpoint_sensor1'], 'r--', label='Setpoint')
            
            # Área de histéresis
            ax.fill_between(df['fecha_hora'], 
                        df['setpoint_sensor1'] - df['histeresis_sensor1'],
                        df['setpoint_sensor1'] + df['histeresis_sensor1'],
                        color='gray', alpha=0.2, label='Banda de Histéresis')
            
            # Configurar el eje X para mostrar solo inicio y fin
            ax.set_xticks([df['fecha_hora'].iloc[0], df['fecha_hora'].iloc[-1]])
            ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M'))
            
            ax.set_title(f"Análisis de Tendencia\n{start_date} a {end_date}")
            ax.set_xlabel("Periodo")
            ax.set_ylabel("Temperatura (°C)")
            ax.legend()
            ax.grid(True)
            
            # Ajustar automáticamente el formato de fechas
            fig.autofmt_xdate()
            
            # Mostrar gráfico en ventana persistente
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en análisis de tendencia: {str(e)}")
    
    def statistical_analysis(self):
        """Muestra estadísticas clave de los datos"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            # Obtener estadísticas para todos los sensores
            stats_report = "📊 Estadísticas por Sensor:\n\n"
            
            for sensor_num in range(1, 5):
                stats = self.db_manager.get_sensor_stats(sensor_num, start_date, end_date)
                
                stats_report += (
                    f"Sensor {sensor_num}:\n"
                    f"• Temperatura promedio: {stats['media_temp']:.2f}°C\n"
                    f"• Mínima: {stats['min_temp']:.2f}°C | Máxima: {stats['max_temp']:.2f}°C\n"
                    f"• Desviación promedio: {stats['media_desviacion']:.2f}°C\n"
                    f"• Eventos fuera de rango: {stats['eventos_fuera_rango']} ({stats['eventos_fuera_rango']/stats['total_registros']:.1%})\n\n"
                )
            
            QMessageBox.information(self, "Estadísticas", stats_report)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en análisis estadístico: {str(e)}")
    
    def outlier_detection(self):
        """Detecta y muestra valores atípicos"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            # Detectar outliers para el primer sensor (puedes adaptar para otros)
            outliers = self.db_manager.detect_anomalies(1, threshold=2.5, days=7)
            
            if outliers.empty:
                QMessageBox.information(self, "Outliers", "No se detectaron valores atípicos")
                return
                
            # Mostrar outliers en tabla
            self.setup_table(outliers)
            
            # Resumen para mensaje
            summary = (
                f"Se detectaron {len(outliers)} valores atípicos\n\n"
                f"Temperatura máxima atípica: {outliers['temp_sensor1'].max():.2f}°C\n"
                f"Temperatura mínima atípica: {outliers['temp_sensor1'].min():.2f}°C\n"
                f"Desviación máxima: {outliers['desviacion_sensor1'].max():.2f}°C"
            )
            
            QMessageBox.information(self, "Outliers Detectados", summary)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en detección de outliers: {str(e)}")   
    def apply_styles(self): 
       # Desactivar la edición para toda la tabla
           self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

            # Desactivar la selección
           self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
           self.tabla.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
           # CSS para la tabla
           self.tabla.setStyleSheet("""
           QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #ccc;
                background-color: #f9f9f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 1px;
            }
            QHeaderView::section {
                background-color: #0078d7;
                color: white;
                padding: 1px;
                font-weight: bold;
            }
             QPushButton {
          
            margin: 2px 4px;  /* Añadir margen para separar botones */
          
            border-radius: 2px;
        }
        QPushButton:hover {
            background-color: #dadada;
        }
           
        """)   
    def suggest_adjustments(self):
        """Muestra sugerencias de ajuste para setpoints e histéresis"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            report = "🔧 Sugerencias de Ajuste:\n\n"
            
            for sensor_num in range(1, 5):
                suggestion = self.db_manager.suggest_setpoint_adjustment(
                    sensor_num, 
                    start_date=start_date, 
                    end_date=end_date
                )
                
                report += (
                    f"Sensor {sensor_num}:\n"
                    f"• Setpoint actual: {suggestion['current_setpoint']}°C\n"
                    f"• Temp. promedio: {suggestion['avg_temperature']:.2f}°C\n"
                    f"• Desviación: {suggestion['avg_deviation']:.2f}°C\n"
                    f"• Recomendación: {suggestion['suggestion']}\n\n"
                )
            
            # Mostrar en QMessageBox con formato mejorado
            msg = QMessageBox(self)
            msg.setWindowTitle("Sugerencias de Ajuste")
            msg.setText(report)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            
        except Exception as e:
            print(f"Error al generar sugerencias:\n{str(e)}")
            QMessageBox.critical(self, "Error", f"Error al generar sugerencias:\n{str(e)}")

    def show_advanced_stats(self):
        """Muestra estadísticas detalladas por sensor"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            # Crear widget personalizado para mostrar estadísticas
            stats_dialog = QDialog(self)
            stats_dialog.setWindowTitle("Estadísticas Avanzadas")
            layout = QVBoxLayout()
            
            # Pestañas para cada sensor
            tab_widget = QTabWidget()
            
            for sensor_num in range(1, 5):
                stats = self.db_manager.get_sensor_stats(
                    sensor_num, 
                    start_date=start_date, 
                    end_date=end_date
                )
                
                # Crear contenido para cada pestaña
                tab = QWidget()
                tab_layout = QFormLayout()
                
                # Agregar estadísticas
                tab_layout.addRow("Temperatura Promedio:", QLabel(f"{stats['media_temp']:.2f} °C"))
                tab_layout.addRow("Máxima:", QLabel(f"{stats['max_temp']:.2f} °C"))
                tab_layout.addRow("Mínima:", QLabel(f"{stats['min_temp']:.2f} °C"))
                tab_layout.addRow("Desviación Estándar:", QLabel(f"{stats['desviacion_absoluta']:.2f} °C"))
                tab_layout.addRow("Eventos Fuera de Rango:", 
                                QLabel(f"{stats['eventos_fuera_rango']} ({stats['eventos_fuera_rango']/stats['total_registros']:.1%})"))
                
                tab.setLayout(tab_layout)
                tab_widget.addTab(tab, f"Sensor {sensor_num}")
            
            layout.addWidget(tab_widget)
            stats_dialog.setLayout(layout)
            stats_dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular estadísticas:\n{str(e)}")

    def compare_sensors(self):
        """Compara el comportamiento de todos los sensores"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            comparison = self.db_manager.compare_sensors(start_date, end_date)
            
            # Crear tabla de comparación
            table = QTableWidget()
            table.setRowCount(4)  # 4 sensores
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels([
                "Sensor", "Temp. Promedio", "Desviación", 
                "Outliers", "% Fuera de Rango"
            ])
            
            for i in range(4):
                sensor_num = i + 1
                table.setItem(i, 0, QTableWidgetItem(f"Sensor {sensor_num}"))
                table.setItem(i, 1, QTableWidgetItem(f"{comparison[f'avg_temp{sensor_num}']:.2f} °C"))
                table.setItem(i, 2, QTableWidgetItem(f"{comparison[f'avg_dev{sensor_num}']:.2f} °C"))
                table.setItem(i, 3, QTableWidgetItem(str(comparison[f'outliers{sensor_num}'])))
                
                total_records = len(self.db_manager.get_data_between_dates(start_date, end_date))
                percent = comparison[f'outliers{sensor_num}'] / total_records * 100
                table.setItem(i, 4, QTableWidgetItem(f"{percent:.1f}%"))
            
            # Mostrar en diálogo
            dialog = QDialog(self)
            dialog.setWindowTitle("Comparación de Sensores")
            layout = QVBoxLayout()
            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al comparar sensores:\n{str(e)}")

    def show_temperature_distribution(self):
        """Muestra histogramas en ventana separada"""
        try:
            start_date = self.fechaInicio.date().toString("yyyy-MM-dd")
            end_date = self.fechaFin.date().toString("yyyy-MM-dd")
            
            # Crear ventana de diálogo para los gráficos
            plot_dialog = QDialog(self)
            plot_dialog.setWindowTitle("Distribución de Temperaturas")
            plot_dialog.resize(800, 600)
            
            # Crear figura matplotlib
            figure, axes = plt.subplots(2, 2, figsize=(10, 8))
            figure.suptitle('Distribución por Sensor')
            
            for i, ax in enumerate(axes.flat):
                sensor_num = i + 1
                df = self.db_manager.get_temperature_distribution(
                    sensor_num, 
                    start_date, 
                    end_date
                )
                
                if not df.empty:
                    ax.hist(df['temperatura'], bins=15, alpha=0.7)
                    ax.set_title(f'Sensor {sensor_num}')
                    ax.grid(True)
            
            # Integrar matplotlib en el diálogo
            canvas = FigureCanvas(figure)
            layout = QVBoxLayout(plot_dialog)
            layout.addWidget(canvas)
            
            plot_dialog.exec()
        
        except Exception as e:
            QMessageBox.critical(self, "Error",  f"Error al generar histogramas:\n{str(e)}")
       

    def show_matplotlib_figure(self, figure):
        """Muestra una figura de matplotlib en la interfaz"""
        # Limpiar figura anterior si existe
        if hasattr(self, 'mpl_canvas'):
            self.ui.plot_layout.removeWidget(self.mpl_canvas)
            self.mpl_canvas.deleteLater()
        
        # Crear nuevo canvas
        self.mpl_canvas = FigureCanvas(figure)
        self.ui.plot_layout.addWidget(self.mpl_canvas)
        self.mpl_canvas.draw() 
    def setup_plot_area(self):
        """Configura el área para mostrar gráficos matplotlib"""
        # Crear un contenedor para el gráfico
        self.plot_container = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_container.setLayout(self.plot_layout)
        
        # Añadir al layout principal (ajusta según tu UI)
        # Si tienes un QScrollArea o similar, usa:
        # self.ui.scrollArea.setWidget(self.plot_container)
        
        # O simplemente añádelo a tu layout principal:
        self.ui.verticalLayout.addWidget(self.plot_container)  # Ajusta 'verticalLayout' según tu diseño
        
        # Inicializar figura matplotlib
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.plot_layout.addWidget(self.canvas)          
