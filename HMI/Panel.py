
import sqlite3
from PyQt6.QtWidgets import QWidget, QMessageBox,QApplication

from panelPrincipal import PanelPrincipal
from plcs7.ConexionPLC import PLC_S7_Communicator
from PyQt6.QtCore import QTimer,QThread, pyqtSignal, QMutex
from PyQt6.QtGui import QColor, QPalette,QIcon
import sys
import struct
from PyQt6.QtCore import Qt,QMargins,QSize
import fotos

from PyQt6.QtGui import QPixmap

import fotos

class Panel(QWidget):    
     def __init__(self):
        super().__init__()        
         # Initialize the UI from the generated 'main_ui' class
        self.ui = PanelPrincipal()
        self.ui.setupUi(self)
        self.plcConectado=False     
        self.plc=None
        self.setWindowIcon(QIcon(":/control/Imagenes/histeresis.png"))
        
        
           # Configuración de la base de datos
        self.db_name = "./pe.db"
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
       
        
        
        self.timer = QTimer()
      # Timer para el círculo pequeño (encender y apagar)
       # self.timer_circulo = QTimer(self)
        #self.timer_circulo.timeout.connect(self.cambiar_color_circulo)
        #self.timer_circulo.start(1000)  # Cambia cada 1000 ms (1 segundo)
        
        # Configurar el diálogo para que no tenga bordes
        # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        
         # Ajustar la altura de la fila al contenido
         # Mostrar el diálogo maximizado
        self.showMaximized()
        self.manual_previo = None  # Guarda el último estado de Manual
        self.leerValores=True      # Guarda el estado para leer los valores de configuracion del PLC 
      
        
            # Configuración mejorada de botones
        self.botones_habilitados = False # Control global

        # Mapeo completo de botones con sus propiedades
        self.botones_config = {
            'btn_Resistencia1': {
                'object': self.ui.btn_Resistencia1,
                'bit_offset': 0,  # M1.0
                'estado_inicial': False,
                'textos': ("Encender", "Apagar")
            },
            'btn_Resistencias_2': {
                'object': self.ui.btn_Resistencias_2,
                'bit_offset': 1,  # M1.1
                'estado_inicial': False,
                'textos': ("Encender", "Apagar")
            },
            
            'btn_Resistencias_4': {
                'object': self.ui.btn_Resistencias_4,
                'bit_offset': 3,  # M1.3
                'estado_inicial': False,
                'textos': ("Encender", "Apagar")
            }
        }

        # Inicialización avanzada de botones
        for nombre, config in self.botones_config.items():
            boton = config['object']
            if boton:  # Verificación de que el botón existe
                boton.setCheckable(True)
                boton.clicked.connect(self.on_boton_clicked)
                boton.setEnabled(self.botones_habilitados)
                
                # Propiedades personalizadas
                boton.setProperty('bit_offset', config['bit_offset'])
                boton.setProperty('current_state', config['estado_inicial'])
                boton.setProperty('text_on', config['textos'][1])
                boton.setProperty('text_off', config['textos'][0])
                
                # Estado visual inicial
                self.actualizar_estado_boton(boton, config['estado_inicial'])
        
    
         
        
        
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        # Conectar al PLC
        try:
            # Crear una instancia de PLC_S7_Communicator
             self.plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC
             self.plcConectado=self.plc.connect()
             if(self.plcConectado):
                 # Temporizador para actualizar los datos
                print(f"Programa Aqui algun mensaje de error de Comunicacion ")
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
         # Botones de los Indicadores
       self.ui.btn_Alimentador.clicked.connect(self.app)
       self.ui.btn_Compresor.clicked.connect(self.app)   
       self.ui.btn_Extrusora.clicked.connect(self.app)
       self.ui.btn_Resistencia1.clicked.connect(self.toggle_button_Resistencia1)
       
       
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
     
       self.ui.Cerrar.clicked.connect(self.cerrarApp)
       #Botnes de maximizar y minimizar
       self.ui.maximizar.clicked.connect(self.maximize_window)
       self.ui.minimizar.clicked.connect(self.showMinimized)
       
       #ÛPonemos en visible falso los boitnes pq noi se va a usar pero en el futuro si 
       self.ui.btn_Extrusora.setVisible(False)
       self.ui.btn_Compresor.setVisible(False)
       self.ui.btn_Alimentador.setVisible(False)
       self.ui.btn_Extrusora.setVisible(False)
    
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
             
     def maximize_window(self):
        # Alternar entre maximizar y restaurar
        if self.isMaximized():
            self.showNormal()
           
        else:
            self.showMaximized()          
     def establecerTime(self):
        """Establece un valor entero en el PLC con validación"""
        try:
            # Detener temporalmente el timer
            self.timer.stop()
            
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
            
                
        except Exception as e:
          QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
        finally:
            # Reanudar el timer
            self.timer.start()
      
     def toggle_bitResistencia1(self):
        """Encender Resistencia 1"""
        
        """Escribe 1 y luego 0 en M1.0 con un pequeño retraso"""
        # Escribir 1
       # self.plc.write_marker(2, 1, 0)
       # self.plc.write_variable_word(10,200)
        
        # Usar QTimer para escribir 0 después de 500ms (medio segundo)
        #QTimer.singleShot(500, lambda: self.plc.write_marker(2, 1, 0)) 
        
         
     def establecerSetPointT (self):       
        """Escribe en VD120."""
        try:
            self.timer.stop()
            value = float(self.ui.t.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 120, data)
            self.ui.t.setText("")            
            self.leerValores=True            
        except Exception as e:
            print(f"Error al escribir en VD120: {e}")
        finally:
            self.timer.start()    
            
            
     def Zona2_establecerSetPointT (self):  
        """Escribe en VD146."""
        try:
            self.timer.stop()
            value = float(self.ui.t1_SP_zona2.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 146, data)
            self.ui.t1_SP_zona2.setText("")            
            self.leerValores=True            
        except Exception as e:
            print(f"Error al escribir en VD146: {e}")
        finally:
            self.timer.start() 
            
            
                  
     def establecerSetPointT1 (self):
        """Escribe en VD120."""
        try:
            self.timer.stop()
            value = float(self.ui.t1.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 134, data)
            self.ui.t1.setText("")
            
          
            self.leerValores=True
            
        except Exception as e:
            print(f"Error al escribir en VD120: {e}")
        finally:
            self.timer.start()  
        
     def establecerHisteresisT (self):
        """Escribe en VD124."""
        try:
            self.timer.stop()
            value = float(self.ui.h.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 124, data)
            self.ui.h.setText("")
            self.leerValores=True
            
        except Exception as e:
            print(f"Error al escribir en VD122: {e}")
        finally:
            self.timer.start()      
         
     def Zona2_establecerHisteresisT (self):
        """Escribe en VD150."""
        try:
            self.timer.stop()
            value = float(self.ui.t1_Hit_zona2.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 150, data)
            self.ui.t1_Hit_zona2.setText("")
            self.leerValores=True            
        except Exception as e:
            print(f"Error al escribir en VD150: {e}")
        finally:
            self.timer.start()  
     def Aire_establecerHisteresisT (self):
        """Escribe en VD162."""
        try:
            self.timer.stop()
            value = float(self.ui.Hist_temp_Aire_texto.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 162, data)
            self.ui.Hist_temp_Aire_texto.setText("")
            self.leerValores=True            
        except Exception as e:
            print(f"Error al escribir en VD158: {e}")
        finally:
            self.timer.start() 
     def Aire_establecerSetPointT1 (self):
        """Escribe en VD158."""
        try:
            self.timer.stop()
            value = float(self.ui.Sp_temp_Aire_texto.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 158, data)
            self.ui.Sp_temp_Aire_texto.setText("")          
            self.leerValores=True            
        except Exception as e:
            print(f"Error al escribir en VD158: {e}")
        finally:
            self.timer.start()         
     def establecerHisteresisT1 (self):
        """Escribe en VD138."""
        try:
            self.timer.stop()
            value = float(self.ui.h1.text())
            data = struct.pack('>f', value)  # Convierte el flotante a bytes
            self.plc.write_vd(1, 138, data)
            self.ui.h1.setText("")
            self.leerValores=True
            
        except Exception as e:
            print(f"Error al escribir en VD120: {e}")
        finally:
            self.timer.start()         
         
     def cambiar_color_circuloZOna1(self):
        # Alterna entre gris (apagado) y verde (encendido)
        if self.ui.indcadorTemp1.palette().color(QPalette.ColorRole.Window) == QColor("gray"):
            self.ui.indcadorTemp1.setStyleSheet(
                """
                QLabel {
                    background-color: red;
                    border-radius: 5px;
                }
                """
            )
            self.ui.indcadorTemp1_2.setStyleSheet(
                """
                QLabel {
                    background-color: red;
                    border-radius: 5px;
                }
                """
            )
            
        else:
           self.ui.indcadorTemp1.setStyleSheet(
                    """
                    QLabel {
                        background-color: gray;
                        border-radius: 5px;
                    }
                    """
                )
           self.ui.indcadorTemp1_2.setStyleSheet(
                """
                QLabel {
                    background-color: gray;
                    border-radius: 5px;
                }
                """
            )
          
     def cambiar_color_circuloZOna2(self):
        # Alterna entre gris (apagado) y verde (encendido)
        if self.ui.indcadorTemp1_3.palette().color(QPalette.ColorRole.Window) == QColor("gray"):
           
            self.ui.indcadorTemp1_3.setStyleSheet(
                """
                QLabel {
                    background-color: red;
                    border-radius: 5px;
                }
                """
            )
            self.ui.indcadorTemp1_4.setStyleSheet(
                """
                QLabel {
                    background-color: red;
                    border-radius: 5px;
                }
                """
            )
        else:
           
           self.ui.indcadorTemp1_3.setStyleSheet(
                """
                QLabel {
                    background-color: gray;
                    border-radius: 5px;
                }
                """
            )
           self.ui.indcadorTemp1_4.setStyleSheet(
                """
                QLabel {
                    background-color: gray;
                    border-radius: 5px;
                }
                """
            )
         
     def cambiar_color_circuloCabezal(self):
        # Alterna entre gris (apagado) y verde (encendido)
        if self.ui.indcadorTempCabezal.palette().color(QPalette.ColorRole.Window) == QColor("gray"):
            self.ui.indcadorTempCabezal.setStyleSheet(
                """
                QLabel {
                    background-color: red;
                    border-radius: 5px;
                }
                """
            )
            
        else:
          self.ui.indcadorTempCabezal.setStyleSheet(
                    """
                    QLabel {
                        background-color: gray;
                        border-radius: 5px;
                    }
                    """
                )
     def cambiar_color_circuloMotorExtrusora(self):
        # Alterna entre gris (apagado) y verde (encendido)
        if self.ui.indcadorMotorExtrusora.palette().color(QPalette.ColorRole.Window) == QColor("gray"):
            self.ui.indcadorMotorExtrusora.setStyleSheet(
                """
                QLabel {
                    background-color: red;
                    border-radius: 5px;
                }
                """
            )
            
        else:
          self.ui.indcadorMotorExtrusora.setStyleSheet(
                    """
                    QLabel {
                        background-color: gray;
                        border-radius: 5px;
                    }
                    """
                )      
     def cambiar_color_circuloAlimentacion(self):
        # Alterna entre gris (apagado) y verde (encendido)
        if self.ui.indcadorMotorExtrusora_2.palette().color(QPalette.ColorRole.Window) == QColor("gray"):
            self.ui.indcadorMotorExtrusora_2.setStyleSheet(
                """
                QLabel {
                    background-color: green;
                    border-radius: 5px;
                }
                """
            )
            
        else:
          self.ui.indcadorMotorExtrusora_2.setStyleSheet(
                    """
                    QLabel {
                        background-color: gray;
                        border-radius: 5px;
                    }
                    """
                )          
     def update_data(self):
        """Actualiza los datos en la interfaz."""
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
                    # Inicialización avanzada de botones
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
                            self.actualizar_estado_boton(boton,  self.botones_habilitados)
        
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
           temp1 = self.plc.read_variable_float(100)  # Lee 4 bytes de VD100          
           self.ui.temp1.setText(f"{temp1:.2f} °C")
           # Leer VD104
           temp2 = self.plc.read_variable_float(104)  # Lee 4 bytes de VD104          
           self.ui.temp2.setText(f"{temp2:.2f} °C")
            # Leer VD108
           temp3 = self.plc.read_variable_float(106)  # Lee 4 bytes de VD106          
           self.ui.temp3.setText(f"{temp3:.2f} °C")
           
           # Leer VD108 temperatura Aire
           tempAire = self.plc.read_variable_float(108)  # Lee 4 bytes de VD108        
           self.ui.temp_Aire.setText(f"{tempAire:.2f} °C")
           
           
           #self.cursor.execute(""" INSERT INTO lecturas_temperatura (t11, t2, t3,setpoint_id)
           # VALUES (?, ?, ?,?)
          #  """, (temp1, temp2, temp3,1))
        
          
        
             # Solo actúa si el estado de self.leerValores cambió pq se cambio algun valor !!!!
           if self.leerValores :
                self.leerValores=False          
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
           
           
           
           #Label del motor de la Extrusora si esta funcuionando 
           #motorEXtrusora = self.plc.read_marker_bit(0,2)
           # Leer entrada (I0.0)
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
                
           if not motorEXtrusora:
               self.cambiar_color_circuloMotorExtrusora()    
            #Label del motor de la Extrusora si esta funcuionando 
           #motorEXtrusora = self.plc.read_marker_bit(0,2)
           # Leer entrada (I0.0)
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
           
           if motorAlimnetador:
               self.cambiar_color_circuloAlimentacion()
               
           
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
           
           if  not Resistencia4:
                self.cambiar_color_circuloCabezal()
           if not (Resistencia1  ) :               
                self.cambiar_color_circuloZOna1() 
           if not (Resistencia2  ) :               
                self.cambiar_color_circuloZOna2()  
           # Falta del Aire       
              
        except Exception as e:
            print(f"Error al leer datos: {e}")  
       
     def toggle_button_Resistencia1(self):
        """Cambia entre estados Encender/Apagar"""
        is_red = self.ui.btn_Resistencia1.isChecked()
        self.ui.btn_Resistencia1.setText("Apagar" if is_red else "Encender")
        self.ui.btn_Resistencia1.setStyleSheet(self.get_button_style(is_red))  
       
     def get_button_style(self, is_red):
        return """
            QPushButton {
                background-color: %s;
                border: 2px solid %s;
                border-radius: 5px;  /* Reducido para 41px de altura */
                color: white;
                font-size: 11px;    /* Tamaño ajustado */
                font-weight: bold;
                padding: 1px 5px;   /* Mínimo padding para 111x41 */
                margin: 2px;         /* Evita recorte */
            }
            QPushButton:hover {
                background-color: %s;
            }
            QPushButton:pressed {
                background-color: %s;
                padding-left: 7px;  /* Ajuste fino para el efecto */
                padding-top: 3px;
            }
        """ % (
            "#FF4444" if is_red else "#4CAF50",  # Color normal
            "#CC0000" if is_red else "#45a049",  # Borde
            "#FF6666" if is_red else "#66BB6A",  # Hover
            "#CC0000" if is_red else "#367c39"   # Pressed
        )
       
     def app(self): 
         print("Cambiar") 
         
     def closeEvent(self, event):
        """Desconecta el PLC al cerrar la aplicación."""
        self.plc.disconnect()
        self.conn.close()
        event.accept()
     def actualizar_estado_boton(self, boton, estado):
        """Actualiza completamente el estado visual de un botón"""
        if not boton:
            return
        
        boton.setProperty('current_state', estado)
        boton.setChecked(estado)
        boton.setText(boton.property('text_on') if estado else boton.property('text_off'))
        boton.setStyleSheet(self.estilo_boton(estado, not self.botones_habilitados))   
        
        
     #### aqui implementamos la logica para los botones delas resistencias def configurar_boton(self, boton, nombre):
     def estilo_boton(self, estado, is_disabled=False):
        """Retorna el CSS para el botón basado en estado (True/False) y si está deshabilitado"""
        if is_disabled:
            return """
                QPushButton {
                    background-color: #CCCCCC;
                    border: 2px solid #999999;
                    color: #666666;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 1px 5px;
                    min-width: 111px;
                    min-height: 41px;
                }
            """
        
        color_normal = "#FF4444" if estado else "#4CAF50"
        color_borde = "#CC0000" if estado else "#45a049"
        color_pressed = "#990000" if estado else "#367C39"
        
        return f"""
            QPushButton {{
                background-color: {color_normal};
                border: 2px solid {color_borde};
                border-radius: 5px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 1px 5px;
                min-width: 111px;
                min-height: 41px;
            }}
            QPushButton:pressed {{
                background-color: {color_pressed};
                border: 2px solid {color_borde};
            }}
        """

     def on_boton_clicked(self):
        """Maneja el clic en cualquier botón"""
        if not self.botones_habilitados:
            return
        
        boton = self.sender()
        if not boton:
            return
        
        try:
            self.timer.stop()
            # Deshabilitar temporalmente el botón
            boton.setEnabled(False)
            bit_offset = boton.property('bit_offset')
            
            # 1. Leer estado actual del PLC
            estado_actual = self.plc.read_marker_bit(1, bit_offset)
            
            # 2. Invertir el estado
            nuevo_estado = not estado_actual
            
            # 3. Escribir nuevo estado en el PLC
            self.plc.write_marker(1, bit_offset, nuevo_estado)
            
          
            self.actualizar_estado_boton(boton, nuevo_estado)
               
           
            
            # Reactivar después de 500ms
            QTimer.singleShot(500, lambda: boton.setEnabled(self.botones_habilitados))
            
        except Exception as e:
            print(f"Error en botón {boton.objectName()}: {str(e)}")
            boton.setEnabled(True)
        finally:
             self.timer.start()    
        
     def reactivar_boton(self, boton):
        """Reactiva el botón manteniendo su estado actual"""
        if not boton:
            return
        
        try:
            estado_actual = boton.property("current_state")
            boton.setEnabled(True)
            boton.setStyleSheet(self.estilo_boton(estado_actual))
        except Exception as e:
            print(f"Error reactivando botón: {str(e)}")
            boton.setEnabled(True)
            boton.setStyleSheet(self.estilo_boton(False))
    
     def set_botones_habilitados(self, habilitar):
        """Habilita/deshabilita todos los botones según la variable booleana"""
        self.botones_habilitados = habilitar
        for boton in self.botones:
            boton.setEnabled(habilitar)
            if not habilitar:
                boton.setChecked(False)
                boton.setStyleSheet(self.estilo_boton(False))
                boton.setText("Encender")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear una instancia de PLC_S7_Communicator
    plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC

    # Crear y mostrar la ventana principal
    window = Panel()
    window.show()

    sys.exit(app.exec())    