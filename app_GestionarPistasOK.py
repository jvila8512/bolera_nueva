import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget,QApplication,QMessageBox,QGridLayout,QSizePolicy,QLabel,QFileDialog,QSizePolicy
from PyQt6.QtCore import Qt,QMargins,QSize
from PyQt6.QtGui import QPixmap # Importa QIcon para usar iconos
from ConexionBD.conexion import Conexion

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QTimer, QDateTime,pyqtSignal

from ConexionBD.juego_Operaciones import JuegoBD_operaciones
from Crud.juegos.app_Resumen_JuegosUser import ResumenJuegosUser
from ProbarCodigos.CarruseldFotos import CarruselFotos
from ProbarCodigos.VideosCarrusel import VentanaVideo
from UI.pistasAdmin import PistasAdmin
from app_DialogoPistas import AdminPistas
from app_DialogoPistas2 import AdminPistas2
from app_TV1 import AnimacionTV1
from app_TV2 import AnimacionTV2
from bd_modelos.usuario import Usuario
from bd_modelos import Sesion
import shutil
import os
from ConexionBD import M221_Bolera
import bolos



class GestionPistas(QWidget):
    
    

    def __init__(self, parent, user: Usuario,sesion:Sesion):
        super().__init__()
         
         # Initialize the UI from the generated 'main_ui' class
        self.ui = PistasAdmin()
        self.ui.setupUi(self)  
        self.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        self.ui.label_3.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed) 
        self.ui.label_2.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        
        self.ui.bolos2.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        self.ui.bolos1.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        
        #Referencia Ventana Principalcls
        
        self.Dasboard =parent
         # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones()
        
        #Referencia a dialogo de Gestion de Pista 1
        self.pista1= None #Iniciliza la ventana secundaria como None
        self.pista2= None #Iniciliza la ventana secundaria como None
        #Referencia a la  sub-ventana de Pista1 Resltados
        self.ventana_ResultadosPista1 = None # Inicializamos la sub-ventana de Pista1 Resltados como None
        self.ventana_ResultadosPista2 = None # Inicializamos la sub-ventana de Pista1 Resltados como None
          
        self.ip_address = "192.168.0.2"  # Reemplaza con la IP de tu PLC
       # self.ip_address2 = "localhost"  # Reemplaza con la IP de tu PLC   
        self.ip_address1 = "192.168.0.1"  # Reemplaza con la IP de tu PLC
        #self.ip_address1 = "localhost"  # Reemplaza con la IP de tu PLC 
        self.conectadoPista1=None
        self.conectadoPista2=None

        self.m221cliente2 = M221_Bolera.M221(self.ip_address)          
        self.m221cliente = M221_Bolera.M221(self.ip_address1)
        
        
        #Conectar con los dos Automatas...
        try:       
            self.conectadoPista2=self.m221cliente2.connectar()
            self.conectadoPista1=self.m221cliente.connectar()
          
        except Exception as e:
          print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
          
        
        
        
        
        
          
              
         # Conectar a la base de datos  
        self.con = Conexion()  
        self.UserLogueado = user
        self.Sesion= sesion
        
        self.id_juego_1=0
        self.id_juego_2=0
         # Temporizador para actualizar cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_tiempo)
        self.timer.start(1000)  # 1000 ms = 1 segundo
        
        self.sub_window11 = None  # Inicializamos la sub-ventana del TV 1 como None
        self.sub_window22 = None  # Inicializamos la sub-ventana del TV 2 como None 
        
        # Mostrar el tiempo al iniciar
        self.mostrar_tiempo()
         # Crear varios QLabel del 1 al 10
        self.bolo1 = QLabel()
        self.bolo2 = QLabel()
        self.bolo3 = QLabel()
        self.bolo4 = QLabel()
        self.bolo5 = QLabel()
        self.bolo6 = QLabel()
        self.bolo7 = QLabel()
        self.bolo8 = QLabel()
        self.bolo9 = QLabel()
        self.bolo10 = QLabel()
        # Lista de QLabel
        self.bolosMostrar = [
                                self.bolo1,
                                self.bolo2,
                                self.bolo3,
                                self.bolo4,
                                self.bolo5,
                                self.bolo6,
                                self.bolo7,
                                self.bolo8,
                                self.bolo9,
                                self.bolo10
        ]
         # Crear varios QLabel del 1 al 10
        self.bolo11 = QLabel()
        self.bolo22 = QLabel()
        self.bolo33 = QLabel()
        self.bolo44 = QLabel()
        self.bolo55 = QLabel()
        self.bolo66 = QLabel()
        self.bolo77 = QLabel()
        self.bolo88 = QLabel()
        self.bolo99 = QLabel()
        self.bolo00 = QLabel()
        # Lista de QLabel
        self.bolosMostrar1 = [
                                self.bolo11,
                                self.bolo22,
                                self.bolo33,
                                self.bolo44,
                                self.bolo55,
                                self.bolo66,
                                self.bolo77,
                                self.bolo88,
                                self.bolo99,
                                self.bolo00
        ]
      
        self.initGUI() 
        self.create_bowling_pins()
        self.create_bowling_pins1()
        self.timer = QTimer()
        self.timer.timeout.connect(self.comunicacion_plc)
        self.timer.start(1000)  # Ejecuta `comunicacion_plc` cada 1000 milisegundos (1 segundo)
                    
    def initGUI(self):
       self.ui.btn_pista1.clicked.connect(self.abrirPista1)
       self.ui.btn_pista2.clicked.connect(self.abrirPista2)
       self.ui.btn_tv1.clicked.connect(self.abrirTV1)
       self.ui.btn_tv2.clicked.connect(self.abrirTV2)
       self.ui.pushButton_8.clicked.connect(self.abrirReportes)
       
       self.ui.pushButtonBolos1.clicked.connect(self.subirBoloPista1)
       self.ui.pushButton2Bolos2.clicked.connect(self.subirBoloPista2)
       self.ui.salva.clicked.connect(self.salva)
    
      # boton de menrgencia
       self.ui.pushButton_3.clicked.connect(self.Emergencia)
       
       self.ui.pushButtonBolos1.setEnabled(False)
       self.ui.pushButton2Bolos2.setEnabled(False)
     
      # Motor de la Bola
    def comunicacion_plc(self):
        
          try:
            if self.conectadoPista1 :        
                #Leo M10 bit 0 para saber si ya se activo la secuencia del juego Pista 1
                leerM0=self.m221cliente.leer_bit(10,1)
                print(f"Pista Activaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {leerM0}")
                #si esta en 1  esta activado el juego Pista 1 y comenzamos a Jugar
                if leerM0==1 : 
                    
                        
                        self.ui.pushButtonBolos1.setEnabled(True)
                        self.bolo1.setHidden(False) 
                        self.bolo2.setHidden(False) 
                        self.bolo3.setHidden(False)
                        self.bolo4.setHidden(False) 
                        self.bolo5.setHidden(False) 
                        self.bolo6.setHidden(False) 
                        self.bolo7.setHidden(False) 
                        self.bolo8.setHidden(False) 
                        self.bolo9.setHidden(False)
                        self.bolo10.setHidden(False)
        
                        #LEemos los bolos de la pista 1
                        bolo1 = self.m221cliente.leer_bit(104, 1)
                        if not bolo1:
                            pixmap = QPixmap(f":/bolo/fotos/bolo1.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo1.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo1T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo1.setPixmap(scaled_pixmap)
                            

                        bolo2 = self.m221cliente.leer_bit(107, 1)
                        if not bolo2:
                            pixmap = QPixmap(f":/bolo/fotos/bolo2.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo2.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo2T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo2.setPixmap(scaled_pixmap)
                        bolo3 = self.m221cliente.leer_bit(102, 1)
                        if not bolo3:
                            pixmap = QPixmap(f":/bolo/fotos/bolo3.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo3.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo3T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo3.setPixmap(scaled_pixmap)

                        bolo4 = self.m221cliente.leer_bit(108, 1)
                        if not bolo4:
                            pixmap = QPixmap(f":/bolo/fotos/bolo4.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo4.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo4T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo4.setPixmap(scaled_pixmap)

                        bolo5 = self.m221cliente.leer_bit(105, 1)
                        if not bolo5:
                            pixmap = QPixmap(f":/bolo/fotos/bolo5.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo5.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo5T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo5.setPixmap(scaled_pixmap)

                        bolo6 = self.m221cliente.leer_bit(101, 1)
                        if not bolo6:
                            pixmap = QPixmap(f":/bolo/fotos/bolo6.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo6.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo6T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo6.setPixmap(scaled_pixmap)

                        bolo7 = self.m221cliente.leer_bit(109, 1)
                        if not bolo7:
                            pixmap = QPixmap(f":/bolo/fotos/bolo7.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo7.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo7T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo7.setPixmap(scaled_pixmap)

                        bolo8 = self.m221cliente.leer_bit(106, 1)
                        if not bolo8:
                            pixmap = QPixmap(f":/bolo/fotos/bolo8.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo8.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo8T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo8.setPixmap(scaled_pixmap)

                        bolo9 = self.m221cliente.leer_bit(103, 1)
                        if not bolo9:
                            pixmap = QPixmap(f":/bolo/fotos/bolo9.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo9.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo9T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo9.setPixmap(scaled_pixmap)

                        bolo10 = self.m221cliente.leer_bit(100, 1)
                        if not bolo10:
                            pixmap = QPixmap(f":/bolo/fotos/bolo10.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo10.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo10T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo10.setPixmap(scaled_pixmap)
                    
                else:
                 self.ui.pushButtonBolos1.setEnabled(False)
     
                 self.bolo1.setHidden(True) 
                 self.bolo2.setHidden(True) 
                 self.bolo3.setHidden(True)
                 self.bolo4.setHidden(True) 
                 self.bolo5.setHidden(True) 
                 self.bolo6.setHidden(True) 
                 self.bolo7.setHidden(True) 
                 self.bolo8.setHidden(True) 
                 self.bolo9.setHidden(True)
                 self.bolo10.setHidden(True)
              
               # Leo M10 bit 0 para saber si ya se activo la secuencia del juego Pista 1
           
           
            if self.conectadoPista2 :  
                leerM00=self.m221cliente2.leer_bit(10,1)      
                if leerM00==1 : 
                    
                        self.ui.pushButton2Bolos2.setEnabled(True)
                        self.bolo11.setHidden(False) 
                        self.bolo22.setHidden(False) 
                        self.bolo33.setHidden(False)
                        self.bolo44.setHidden(False) 
                        self.bolo55.setHidden(False) 
                        self.bolo66.setHidden(False) 
                        self.bolo77.setHidden(False) 
                        self.bolo88.setHidden(False) 
                        self.bolo99.setHidden(False)
                        self.bolo00.setHidden(False)
                        #LEemos los bolos de la pista 1
                        bolo11 = self.m221cliente2.leer_bit(104, 1)
                        if not bolo11:
                            pixmap = QPixmap(f":/bolo/fotos/bolo1.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo11.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo1T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo11.setPixmap(scaled_pixmap)
                            

                        bolo22 = self.m221cliente2.leer_bit(107, 1)
                        if not bolo22:
                            pixmap = QPixmap(f":/bolo/fotos/bolo2.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo22.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo2T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo22.setPixmap(scaled_pixmap)
                                
                        bolo33 = self.m221cliente2.leer_bit(102, 1)
                        if not bolo33:
                            pixmap = QPixmap(f":/bolo/fotos/bolo3.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo33.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo3T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo33.setPixmap(scaled_pixmap)
                                
                                

                        bolo44 = self.m221cliente2.leer_bit(108, 1)
                        if not bolo44:
                            pixmap = QPixmap(f":/bolo/fotos/bolo4.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo44.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo4T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo44.setPixmap(scaled_pixmap)

                        bolo55 = self.m221cliente2.leer_bit(105, 1)
                        if not bolo55:
                            pixmap = QPixmap(f":/bolo/fotos/bolo5.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo55.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo5T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo55.setPixmap(scaled_pixmap)

                        bolo66 = self.m221cliente2.leer_bit(101, 1)
                        if not bolo66:
                            pixmap = QPixmap(f":/bolo/fotos/bolo6.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo66.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo6T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo66.setPixmap(scaled_pixmap)

                        bolo77 = self.m221cliente2.leer_bit(109, 1)
                        if not  bolo77:
                            pixmap = QPixmap(f":/bolo/fotos/bolo7.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo77.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo7T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo77.setPixmap(scaled_pixmap)

                        bolo8 = self.m221cliente2.leer_bit(106, 1)
                        if not bolo8:
                            pixmap = QPixmap(f":/bolo/fotos/bolo8.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo88.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo8T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo88.setPixmap(scaled_pixmap)

                        bolo99 = self.m221cliente2.leer_bit(103, 1)
                        if not bolo99:
                            pixmap = QPixmap(f":/bolo/fotos/bolo9.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo99.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo9T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo99.setPixmap(scaled_pixmap)

                        bolo00 = self.m221cliente2.leer_bit(100, 1)
                        if not bolo00:
                            pixmap = QPixmap(f":/bolo/fotos/bolo10.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo00.setPixmap(scaled_pixmap)                                          
                        else:                       
                            # Cargar imagen y escalarla
                            pixmap = QPixmap(f":/boloTumbado/fotos/bolo10T.png")
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                            Qt.AspectRatioMode.KeepAspectRatio)
                                self.bolo00.setPixmap(scaled_pixmap)
                    
                else:
                 self.ui.pushButton2Bolos2.setEnabled(False)
                 self.bolo11.setHidden(True) 
                 self.bolo22.setHidden(True) 
                 self.bolo33.setHidden(True)
                 self.bolo44.setHidden(True) 
                 self.bolo55.setHidden(True) 
                 self.bolo66.setHidden(True) 
                 self.bolo77.setHidden(True) 
                 self.bolo88.setHidden(True) 
                 self.bolo99.setHidden(True)
                 self.bolo00.setHidden(True) 
                 
          except Exception as e:
            print(f"Error en la comunicación con el PLC: {e}")
            # Manejo de errores

        
        
        
    def salva(self):
       # Diálogo para seleccionar la ubicación de guardado
         # Nombre fijo para la copia de seguridad
        nombre_backup = "bolera.bd"
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Copia de Seguridad", "bolera.db")
          

        if archivo:
            # Ruta de la base de datos original
            ruta_db_original = "./bolera.db"  # Cambia esto a la ruta de tu base de datos

            try:
                # Copiar el archivo de la base de datos a la ubicación seleccionada
                shutil.copy(ruta_db_original, archivo)
                QMessageBox.information(self, "Éxito", "Copia de seguridad realizada con éxito.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo realizar la copia de seguridad: {e}")

      
          
    def subirBoloPista1(self):
       
           #Activamos en Juego por la pista 1
           print("sdsd")
           #self.m221cliente.escribir_bit_M(14,1, True)
           #self.m221cliente.escribir_bit_M(14,1, False)
        
    def subirBoloPista2(self):
           print("Subimos bolos pista 2222") 
           #Activamos en Juego por la pista 1
          # self.m221cliente2.escribir_bit_M(14,1, True)
          # self.m221cliente2.escribir_bit_M(14,1, False)
        
    def Emergencia(self):
        print("Emergenciaaaaaaaaaaaaaaaaaaaaaaaaaa")    
    def create_bowling_pins(self):
        
         # Lista de QLabel
        self.bolosMostrar = [
            self.bolo1,
            self.bolo2,
            self.bolo3,
            self.bolo4,
            self.bolo5,
            self.bolo6,
            self.bolo7,
            self.bolo8,
            self.bolo9,
            self.bolo10
        ]

        # Crear un QGridLayout
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(QMargins(0,0,0,10))
        grid_layout.setSpacing(10)
       
        # Disposición de los bolos en una matriz de 4 filas y 7 columnas
        pins = [
            (0, 0, "7"),  # Fila 0
            (0, 2, "8"),  # Fila 0
            (0, 4, "9"),  # Fila 0
            (0, 6, "10"),  # Fila 0
            (1, 1, "4"),  # Fila 1
            (1, 3, "5"),  # Fila 1
            (1, 5, "6"),  # Fila 1
            (2, 2, "2"),  # Fila 2
            (2, 4, "3"),  # Fila 2
            (3, 3, "1")   # Fila 3
        ]

        # Agregar los bolos a la rejilla
        for x in range(4):  # 4 filas
            for y in range(7):  # 7 columnas
                # Verificar si hay un bolo en la posición actual
                pin_label = next((pin for pin in pins if pin[0] == x and pin[1] == y), None)
                if pin_label:
                    # Obtener el número del bolo
                    bolo_numero = pin_label[2]
                    # Obtener el QLabel correspondiente
                    label =  self.bolosMostrar[int(bolo_numero) - 1]  # Convertir a índice (0-9)
                   # Cargar imagen y escalarla
                    pixmap = QPixmap(f":/bolo/fotos/bolo{bolo_numero}.png")
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                     Qt.AspectRatioMode.KeepAspectRatio)
                        label.setPixmap(scaled_pixmap)
                        label.setMinimumSize(scaled_pixmap.size())
                        # Opción 1: ajustar el size policy a preferred para el tamaño vertical
                        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
                         # Aplicar margen inferior individual a algunos bolos (Ejemplo)
                        
                    else:
                        label.setText(f"Image {bolo_numero} not found.")


                    
                    grid_layout.addWidget(label, x, y) 
        #self.ui.bolos.setStyleSheet("border: 2px solid red;")  # Cambia el color y el grosor según tus necesidades
         # Establecer el espaciado específico entre las filas 0 y 1
    
         # Establecer el layout en el QFrame o QWidget correspondiente
        self.ui.bolos1.setLayout(grid_layout) 
       
        self.ui.bolos1.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)

        

    
    
    
   
    def create_bowling_pins1(self):
     

        # Crear un QGridLayout
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(QMargins(0,0,0,10))
        grid_layout.setSpacing(10)
       
        # Disposición de los bolos en una matriz de 4 filas y 7 columnas
        pins = [
            (0, 0, "7"),  # Fila 0
            (0, 2, "8"),  # Fila 0
            (0, 4, "9"),  # Fila 0
            (0, 6, "10"),  # Fila 0
            (1, 1, "4"),  # Fila 1
            (1, 3, "5"),  # Fila 1
            (1, 5, "6"),  # Fila 1
            (2, 2, "2"),  # Fila 2
            (2, 4, "3"),  # Fila 2
            (3, 3, "1")   # Fila 3
        ]

        # Agregar los bolos a la rejilla
        for x in range(4):  # 4 filas
            for y in range(7):  # 7 columnas
                # Verificar si hay un bolo en la posición actual
                pin_label = next((pin for pin in pins if pin[0] == x and pin[1] == y), None)
                if pin_label:
                    # Obtener el número del bolo
                    bolo_numero = pin_label[2]
                    # Obtener el QLabel correspondiente
                    label =  self.bolosMostrar1[int(bolo_numero) - 1]  # Convertir a índice (0-9)
                   # Cargar imagen y escalarla
                    pixmap = QPixmap(f":/bolo/fotos/bolo{bolo_numero}.png")
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(QSize(40, 60),
                                                     Qt.AspectRatioMode.KeepAspectRatio)
                        label.setPixmap(scaled_pixmap)
                        label.setMinimumSize(scaled_pixmap.size())
                        # Opción 1: ajustar el size policy a preferred para el tamaño vertical
                        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
                         # Aplicar margen inferior individual a algunos bolos (Ejemplo)
                        
                    else:
                        label.setText(f"Image {bolo_numero} not found.")


                    
                    grid_layout.addWidget(label, x, y) 
        #self.ui.bolos.setStyleSheet("border: 2px solid red;")  # Cambia el color y el grosor según tus necesidades
         # Establecer el espaciado específico entre las filas 0 y 1
    
         # Establecer el layout en el QFrame o QWidget correspondiente
         
        self.ui.bolos2.setLayout(grid_layout)  
        self.ui.bolos2.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)      
    def abrirReportes(self):
        
         resportesUser= ResumenJuegosUser(self, self.Sesion,self.UserLogueado.usuario)
         resportesUser.exec()
       
    def abrirTV1(self):
         # Obtener información sobre las pantallas
        screen_count = QApplication.screens()
        
       
        
        if self.sub_window11 is None or not self.sub_window11.isVisible():
                     
         # Comprobar que hay suficientes pantallas conectadas.
            if len(screen_count) < 2:
                # Crear un mensaje de diálogo
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Información")
                msg_box.setText("Revise la salida de video del Televisor 1.")
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.exec()
                return
            self.ui.btn_tv1.setText("Cerrar TV 1")
            self.sub_window11=AnimacionTV1()
            self.Dasboard.sub_window=self.sub_window11
                
            # Obtener la segunda pantalla
            segunda_pantalla = screen_count[1]
            # self.sub_window11=CarruselFotos()
            # Calcular la posición de la segunda pantalla
            screen_geometry = segunda_pantalla.geometry()
            self.sub_window11.setGeometry(screen_geometry.x() + 100, screen_geometry.y() + 100, 300, 100)
            # Mostrar el diálogo
            self.sub_window11.showFullScreen()
           
        
           
        else:
            # Si la sub-ventana es visible, la cerramos
            self.sub_window11.close()
            self.sub_window11= None  # Restablecemos a None
            self.ui.btn_tv1.setText("Abrir TV 1")
            self.Dasboard.sub_window=None

       
    def abrirTV2(self):
        # Obtener información sobre las pantallas
        screen_count = QApplication.screens()
       
        
        if self.sub_window22 is None or not self.sub_window22.isVisible():
                     
         # Comprobar que hay suficientes pantallas conectadas.
            if len(screen_count) < 3:
                # Crear un mensaje de diálogo
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Información")
                msg_box.setText("Revise la salida de video del Televisor 2.")
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.exec()
                return
            self.ui.btn_tv2.setText("Cerrar TV 2")
            
                
            # Obtener la segunda pantalla
            segunda_pantalla = screen_count[2]
            
            self.sub_window22=AnimacionTV2()
            self.Dasboard.sub_window1=self.sub_window22
            # Calcular la posición de la segunda pantalla
            screen_geometry = segunda_pantalla.geometry()
            self.sub_window22.setGeometry(screen_geometry.x() + 100, screen_geometry.y() + 100, 300, 100)
            # Mostrar el diálogo
            self.sub_window22.showFullScreen()
        
           
        else:
            # Si la sub-ventana es visible, la cerramos
            self.sub_window22.close()
            self.sub_window22= None  # Restablecemos a None
            self.Dasboard.sub_window1=None
            self.ui.btn_tv2.setText("Abrir TV 2")
       
    def mostrar_tiempo(self):
        # Obtener la fecha y hora actual
        ahora = QDateTime.currentDateTime()
        formato_fecha = 'dd/MM/yyyy'  # Formato de fecha
        formato_hora = 'hh:mm:ss'  # Formato de hora
        
        self.ui.fecha.setText('' + ahora.toString(formato_fecha))
        self.ui.hora.setText('' + ahora.toString(formato_hora))  
                
    def abrirPista1(self):
        
        texto_label=self.ui.label_7.text()
       # print("Texto del Label "+texto_label)
     
        if( texto_label=="Ocupado"): 
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Confirmación")         
            msgBox.setText(f"¿Desea cerrar el juego de la Pista 1?")
            msgBox.setIcon(QMessageBox.Icon.Question)
            msgBox.setStandardButtons( QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)          
                    # Obtén el botón "Yes"
            boton_si = msgBox.button(QMessageBox.StandardButton.Yes)
            # Cambia el texto del botón a "Sí"
            boton_si.setText("Sí")       
            # Muestra el mensaje y obtiene la respuesta
            respuesta = msgBox.exec()
        
            # Si el usuario confirma (clickea en 'Yes')
            if respuesta == QMessageBox.StandardButton.Yes:
                 #Desactivamos el juego para que no se quede activo
                self.juegoBD_operaciones.desactivarJuegoForzado1(self.id_juego_1)
                self.modificar_Pista1_Boton()
                self.ventana_ResultadosPista1.close()
                self.ventana_ResultadosPista1 = None  
                # activamos la comunicacion con el aUTOMATA Y CERRAMOS LA PISTA
               
                #ip_address = "localhost"  # Reemplaza con la IP de tu PLC
                #self.m221cliente = M221_Bolera.M221(self.ip_address1)
                try:       
                    #self.m221cliente.connectar()
                    
                    #Desactivamos Activamos en Juego por la pista 1
                    self.m221cliente.escribir_bit_M(10,1, False)
                    self.ui.pushButtonBolos1.setEnabled(False)
       
                except Exception as e:
                 print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
                 
            
            
        else:
            self.pista1=AdminPistas(self,self.UserLogueado, self.Dasboard,self.Sesion)
            self.pista1.enviar_datos1.connect(self.recibir_datos_Pista1)
            self.pista1.exec()
     
     
    
     
    def abrirPista2(self):
    
        texto_label=self.ui.label_6.text()
       # print("Texto del Label "+texto_label)
     
        if( texto_label=="Ocupado"): 
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Confirmación")         
            msgBox.setText(f"¿Desea cerrar el juego de la Pista 2?")
            msgBox.setIcon(QMessageBox.Icon.Question)
            msgBox.setStandardButtons( QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)          
                    # Obtén el botón "Yes"
            boton_si = msgBox.button(QMessageBox.StandardButton.Yes)
            # Cambia el texto del botón a "Sí"
            boton_si.setText("Sí")       
            # Muestra el mensaje y obtiene la respuesta
            respuesta = msgBox.exec()
        
            # Si el usuario confirma (clickea en 'Yes')
            if respuesta == QMessageBox.StandardButton.Yes:
                 #Desactivamos el juego para que no se quede activo
                self.juegoBD_operaciones.desactivarJuegoForzado1(self.id_juego_2)
                self.modificar_Pista2_Boton()
                self.ventana_ResultadosPista2.close()
                self.ventana_ResultadosPista2 = None 
                
                
                self.id_juego_2=0
                try:       
                    
                    
                    #Desactivamos en Juego por la pista 2
                    self.m221cliente2.escribir_bit_M(10,1, False)  
                    # Desactivamos el motor de los bolos automata 1 
                    self.m221cliente.escribir_bit_M(12,1,False)

                    self.ui.pushButton2Bolos2.setEnabled(False)

                except Exception as e:
                 print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
            
        else:
            self.pista2=AdminPistas2(self,self.UserLogueado, self.Dasboard,self.Sesion)
            self.pista2.enviar_datos1.connect(self.recibir_datos_Pista2)
            self.pista2.exec()
     
    def modificar_Pista1_Boton(self):
        self.ui.btn_pista1.setText("Jugar")
        self.ui.btn_pista1.setStyleSheet("background-color: rgb(7, 125, 195); color:rgba(255, 255, 255, 210);	border-radius:5px;")
        self.ui.label_7.setText("Libre")  
        self.ui.label_7.setStyleSheet("color: rgb(0, 176, 0);")
        
    def modificar_Pista2_Boton(self):
        self.ui.btn_pista2.setText("Jugar")
        self.ui.btn_pista2.setStyleSheet("background-color: rgb(7, 125, 195); color:rgba(255, 255, 255, 210);	border-radius:5px;")
        self.ui.label_6.setText("Libre")  
        self.ui.label_6.setStyleSheet("color: rgb(0, 176, 0);")
   
    def recibir_datos_Pista1(self, id_juego, dato2):
        self.id_juego_1=id_juego
        #self.label_resultado.setText(f"Datos recibidos: {id_juego}, {dato2}")
        self.ui.btn_pista1.setText("Cerrar Pista")
        self.ui.btn_pista1.setStyleSheet("background-color: #FF7F7F;color:rgba(255, 255, 255, 210); border-radius:5px;")
        
        self.ui.label_7.setText("Ocupado")  
        self.ui.label_7.setStyleSheet("color: rgb(255, 0, 0);")
        
        
    def recibir_datos_Pista2(self, id_juego, dato2):
        self.id_juego_2=id_juego
        #self.label_resultado.setText(f"Datos recibidos: {id_juego}, {dato2}")
        self.ui.btn_pista2.setText("Cerrar Pista")
        self.ui.btn_pista2.setStyleSheet("background-color: #FF7F7F;color:rgba(255, 255, 255, 210); border-radius:5px;")
        
        self.ui.label_6.setText("Ocupado")  
        self.ui.label_6.setStyleSheet("color: rgb(255, 0, 0);") 
        