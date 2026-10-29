from datetime import datetime
import sqlite3
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication

from HMI.BD import DatabaseManager
from HMI.PanelConfiguracion import PanelConfiguracion

from HMI.VistaPrincipal import VistaPrincipal


from plcs7.ConexionPLC import PLC_S7_Communicator
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import  QIcon
import sys

from PyQt6.QtCore import Qt
import fotos
from PyQt6.QtGui import QPixmap

# Importa la clase DatabaseManager que te proporcioné anteriormente


class PanelControl(QWidget):    
    def __init__(self):
        super().__init__()        
        # Initialize the UI from the generated 'main_ui' class
        self.ui = VistaPrincipal()
        self.ui.setupUi(self)
        self.plcConectado = False     
        self.plc = None
        self.setWindowIcon(QIcon(":/control/Imagenes/histeresis.png"))
        # Inicializar labels de temperatura con valor por defecto y centrado
        self.ui.temp1.setText("-- °C")
        self.ui.temp2.setText("-- °C")
        self.ui.temp3.setText("-- °C")
        self.ui.temp_Aire.setText("-- °C")
        self.ui.temp1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.temp2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.temp3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.temp_Aire.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Inicializa el DatabaseManager
        self.db_manager = DatabaseManager("./temperaturasPe.db")
        
        # Configura el timer para insertar datos cada 10 segundos
        self.timer_db = QTimer(self)
        self.timer_db.timeout.connect(self.insertar_datos_periodicamente)
        self.timer_db.start(20000)  # 10,000 ms = 10 segundos
        
        # Otras inicializaciones que ya tengas...
        self.timer = QTimer()
     
        # Configurar el diálogo para que no tenga bordes
        # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
          # Ajustar la altura de la fila al contenido
         # Mostrar el diálogo maximizado
        self.showMaximized()
        self.manual_previo = None  # Guarda el último estado de Manual
        self.leerValores=True      # Guarda el estado para leer los valores de configuracion del PLC 
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        self.temp1=0
        self.temp2=0
        self.temp3=0
        self.tempAire=0
        self.sp_Temp1 = 0
        self.sp_Temp2  = 0
        self.sp_Temp3 = 0
        self.sp_TempAire = 0

        self.sh_Temp1 = 0
        self.sh_Temp2 = 0
        self.sh_Temp3 = 0
        self.sh_TempAire = 0
        # Conectar al PLC
        try:
            # Crear una instancia de PLC_S7_Communicator
             self.plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC
             self.plcConectado=self.plc.connect()
             if(self.plcConectado):
                 # Temporizador para actualizar los datos
                self.timer.timeout.connect(self.update_data)
                self.timer.start(1000)  # Actualizar cada 1/2 segundo  
             else:
                print(f"Programa Aqui algun mensaje de error de Comunicacion ")
                msgBox = QMessageBox(self)
                msgBox.setWindowTitle("Información")         
                msgBox.setText(f"No hay comunicación con el PLC. Por favor revisar o llamar Asistencia Técnica")
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.exec()    
             
             
        except Exception as e:
            print(f"Error al conectar al PLC: {e}")
       
        self.initGUI() 
    def initGUI(self):
       
       
       
       #Botones de Configuracion temperatura Zona 1
       self.ui.btn_configuracion.clicked.connect(self.abrir_COnfiguracion)
       
       self.ui.Cerrar.clicked.connect(self.cerrarApp)
    
       
    def app(self):
         print(f"Error al conectar al PLC: ")
        
         
    def abrir_COnfiguracion(self):
      
        cambiar= PanelConfiguracion()
        cambiar.exec()
        
    def cerrarApp(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Confirmación")         
        msgBox.setText(f"¿Estás seguro de cerrar?")
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setStandardButtons( QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)          
                # Obtén el botón "Yes"
        boton_si = msgBox.button(QMessageBox.StandardButton.Yes)
         # Cambia el texto del botón a "Sí"
        boton_si.setText("Sí")
           # Muestra el mensaje y obtiene la respuesta
        respuesta = msgBox.exec()
        if respuesta == QMessageBox.StandardButton.Yes:
           
                        
             self.close()    
        
    
    def insertar_datos_periodicamente(self):
     
     
       if self.plcConectado :
     
        """Método que se ejecuta cada 10 segundos para insertar datos"""
        try:
            # Aquí obtienes los datos de tus sensores o PLC
            # Ejemplo con datos dummy - reemplaza con tus datos reales
            self.temp1 = self.plc.read_variable_float(100)  # Lee 4 bytes de VD100          
            self.temp2 = self.plc.read_variable_float(104)  # Lee 4 bytes de VD104    
            self.temp3 = self.plc.read_variable_float(106)  # Lee 4 bytes de VD106         
            self.tempAire = self.plc.read_variable_float(108)  # Lee 4 bytes de VD108        
         
          # Obtener temperaturas (ejemplo)
            temps = [self.temp1, self.temp2, self.temp3, self.tempAire]
            
            self.sp_Temp1 = self.plc.read_variable_float(120)  # Lee 4 bytes de VD120
            self.sp_Temp2  = self.plc.read_variable_float(146)  # Lee 4 bytes de VD120
            self.sp_Temp3 = self.plc.read_variable_float(134)  # Lee 4 bytes de VD120
            self.sp_TempAire = self.plc.read_variable_float(158)  # Lee 4 bytes de VD120

            self.sh_Temp1 = self.plc.read_variable_float(124)
            self.sh_Temp2 = self.plc.read_variable_float(150)
            self.sh_Temp3 = self.plc.read_variable_float(138)
            self.sh_TempAire = self.plc.read_variable_float(162)
            
            
        
           # Obtener setpoints e histéresis (podrían venir de la tabla configuracion_sensores)
            
            setpoints = [self.sp_Temp1, self.sp_Temp2, self.sp_Temp3,self.sp_TempAire]
            hysteresis = [self.sh_Temp1,self.sh_Temp2,self.sh_Temp3,self.sh_TempAire]  # Valores de histéresis para cada sensor
        
            # Insertar con el DatabaseManager actualizado
            self.db_manager.insert_reading(
                temps=temps,
                setpoints=setpoints,
                hysteresis=hysteresis,
                observaciones=f"Lectura automática {datetime.now().strftime('%H:%M:%S')}"
            )
            print("Datos Insretaddossssssssssssssssssssssss") 
            # Si estás usando el PLC, podrías hacer algo como:
            # if self.plcConectado and self.plc:
            #     temperaturas = [self.plc.leer_temperatura(1), 
            #                   self.plc.leer_temperatura(2),
            #                   ...]
            
           
          
            
        except Exception as e:
            print(f"Error al insertar datos: {e}")
         
    
    def closeEvent(self, event):
        """Método que se ejecuta al cerrar la aplicación"""
        # Detener el timer antes de cerrar
        self.timer_db.stop()
        
        # Cualquier otra limpieza que necesites hacer...
        if self.plcConectado and self.plc:
            self.plc.disconnect()
        
        super().closeEvent(event)
    def update_data(self):
        
        if self.plcConectado :
            """Actualiza los datos en la interfaz."""
            print(f"Entroooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo {self.plcConectado}")
            try:    
            
                    # Ahora debemos leer la entrada I0.1 que es el modo Automatico 0 y Manual 1         
                        # Ahora vamos a configrar los botones para el modo Manual
                """Método llamado periódicamente (ej. con QTimer)"""
                Manual = self.plc.read_input_bit(0, 1)  # Lee I0.1
                
                    # Solo actúa si el estado de Manual cambió
                if Manual != self.manual_previo:
                        self.manual_previo = Manual
                        self.botones_habilitados=Manual
                        
                        if not Manual:
                        # self.ui.btn_Extrusora.setVisible(False)
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/encender.png")   
                            self.ui.label_TextoCOntrol.setText("Automático")              
                            scaled_pixmap = pixmap.scaled(131, 141, Qt.AspectRatioMode.KeepAspectRatio)
                            self.ui.label_Control.setPixmap(scaled_pixmap)
                            self.ui.label_Control.repaint()  # Fuerza redibujado
                            # Resetear botones
                           
                
                        else:
                        # self.ui.btn_Extrusora.setVisible(True)
                                    
                        
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/apagar.png") 
                            self.ui.label_TextoCOntrol.setText("Manual")              
                            scaled_pixmap = pixmap.scaled(131, 141, Qt.AspectRatioMode.KeepAspectRatio)
                            self.ui.label_Control.setPixmap(scaled_pixmap)
                            self.ui.label_Control.repaint()  # Fuerza redibujado
                                
                            for nombre, config in self.botones_config.items():
                                boton = config['object']
                                if boton:  # Verificación de que el botón existe                        
                                
                                    boton.setEnabled(self.botones_habilitados)                            
                                    # Propiedades personalizadas
                                    boton.setProperty('bit_offset', config['bit_offset'])
                                    boton.setProperty('current_state', config['estado_inicial'])
                                    boton.setProperty('text_on', config['textos'][1])
                                    boton.setProperty('text_off', config['textos'][0])                            
                                    # Estado visual inicial
                                    self.actualizar_estado_boton(boton,  not self.botones_habilitados) 
                                                    
                                
                        
                
                    
                # Leer VD100
                self.temp1 = self.plc.read_variable_float(100)  # Lee 4 bytes de VD100          
                self.ui.temp1.setText(f"{self.temp1:.2f} °C")
                # Leer VD104
                self.temp2 = self.plc.read_variable_float(104)  # Lee 4 bytes de VD104          
                self.ui.temp2.setText(f"{self.temp2:.2f} °C")
                    # Leer VD108
                self.temp3 = self.plc.read_variable_float(106)  # Lee 4 bytes de VD106          
                self.ui.temp3.setText(f"{self.temp3:.2f} °C")
                
                # Leer VD108 temperatura Aire
                self.tempAire = self.plc.read_variable_float(108)  # Lee 4 bytes de VD108        
                self.ui.temp_Aire.setText(f"{self.tempAire:.2f} °C")
                        
                
                motorEXtrusora= self.plc.read_input_bit(0,6)  # Lee 1 byte de la entrada I0.2
                print(f"Valor leído de PLC: {motorEXtrusora}")  # Depuración

                    
                if  motorEXtrusora:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/OFF.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen OFF")
                else:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/onO.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen ON")
                        
                scaled_pixmap = pixmap.scaled(101, 101, Qt.AspectRatioMode.KeepAspectRatio)
                self.ui.label_Extrusora.setPixmap(scaled_pixmap)
                self.ui.label_Extrusora.repaint()  # Fuerza redibujado
                        
                
                motorCompresor= self.plc.read_input_bit(0,7)  # Lee 1 byte de la entrada I0.2  

                if   motorCompresor:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/OFF.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen OFF")
                else:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/onO.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen ON")
                        
                scaled_pixmap = pixmap.scaled(101, 101, Qt.AspectRatioMode.KeepAspectRatio)
                self.ui.label_Compresor.setPixmap(scaled_pixmap)
                self.ui.label_Compresor.repaint()  # Fuerza redibujado
                
                motorAlimnetador= self.plc.read_input_bit(1,0)  # Lee 1 byte de la entrada I0.2
            
                if   motorAlimnetador:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/OFF.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen OFF")
                else:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/onO.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen ON")
                        
                scaled_pixmap = pixmap.scaled(101, 101, Qt.AspectRatioMode.KeepAspectRatio)
                self.ui.label_Alimentador.setPixmap(scaled_pixmap)
                self.ui.label_Alimentador.repaint()  # Fuerza redibujado
                
                        
                Resistencia1= self.plc.read_input_bit(0,5)  # Lee 1 byte de la entrada I0.5            
                if   Resistencia1:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/OFF.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen OFF")
                else:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/onO.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen ON")
                        
                scaled_pixmap = pixmap.scaled(101, 101, Qt.AspectRatioMode.KeepAspectRatio)
                self.ui.label_Resistencias.setPixmap(scaled_pixmap)
                self.ui.label_Resistencias.repaint()  # Fuerza redibujado
                
                Resistencia2= self.plc.read_input_bit(0,4)  # Lee 1 byte de la entrada I0.2 Puede ser I0.4 y I0.3 porque es la mimsa zona           
                if  Resistencia2:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/OFF.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen OFF")
                else:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/onO.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen ON")
                        
                scaled_pixmap = pixmap.scaled(101, 101, Qt.AspectRatioMode.KeepAspectRatio)
                self.ui.label_Resistencias_2.setPixmap(scaled_pixmap)
                self.ui.label_Resistencias_2.repaint()  # Fuerza redibujado
                
                
                
                Resistencia4= self.plc.read_input_bit(0,2)  # Lee 1 byte de la entrada I0.2            
                if   Resistencia4:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/OFF.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen OFF")
                else:
                        
                            pixmap = QPixmap(":/control/Imagenes/Nueva carpeta/onO.png")
                            if pixmap.isNull():
                                raise FileNotFoundError("No se pudo cargar imagen ON")
                        
                scaled_pixmap = pixmap.scaled(101, 101, Qt.AspectRatioMode.KeepAspectRatio)
                self.ui.label_Resistencias_4.setPixmap(scaled_pixmap)
                self.ui.label_Resistencias_4.repaint()  # Fuerza redibujado
                
            except Exception as e:
                print(f"Error al leer datos: {e}")     
              

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = PanelControl()
    main_app.show()
    sys.exit(app.exec())      