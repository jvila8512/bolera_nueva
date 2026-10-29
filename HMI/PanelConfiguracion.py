
from datetime import datetime
import sqlite3
from PyQt6.QtWidgets import  QDialog,QWidget, QMessageBox, QApplication

from HMI.VistaConfiguracion import VistaConfiguracion
from plcs7.ConexionPLC import PLC_S7_Communicator
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QMutex
from PyQt6.QtGui import QColor, QPalette, QIcon
import sys
import struct
from PyQt6.QtCore import Qt, QMargins, QSize
import fotos
from PyQt6.QtGui import QPixmap

class PanelConfiguracion(QDialog):    
    def __init__(self, parent=None):
        super().__init__(parent)     
        # Initialize the UI from the generated 'main_ui' class
        self.ui = VistaConfiguracion()
        self.ui.setupUi(self)
        self.setWindowTitle("Configuración General")
        self.move(0, 0)  # Posición (x,y)
   
        self.plc = None
        self.setWindowIcon(QIcon(":/control/Imagenes/histeresis.png"))
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
        self.plcConectado=False
         # Conectar al PLC
        try:
            # Crear una instancia de PLC_S7_Communicator
             self.plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC
             self.plcConectado=self.plc.connect()
             if(self.plcConectado):
                     print(f"COnfiguracion de los Parametros ")
                     self.actualizarValores()
                 # Temporizador para actualizar los datos
                #self.timer.timeout.connect(self.update_data)
                #self.timer.start(1000)  # Actualizar cada 1/2 segundo  
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
       self.ui.btnT.clicked.connect(self.establecerSetPointT)
       self.ui.btnH.clicked.connect(self.establecerHisteresisT)
      
       
       #Botones de Configuracion temperatura Zona 2
       self.ui.btnT1_Zona2.clicked.connect(self.Zona2_establecerSetPointT)
       self.ui.btnHist_Zona2.clicked.connect(self.Zona2_establecerHisteresisT)
        
        
       #Botones de Configuracion temperatura Zona 3 Cabezal 
       self.ui.btnT1.clicked.connect(self.establecerSetPointT1)      
       self.ui.btnH1.clicked.connect(self.establecerHisteresisT1)
       
       
       #COnfiguracion tempeartura del Aire....
       self.ui.btnT1_Zona2_3.clicked.connect(self.Aire_establecerSetPointT1)       
       self.ui.btnHist_Zona2_3.clicked.connect(self.Aire_establecerHisteresisT)
      
       #Boton para establecer tiempo de Enecido de Motor Exrusora 
       self.ui.btn_Tiempo.clicked.connect(self.establecerTime)
       
     
    def actualizarValores (self):
        
        #Set Point  y Histeresis ZOna 1
                sp = self.plc.read_variable_float(120)  # Lee 4 bytes de VD120         
                self.ui.temp_referencia.setText(f"{sp:.0f} °C")               
                setH = self.plc.read_variable_float(124)  # Lee 4 bytes de VD124         
                self.ui.temp_referencia_2.setText(f"{setH:.0f} °C")
                
                #Set Point  y Histeresis Zona 2
                sp = self.plc.read_variable_float(146)  # Lee 4 bytes de VD146         
                self.ui.Sp_temp_Zona2.setText(f"{sp:.0f} °C")               
                setH = self.plc.read_variable_float(150)  # Lee 4 bytes de VD150        
                self.ui.Hist_temp_Zona2.setText(f"{setH:.0f} °C")                
                              
                #Set Pont y Histeresis de la temp Cabezal
                setPT1 = self.plc.read_variable_float(134)  # Lee 4 bytes de VD134        
                self.ui.temp_referencia_3.setText(f"{setPT1:.0f} °C")                                               
                setHt1 = self.plc.read_variable_float(138)  # Lee 4 bytes de VD138         
                self.ui.temp_referencia_4.setText(f"{setHt1:.0f} °C")
                
                #Set Point  y Histeresis Temeratura del Aire
                sp = self.plc.read_variable_float(158)  # Lee 4 bytes de VD158         
                self.ui.Sp_temp_Aire.setText(f"{sp:.0f} °C")               
                setH = self.plc.read_variable_float(162)  # Lee 4 bytes de VD162        
                self.ui.Hist_temp_Aire.setText(f"{setH:.0f} °C")  
                
                
                tiempo=self.plc.read_variable_word(10)
                minutos=tiempo/600
                self.ui.label_tiempo.setText(f"{minutos:.0f}")
       
       
    def cerrarApp(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Confirmación")         
        msgBox.setText(f"¿Estás seguro de cerrar la Configuración?")
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setStandardButtons( QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)          
                # Obtén el botón "Yes"
        boton_si = msgBox.button(QMessageBox.StandardButton.Yes)
         # Cambia el texto del botón a "Sí"
        boton_si.setText("Sí")
           # Muestra el mensaje y obtiene la respuesta
        respuesta = msgBox.exec()
        if respuesta == QMessageBox.StandardButton.Yes:    
             self.plc.disconnect()               
             self.close()   
    def establecerTime(self):
        """Establece un valor entero en el PLC con validación"""
        try:
            # Detener temporalmente el timer
         
            
            # Obtener y validar el texto
            texto = self.ui.tiempo.text().strip()
            
            if not texto:
                QMessageBox.warning(
                self,
                "Campo vacío",
                "Por favor ingrese un valor numérico",
                QMessageBox.StandardButton.Ok
                )
                return
                
            if not texto.isdigit():
                QMessageBox.critical(
                self,
                "Valor inválido",
                "Solo se permiten números enteros (sin decimales o caracteres)",
                QMessageBox.StandardButton.Ok
                    )
                return
                
            minutos = int(texto)
        
            # Validar rango
            if not (1 <= minutos <= 54):
                QMessageBox.warning(
                    self,
                    "Atención",
                    "El tiempo debe estar entre 1 y 54 minutos"
                )
                return
                
            
            unidades = minutos * 600
            self.plc.write_variable_word(10, unidades)
            self.ui.tiempo.setText("")
            self.leerValores=True
            QMessageBox.information(
                        self,
                        "Listo",
                        f"Activación de Motor Extrusora  programado a {minutos} minutos después de alcanzar temperatura de Referencia"
                    )
            
            self.actualizarValores()  
        except Exception as e:
          QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
        finally:
            # Reanudar el timer
            self.timer.start()         
    def establecerSetPointT (self):       
        """Escribe en VD120."""
        try:
         
            value = float(self.ui.t.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 120, data)
            self.ui.t.setText("")            
            self.leerValores=True  
            self.actualizarValores()            
        except Exception as e:
            print(f"Error al escribir en VD120: {e}")
          
            
            
    def Zona2_establecerSetPointT (self):  
        """Escribe en VD146."""
        try:
            
            value = float(self.ui.t1_SP_zona2.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 146, data)
            self.ui.t1_SP_zona2.setText("")            
            self.leerValores=True   
            self.actualizarValores()           
        except Exception as e:
            print(f"Error al escribir en VD146: {e}")
        
            
            
                  
    def establecerSetPointT1 (self):
        """Escribe en VD120."""
        try:
           
            value = float(self.ui.t1.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 134, data)
            self.ui.t1.setText("")
            
          
            self.leerValores=True
            self.actualizarValores()
            
        except Exception as e:
            print(f"Error al escribir en VD120: {e}")
       
        
    def establecerHisteresisT (self):
        """Escribe en VD124."""
        try:
      
            value = float(self.ui.h.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 124, data)
            self.ui.h.setText("")
            self.leerValores=True
            self.actualizarValores()
            
        except Exception as e:
            print(f"Error al escribir en VD122: {e}")
        
         
    def Zona2_establecerHisteresisT (self):
        """Escribe en VD150."""
        try:
       
            value = float(self.ui.t1_Hit_zona2.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 150, data)
            self.ui.t1_Hit_zona2.setText("")
            self.leerValores=True
            self.actualizarValores()            
        except Exception as e:
            print(f"Error al escribir en VD150: {e}")
      
    def Aire_establecerHisteresisT (self):
        """Escribe en VD162."""
        try:
            
            value = float(self.ui.Hist_temp_Aire_texto.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 162, data)
            self.ui.Hist_temp_Aire_texto.setText("")
            self.leerValores=True
            self.actualizarValores()            
        except Exception as e:
            print(f"Error al escribir en VD158: {e}")
        
    def Aire_establecerSetPointT1 (self):
        """Escribe en VD158."""
        try:
            
            value = float(self.ui.Sp_temp_Aire_texto.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 158, data)
            self.ui.Sp_temp_Aire_texto.setText("")          
            self.leerValores=True     
            self.actualizarValores()       
        except Exception as e:
            print(f"Error al escribir en VD158: {e}")
               
    def establecerHisteresisT1 (self):
        """Escribe en VD138."""
        try:
           
            value = float(self.ui.h1.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 138, data)
            self.ui.h1.setText("")
            self.leerValores=True
            self.actualizarValores()
            
        except Exception as e:
            print(f"Error al escribir en VD120: {e}")
    def closeEvent(self, event):
        """Método que se ejecuta al cerrar la aplicación"""
        # Detener el timer antes de cerrar
        
        
        # Cualquier otra limpieza que necesites hacer...
        if self.plcConectado and self.plc:
            self.plc.disconnect()
        
        super().closeEvent(event)   