import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,QFileDialog, QMessageBox,QGridLayout,QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QLabel,QHeaderView,QSizePolicy,QTableWidget,QAbstractItemView


from PyQt6.QtCore import Qt,QTimer, QTime,QMargins, QSize
from PyQt6.QtGui import QColor,QBrush, QPixmap

from PyQt6.QtGui import QFont
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
from bd_modelos.juego_bolos import JuegoBolos
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
        
        #self.ui.bolos2.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
      #  self.ui.bolos1.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        
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
        #self.ip_address = "localhost"  # Reemplaza con la IP de tu PLC   
        #self.ip_address1 = "192.168.0.1"  # Reemplaza con la IP de tu PLC
        self.ip_address1 = "localhost"  # Reemplaza con la IP de tu PLC 
        self.conectadoPista1=False
        self.conectadoPista2=False
        
        self.m221cliente2 = M221_Bolera.M221(self.ip_address)          
        self.m221cliente = M221_Bolera.M221(self.ip_address1)
        
        # Operaicones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones() 
        
        self.jugadoresJuego1=None #self.juegoBD_operaciones.obtenerDeJuegoJugadores(self.id_juego) 
         
        

        # Configuracion del juego 1
        # Inicializamos la bandera como un atributo de la clase
        self.bandera_ejecutado1 = False
        # Jugador Activo
        self.jugadorActivo=1
        # Valor de Ronda activa
        self.rondaActiva=1
        # Tiro activo
        self.tiroActivo=1
        
         #obtengo los datos del Juego 1 de la BD . eso lo hacemos cdo se cree el juego
        self.jugadores1= None  #self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego)
         # Inicializar el juego de bolos 1 para poder Calcular puntucion
        self.juego1 = None #JuegoBolos(self.jugadores)
        self.resultados1=[]
        
        
        # Configuracion del juego 2
        # Inicializamos la bandera como un atributo de la clase
        self.bandera_ejecutado2 = False
        # Jugador Activo
        self.jugadorActivo2=1
        # Valor de Ronda activa
        self.rondaActiva2=1
        # Tiro activo
        self.tiroActivo2=1
        
        #obtengo los datos del Juego 2 de la BD . eso lo hacemos cdo se cree el juego
        self.jugadoresJuego2= None  #self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego)
           # Inicializar el juego de bolos 2 para poder Calcular puntucion
        self.juego2 = None #JuegoBolos(self.jugadores)
        self.resultados2=[]
        
        
        #Tablas de los resultados Falta Buscar los noimbres 
        self.table1=self.ui.tablaPista1
        self.table2=self.ui.tablaPista2
        
        
        
      
        #self.conectadoPista2=self.m221cliente2.connectar()  
        self.conectadoPista1=self.m221cliente.connectar()
        
        
        
        
        
          
              
         # Conectar a la base de datos  
        self.con = Conexion()  
        self.UserLogueado = user
        self.Sesion= sesion
        
        self.id_juego_1= 0 #89
        self.id_juego_2=0
         # Temporizador para actualizar cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_tiempo)
        self.timer.start(1000)  # 1000 ms = 1 segundo
        
        self.sub_window11 = None  # Inicializamos la sub-ventana del TV 1 como None
        self.sub_window22 = None  # Inicializamos la sub-ventana del TV 2 como None 
        
        # Mostrar el tiempo al iniciar
        self.mostrar_tiempo()
       
      
        self.initGUI() 
       # self.create_bowling_pins()
        #self.create_bowling_pins1()
        self.timer = QTimer()
        self.timer.timeout.connect(self.comunicacion_plc)
        self.timer.start(500)  # Ejecuta `comunicacion_plc` cada 1000 milisegundos (1 segundo)
                    
    def initGUI(self):
       self.ui.btn_pista1.clicked.connect(self.abrirPista1)
       self.ui.btn_pista2.clicked.connect(self.abrirPista2)
       self.ui.btn_tv1.clicked.connect(self.abrirTV1)
       self.ui.btn_tv2.clicked.connect(self.abrirTV2)
       self.ui.pushButton_8.clicked.connect(self.abrirReportes)
       
       #self.ui.pushButtonBolos1.clicked.connect(self.subirBoloPista1)
       #self.ui.pushButton2Bolos2.clicked.connect(self.subirBoloPista2)
       self.ui.salva.clicked.connect(self.salva)
    
      # boton de menrgencia
       self.ui.pushButton_3.clicked.connect(self.Emergencia)
       self.configurar_tabla1()
       self.configurar_tabla2()
       
       #self.ui.pushButtonBolos1.setEnabled(False)
       #self.ui.pushButton2Bolos2.setEnabled(False)
       
       
     
      # Motor de la Bola
    def comunicacion_plc(self):
        
          try:
              
            if self.conectadoPista1 and self.id_juego_1!=0:        
                #Leo M10 bit 0 para saber si ya se activo la secuencia del juego Pista 1
                leerM0=self.m221cliente.leer_bit(10,1)
                print(f"Pista Activaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {leerM0}")
                #si esta en 1  esta activado el juego Pista 1 y comenzamos a Jugar
                if leerM0==1 : 
                    
                 #Leer jugador activo %MW24
                 self.jugadorActivo1=self.m221cliente.leer_MW(24)              
                 #Leer ronda activa  %MW26
                 self.rondaActiva1=self.m221cliente.leer_MW(26)
                 #Leer Tiro Activo             
                 self.tiroActivo1=self.m221cliente.leer_MW(30)
                 # Leemos si el Jugador ya tiro
                 # Leo M7 bit 0 para saber si se produjo el tiro y podemos leer
                 leerM7=self.m221cliente.leer_bit(7,1)
                 if not leerM7 and self.bandera_ejecutado1:                   
                    self.bandera_ejecutado1 = False # Reseteamos la bandera a False para la proxima ejecución
                    print("Bandera reseteada a false")                 
                 if leerM7 and not self.bandera_ejecutado1:                    
                    print("************* Leer **************")
                    self.bandera_ejecutado1 = True
                    #obtengo los datos de la BD
                    self.jugadoresJuego1=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego_1)
                      # Inicializar el juego de bolos
                    self.juego1 = JuegoBolos(self.jugadoresJuego1)
                    self.resultados1 = self.juego1.calcular_puntuacion()  
                      #print(self.resultados)
                    self.configurar_tabla1()
                    self.llenar_tabla1(self.jugadorActivo1,self.rondaActiva1) 
                    
                    
                else:
                    # self.ui.pushButtonBolos1.setEnabled(False)
                     print(f"HAcer algooo {leerM0}")
     
                
              
               # Leo M10 bit 0 para saber si ya se activo la secuencia del juego Pista 1
           
           
            if self.conectadoPista1 and self.id_juego_2!=0:  
                leerM00=self.m221cliente.leer_bit(210,1)      
                if leerM00==1 : 
                    
                    print(f"Pista 2 Activaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {leerM0}")
                         #Leo M10 bit 0 para saber si ya se activo la secuencia del juego Pista 1
                    leerM0=self.m221cliente.leer_bit(210,1)
                
                    #si esta en 1  esta activado el juego Pista 1 y comenzamos a Jugar
                    if leerM0==1 : 
                        
                        #Leer jugador activo %MW24
                        self.jugadorActivo2=self.m221cliente.leer_MW(224)              
                        #Leer ronda activa  %MW26
                        self.rondaActiva2=self.m221cliente.leer_MW(226)
                        #Leer Tiro Activo             
                        self.tiroActivo2=self.m221cliente.leer_MW(230)
                        # Leemos si el Jugador ya tiro
                        # Leo M207 bit 0 para saber si se produjo el tiro y podemos leer
                        leerM7=self.m221cliente.leer_bit(207,1)
                        if not leerM7 and self.bandera_ejecutado2:                   
                            self.bandera_ejecutado2 = False # Reseteamos la bandera a False para la proxima ejecución
                            print("Bandera reseteada a false")                 
                        if leerM7 and not self.bandera_ejecutado2:                    
                            print("************* Leer **************")
                            self.bandera_ejecutado2 = True
                            #obtengo los datos de la BD
                            self.jugadoresJuego2=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego_2)
                            # Inicializar el juego de bolos
                            self.juego2= JuegoBolos(self.jugadoresJuego2)
                            self.resultados2 = self.juego2.calcular_puntuacion()  
                            #print(self.resultados)
                            self.configurar_tabla2()
                            self.llenar_tabla2(self.jugadorActivo2,self.rondaActiva2) 
                    
                else:
                    
                 print(f"Pista Activaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {leerM0}")
                 
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
        
             
     
       
        if(self.conectadoPista1)    :
            
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
                         # Desactivamos el motor de los bolos automata 1 
                        self.m221cliente.escribir_bit_M(12,1,False)
                        #self.ui.pushButtonBolos1.setEnabled(False)
                       
        
                    except Exception as e:
                     print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
                    
                
                
            else:
                self.pista1=AdminPistas(self,self.UserLogueado, self.Dasboard,self.Sesion)
                self.pista1.enviar_datos1.connect(self.recibir_datos_Pista1)
                self.pista1.exec()
            
            
          
        else:
            print(f"Programa Aqui algun mensaje de error de Comunicacion ")
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Información")         
            msgBox.setText(f"No hay comunicación con Pista 1. Por favor revisar o llamar Asistencia Técnica")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
        
        
        
        
        
       
     
     
    
     
    def abrirPista2(self):
     
      if(self.conectadoPista1)    :  
       
    
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
                    self.m221cliente.escribir_bit_M(210,1, False)  
                    # Desactivamos el motor de los bolos automata 1 
                    self.m221cliente.escribir_bit_M(12,1,False)

                   # self.ui.pushButton2Bolos2.setEnabled(False)

                except Exception as e:
                 print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
            
        else:
            self.pista2=AdminPistas2(self,self.UserLogueado, self.Dasboard,self.Sesion)
            self.pista2.enviar_datos1.connect(self.recibir_datos_Pista2)
            self.pista2.exec()
      else:
            print(f"Programa Aqui algun mensaje de error de Comunicacion ")
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Información")         
            msgBox.setText(f"No hay comunicación con Pista 2. Por favor revisar o llamar Asistencia Técnica")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()          
     
    def modificar_Pista1_Boton(self):
        self.id_juego_1=0
        # cerramos laself.m221cliente.desconectar() comunicacion con el automata 
        
        self.resultados1=[]
        self.configurar_tabla1()
        
        
        
        self.ui.btn_pista1.setText("Jugar")
        self.ui.btn_pista1.setStyleSheet("background-color: rgb(7, 125, 195); color:rgba(255, 255, 255, 210);	border-radius:5px;")
        self.ui.label_7.setText("Libre")  
        self.ui.label_7.setStyleSheet("color: rgb(0, 176, 0);")
        
    def modificar_Pista2_Boton(self):
        self.id_juego_2=0
        # cerramos la comunicacion con el automata 
        self.resultados2=[]
        self.configurar_tabla2()
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
        # Ahora nos conectamos al automata 
          #Conectar con los dos Automatas...
        try:       
     
           # self.conectadoPista1=self.m221cliente.connectar()
             # Ahora pedimos todos los datos de la pista 1 porque el juego se activo 
            self.jugadoresJuego1=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(id_juego) 
            self.juego1= JuegoBolos(self.jugadoresJuego1)
            self.resultados1 = self.juego1.calcular_puntuacion()
        # print(self.resultados)     
            self.configurar_tabla1()
            self.llenar_tabla1(self.jugadorActivo,self.rondaActiva)
        
          
        except Exception as e:
          print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
        
         
        
    def recibir_datos_Pista2(self, id_juego, dato2):
        self.id_juego_2=id_juego
        #self.label_resultado.setText(f"Datos recibidos: {id_juego}, {dato2}")
        self.ui.btn_pista2.setText("Cerrar Pista")
        self.ui.btn_pista2.setStyleSheet("background-color: #FF7F7F;color:rgba(255, 255, 255, 210); border-radius:5px;")
        
        self.ui.label_6.setText("Ocupado")  
        self.ui.label_6.setStyleSheet("color: rgb(255, 0, 0);") 
          # Ahora nos conectamos al automata 
          #Conectar con los dos Automatas...
        try:       
     
        
            # Ahora piodimos todos los datos de la pista 1 porque el juego se activo 
            self.jugadoresJuego2=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(id_juego) 
            self.juego2 = JuegoBolos(self.jugadoresJuego2)
            self.resultados2 = self.juego2.calcular_puntuacion()
        # print(self.resultados)     
            self.configurar_tabla2()
            self.llenar_tabla2(self.jugadorActivo,self.rondaActiva)
          
        except Exception as e:
          print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
        
        
        
        
    def pista1Cerrada(self):
        self.id_juego_1=0
    def pista2Cerrada(self):
        self.id_juego_2=0    
           
    def configurar_tabla1(self):
        columnas = ['Jug.']
        columnas.extend([f'{i+1}' for i in range(10)])
        columnas.append("Total") #Agregamos la columna de puntuacion total
        self.table1.setColumnCount(len(columnas))
        self.table1.setHorizontalHeaderLabels(columnas)
        self.table1.setRowCount(len(self.resultados1))
        if len(self.resultados1)<=  2 and len(self.resultados1)!= 0:
           for _ in range(2):  # Agregar 2 filas
            row_position = self.table1.rowCount()
            self.table1.insertRow(row_position)

        #Aplicar estilos en los encabezados de la fila 
         # Personalización de cada encabezado de columna
        font = QFont("Arial", 11, QFont.Weight.Bold) #Fuente Arial, tamaño 12, negritacd.

        for i in range(len(columnas)):
            if i==0:
                item = QTableWidgetItem(columnas[i])
                font1 = QFont("Arial", 11, QFont.Weight.Bold) #Fuente Arial, tamaño 12, negritacd.
                item.setFont(font1) #Aplicando la fuente personalizada
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión
                item.setForeground(QColor(255, 255, 255)) 
                self.table1.setHorizontalHeaderItem(i, item)

            else:    

                item = QTableWidgetItem(columnas[i])
                item.setFont(font) #Aplicando la fuente personalizada
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión
                item.setForeground(QColor(255, 255, 255)) 
                self.table1.setHorizontalHeaderItem(i, item)


        self.table1.setColumnWidth(0, 400) #  Ajusta el valor 150 a tu gusto.
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Ocultar el encabezado vertical (numeración de filas)
        self.table1.verticalHeader().setHidden(True)  # Cambia esto para ocultar el encabezado vertical
           
        self.table1.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
         # Ajustar el estilo del encabezado
        self.table1.horizontalHeader().setStyleSheet("QHeaderView::section { height: 30px;  background-color: #00007f; }")  # Aumentar la altura del encabezado
         # Quitar las líneas verticales
        self.table1.setStyleSheet("QTableWidget { border: none; }")  # Sin bordes en la tabla
       # self.table.setShowGrid(False)  # Quitar la cuadrícula
        self.table1.verticalHeader().setDefaultSectionSize(110)
         #Este es el truco para distribuir uniformemente las filas
        self.table1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  
          # Desactivar la selección
        
        self.table1.setSelectionMode(QTableWidget.SelectionMode.NoSelection)   
        
        
    def configurar_tabla2(self):
        columnas = ['Jug.']
        columnas.extend([f'{i+1}' for i in range(10)])
        columnas.append("Total") #Agregamos la columna de puntuacion total
        self.table2.setColumnCount(len(columnas))
        self.table2.setHorizontalHeaderLabels(columnas)
        self.table2.setRowCount(len(self.resultados2))
        if len(self.resultados2)<=  2 and len(self.resultados2)!= 0:
           for _ in range(2):  # Agregar 2 filas
            row_position = self.table2.rowCount()
            self.table2.insertRow(row_position)

        #Aplicar estilos en los encabezados de la fila 
         # Personalización de cada encabezado de columna
        font = QFont("Arial", 11, QFont.Weight.Bold) #Fuente Arial, tamaño 12, negritacd.

        for i in range(len(columnas)):
            if i==0:
                item = QTableWidgetItem(columnas[i])
                font1 = QFont("Arial", 11, QFont.Weight.Bold) #Fuente Arial, tamaño 12, negritacd.
                item.setFont(font1) #Aplicando la fuente personalizada
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión
                item.setForeground(QColor(255, 255, 255)) 
                self.table2.setHorizontalHeaderItem(i, item)

            else:    

                item = QTableWidgetItem(columnas[i])
                item.setFont(font) #Aplicando la fuente personalizada
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión
                item.setForeground(QColor(255, 255, 255)) 
                self.table2.setHorizontalHeaderItem(i, item)


        self.table2.setColumnWidth(0, 400) #  Ajusta el valor 150 a tu gusto.
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Ocultar el encabezado vertical (numeración de filas)
        self.table2.verticalHeader().setHidden(True)  # Cambia esto para ocultar el encabezado vertical
           
        self.table2.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
         # Ajustar el estilo del encabezado
        self.table2.horizontalHeader().setStyleSheet("QHeaderView::section { height: 30px;  background-color: #00007f; }")  # Aumentar la altura del encabezado
         # Quitar las líneas verticales
        self.table2.setStyleSheet("QTableWidget { border: none; }")  # Sin bordes en la tabla
       # self.table.setShowGrid(False)  # Quitar la cuadrícula
        self.table2.verticalHeader().setDefaultSectionSize(110)
         #Este es el truco para distribuir uniformemente las filas
        self.table2.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  
          # Desactivar la selección
        
        self.table2.setSelectionMode(QTableWidget.SelectionMode.NoSelection) 
        
        
    def llenar_tabla1(self,jugadorActivo,rondaActiva):
        #enumerate(self.resultados)
        
        for fila, resultado in enumerate(self.resultados1):
           
                nombre_item = QTableWidgetItem(resultado['nombre'])
                nombre_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                nombre_item.setBackground(QColor(0, 85, 255)) #Color en RGB para mas precisión 
                nombre_item.setForeground(QColor("white")) # Cambiando el color del texto a blanco          
                fontNombre = QFont()
                fontNombre.setPointSize(12)  # Tamaño de letra
                fontNombre.setBold(True) #opcional si quieres negrita           
                nombre_item.setFont(fontNombre)
                self.table1.setItem(fila, 0, nombre_item)            
                puntuacion_acumulada = 0



                for columna, puntuacion_ronda in enumerate(resultado['rondas']):
                    if columna<rondaActiva and fila<= len(self.resultados1):
                        op1 = resultado['tiros'][columna]['op1']
                        op2 = resultado['tiros'][columna]['op2']
                        op3 = 0
                        puntuacion_acumulada += puntuacion_ronda
                        if columna < 9:
                            texto = f"{op1}-{op2}={puntuacion_acumulada}"
                        else:
                            op3 = resultado['tiros'][columna]['op3']
                            texto = f"{op1}-{op2}-{op3}={puntuacion_acumulada}"
                        
                        # solo se muestra cdo no hay informacion
                        # Crear un widget para la celda
                        cell_widget = QWidget()        
                    
                        # Crear el layout vertical
                        main_layout = QVBoxLayout()
                        main_layout.setContentsMargins(0, 0, 0, 0)  # (izquierda, arriba, derecha, abajo)
                        main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear un layout horizontal para los dos labels de arriba
                        top_layout = QHBoxLayout()
                        top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
                        top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear los dos labels de arriba
                        label1 = QLabel()
                        label2 = QLabel()
                        tiro10_label3 = QLabel()
                    
                        
                        if columna==9 :
                            #Si todos los tiros fueron 10 escribir X rgb(0, 0, 168) rgb(0, 0, 168)
                            if op1==10 and op2==10 and op3==10:
                                label1.setText("X")
                                label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF; font-size: 20px; ")    # Color de fondo para visualizar mejor                       
                                label2.setText("X")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                tiro10_label3.setText("X")
                                tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                tiro10_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            else:
                            #si el primero es 10 ya tiene derecho a otro tiro adicional
                             if op1<10:
                               
                               
                                  if op1!=0:  
                                      label1.setText(f"{op1}")
                                      label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor                       
                                  else:
                                      label1.setText("0")
                                      label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor    

                             else:
                                label1.setText("X")
                                label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF; font-size: 20px; ")    # Color de fondo para visualizar mejor
                            
                            # if  self.tiroActivo==2 and self.bolosTiro1<10 and self.bolosTiro1+self.bolosTiro2==10:

                             if op2<10:
                                if op1+op2==10 and op1<10 :
                                    label2.setText("/")
                                    label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor                       
                                else:
                                  if op2!=0:
                                      label2.setText(f"{op2}")
                                      label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                  else:
                                      label2.setText("0")
                                      label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                             else:
                                    label2.setText("X")
                                    label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor  
                            
                            
                            
                            
                            
                            
                             if op3<10: 
                                if op3!=0:
                                    tiro10_label3.setText(f"{op3}")
                                    tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                else:
                                    tiro10_label3.setText("0")
                                    tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                            
                             else:
                                tiro10_label3.setText("X")
                                tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor 
                    
                        else:
                          if op1 == 10:
                                label1.setText("")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText("X")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          elif op1 == 0 and op2 == 10:
                                label1.setText("0")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText("/")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          elif op1 == 0 and op2 == 0:
                                label1.setText("0")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px;")  
                                label2.setText("0")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          elif op1 + op2 == 10:
                                label1.setText(f"{op1}")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText("/")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          else:
                                label1.setText(f"{op1}")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText(f"{op2}")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")

                        #label2.setStyleSheet("background-color: lightgray;")  # Color de fondo para visualizar mejor
                        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

                        # Añadir un poco de espacio entre los labels
                        top_layout.addWidget(label1)
                        top_layout.addSpacing(0)  # Espacio de 20 píxeles
                        top_layout.addWidget(label2)                  

                        if columna >= 9:
                            top_layout.addSpacing(0)  # Espacio de 20 píxeles
                            top_layout.addWidget(tiro10_label3)
                        
                            # Añadir el layout horizontal al layout principal
                        main_layout.addLayout(top_layout)
                            # Crear el label de abajo que ocupa el espacio de los dos de arriba
                        label3 = QLabel(f"{puntuacion_acumulada}")
                        label3.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 22px;")  # Color de fondo para visualizar mejor
                        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)                
                        main_layout.addWidget(label3)
                            # Establecer el layout en el widget de la celda
                        cell_widget.setLayout(main_layout)                        
                            # Añadir el widget a la celda de la tabla
                        self.table1.setCellWidget(fila, columna + 1, cell_widget)               
                    
                    else:
                        # Crear un widget para la celda
                        cell_widget = QWidget()                    
                        # Crear el layout vertical
                        main_layout = QVBoxLayout()
                        main_layout.setContentsMargins(0, 0, 0, 0)  # (izquierda, arriba, derecha, abajo)
                        main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear un layout horizontal para los dos labels de arriba
                        top_layout = QHBoxLayout()
                        top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
                        top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear los dos labels de arriba
                        label1 = QLabel()
                        label2 = QLabel()
                        tiro10_label3 = QLabel() #0055ff
                        label1.setText("")
                        label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px")    # Color de fondo para visualizar mejor
                        label2.setText("")
                        label2.setStyleSheet(" background-color: #0055ff; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visua
                        
                        tiro10_label3.setText("")
                        tiro10_label3.setStyleSheet(" background-color: #0055ff; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visua
                        # Añadir un poco de espacio entre los labels
                        top_layout.addWidget(label1)
                        top_layout.addSpacing(0)  # Espacio de 20 píxeles
                        top_layout.addWidget(label2)   
                        if columna >= 9:
                            top_layout.addSpacing(0)  # Espacio de 20 píxeles
                            top_layout.addWidget(tiro10_label3)
                        
                            # Añadir el layout horizontal al layout principal
                        main_layout.addLayout(top_layout)
                            # Crear el label de abajo que ocupa el espacio de los dos de arriba
                        label3 = QLabel("")
                        label3.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 22px;")  # Color de fondo para visualizar mejor
                        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)                
                        main_layout.addWidget(label3)
                            # Establecer el layout en el widget de la celda
                        cell_widget.setLayout(main_layout)
                        # Añadir el widget a la celda de la tabla
                        self.table1.setCellWidget(fila, columna + 1, cell_widget)
                        
                        
                        
                        
                #if fila==jugadorActivo :
                  #  self.ui.label_puntaje.setText(f"{puntuacion_acumulada}")
                # Agregar colunma 11 la puntuación total a la última columna
                total_item = QTableWidgetItem(str(puntuacion_acumulada))
                total_item.setBackground(QColor(0, 85, 255)) #Color en RGB para mas precisión           
                total_item.setForeground(QColor("white")) # Cambiando el color del texto a blanco
                #total_item = QTableWidgetItem(str(300))
                # Crear un objeto QFont para definir el estilo de la fuente
                font = QFont()
                font.setPointSize(22)  # Tamaño de letra
                font.setBold(True) #opcional si quieres negrita
                # Aplicar el estilo de fuente al QTableWidgetItem
                total_item.setFont(font)
                # Centrar el texto horizontal y verticalmente
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

                self.table1.setItem(fila, 11, total_item) # 11 porque tenemos 10 rondas + nombre
                i=0
            
       
        self.aplicar_bordes_rojos( jugadorActivo)
            
    
    def llenar_tabla2(self,jugadorActivo,rondaActiva):
        #enumerate(self.resultados)
      for fila, resultado in enumerate(self.resultados2):
           
                nombre_item = QTableWidgetItem(resultado['nombre'])
                nombre_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                nombre_item.setBackground(QColor(0, 85, 255)) #Color en RGB para mas precisión 
                nombre_item.setForeground(QColor("white")) # Cambiando el color del texto a blanco          
                fontNombre = QFont()
                fontNombre.setPointSize(12)  # Tamaño de letra
                fontNombre.setBold(True) #opcional si quieres negrita           
                nombre_item.setFont(fontNombre)
                self.table2.setItem(fila, 0, nombre_item)            
                puntuacion_acumulada = 0



                for columna, puntuacion_ronda in enumerate(resultado['rondas']):
                    if columna<rondaActiva and fila<= len(self.resultados2):
                        op1 = resultado['tiros'][columna]['op1']
                        op2 = resultado['tiros'][columna]['op2']
                        op3 = 0
                        puntuacion_acumulada += puntuacion_ronda
                        if columna < 9:
                            texto = f"{op1}-{op2}={puntuacion_acumulada}"
                        else:
                            op3 = resultado['tiros'][columna]['op3']
                            texto = f"{op1}-{op2}-{op3}={puntuacion_acumulada}"
                        
                        # solo se muestra cdo no hay informacion
                        # Crear un widget para la celda
                        cell_widget = QWidget()        
                    
                        # Crear el layout vertical
                        main_layout = QVBoxLayout()
                        main_layout.setContentsMargins(0, 0, 0, 0)  # (izquierda, arriba, derecha, abajo)
                        main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear un layout horizontal para los dos labels de arriba
                        top_layout = QHBoxLayout()
                        top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
                        top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear los dos labels de arriba
                        label1 = QLabel()
                        label2 = QLabel()
                        tiro10_label3 = QLabel()
                    
                        
                        if columna==9 :
                            #Si todos los tiros fueron 10 escribir X rgb(0, 0, 168) rgb(0, 0, 168)
                            if op1==10 and op2==10 and op3==10:
                                label1.setText("X")
                                label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF; font-size: 20px; ")    # Color de fondo para visualizar mejor                       
                                label2.setText("X")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                tiro10_label3.setText("X")
                                tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                tiro10_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            else:
                            #si el primero es 10 ya tiene derecho a otro tiro adicional
                             if op1<10:
                               
                               
                                  if op1!=0:  
                                      label1.setText(f"{op1}")
                                      label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor                       
                                  else:
                                      label1.setText("0")
                                      label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor    

                             else:
                                label1.setText("X")
                                label1.setStyleSheet(" background-color: #0000b9; color:#FFFFFF; font-size: 20px; ")    # Color de fondo para visualizar mejor
                            
                            # if  self.tiroActivo==2 and self.bolosTiro1<10 and self.bolosTiro1+self.bolosTiro2==10:

                             if op2<10:
                                if op1+op2==10 and op1<10 :
                                    label2.setText("/")
                                    label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor                       
                                else:
                                  if op2!=0:
                                      label2.setText(f"{op2}")
                                      label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                  else:
                                      label2.setText("0")
                                      label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                             else:
                                    label2.setText("X")
                                    label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor  
                            
                            
                            
                            
                            
                            
                             if op3<10: 
                                if op3!=0:
                                    tiro10_label3.setText(f"{op3}")
                                    tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                                else:
                                    tiro10_label3.setText("0")
                                    tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor
                            
                             else:
                                tiro10_label3.setText("X")
                                tiro10_label3.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visualizar mejor 
                    
                        else:
                          if op1 == 10:
                                label1.setText("")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText("X")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          elif op1 == 0 and op2 == 10:
                                label1.setText("0")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText("/")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          elif op1 == 0 and op2 == 0:
                                label1.setText("0")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px;")  
                                label2.setText("0")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          elif op1 + op2 == 10:
                                label1.setText(f"{op1}")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText("/")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")
                          else:
                                label1.setText(f"{op1}")
                                label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px; ")  
                                label2.setText(f"{op2}")
                                label2.setStyleSheet(" background-color: #0000b9; color:#FFFFFF;font-size: 20px;")

                        #label2.setStyleSheet("background-color: lightgray;")  # Color de fondo para visualizar mejor
                        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

                        # Añadir un poco de espacio entre los labels
                        top_layout.addWidget(label1)
                        top_layout.addSpacing(0)  # Espacio de 20 píxeles
                        top_layout.addWidget(label2)                  

                        if columna >= 9:
                            top_layout.addSpacing(0)  # Espacio de 20 píxeles
                            top_layout.addWidget(tiro10_label3)
                        
                            # Añadir el layout horizontal al layout principal
                        main_layout.addLayout(top_layout)
                            # Crear el label de abajo que ocupa el espacio de los dos de arriba
                        label3 = QLabel(f"{puntuacion_acumulada}")
                        label3.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 22px;")  # Color de fondo para visualizar mejor
                        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)                
                        main_layout.addWidget(label3)
                            # Establecer el layout en el widget de la celda
                        cell_widget.setLayout(main_layout)                        
                            # Añadir el widget a la celda de la tabla
                        self.table2.setCellWidget(fila, columna + 1, cell_widget)               
                    
                    else:
                        # Crear un widget para la celda
                        cell_widget = QWidget()                    
                        # Crear el layout vertical
                        main_layout = QVBoxLayout()
                        main_layout.setContentsMargins(0, 0, 0, 0)  # (izquierda, arriba, derecha, abajo)
                        main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear un layout horizontal para los dos labels de arriba
                        top_layout = QHBoxLayout()
                        top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
                        top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

                        # Crear los dos labels de arriba
                        label1 = QLabel()
                        label2 = QLabel()
                        tiro10_label3 = QLabel() #0055ff
                        label1.setText("")
                        label1.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 20px")    # Color de fondo para visualizar mejor
                        label2.setText("")
                        label2.setStyleSheet(" background-color: #0055ff; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visua
                        
                        tiro10_label3.setText("")
                        tiro10_label3.setStyleSheet(" background-color: #0055ff; color:#FFFFFF;font-size: 20px;")  # Color de fondo para visua
                        # Añadir un poco de espacio entre los labels
                        top_layout.addWidget(label1)
                        top_layout.addSpacing(0)  # Espacio de 20 píxeles
                        top_layout.addWidget(label2)   
                        if columna >= 9:
                            top_layout.addSpacing(0)  # Espacio de 20 píxeles
                            top_layout.addWidget(tiro10_label3)
                        
                            # Añadir el layout horizontal al layout principal
                        main_layout.addLayout(top_layout)
                            # Crear el label de abajo que ocupa el espacio de los dos de arriba
                        label3 = QLabel("")
                        label3.setStyleSheet(" background-color: #0055ff; color:#FFFFFF; font-size: 22px;")  # Color de fondo para visualizar mejor
                        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)                
                        main_layout.addWidget(label3)
                            # Establecer el layout en el widget de la celda
                        cell_widget.setLayout(main_layout)
                        # Añadir el widget a la celda de la tabla
                        self.table2.setCellWidget(fila, columna + 1, cell_widget)
                        
                        
                        
                        
                #if fila==jugadorActivo :
                  #  self.ui.label_puntaje.setText(f"{puntuacion_acumulada}")
                # Agregar colunma 11 la puntuación total a la última columna
                total_item = QTableWidgetItem(str(puntuacion_acumulada))
                total_item.setBackground(QColor(0, 85, 255)) #Color en RGB para mas precisión           
                total_item.setForeground(QColor("white")) # Cambiando el color del texto a blanco
                #total_item = QTableWidgetItem(str(300))
                # Crear un objeto QFont para definir el estilo de la fuente
                font = QFont()
                font.setPointSize(22)  # Tamaño de letra
                font.setBold(True) #opcional si quieres negrita
                # Aplicar el estilo de fuente al QTableWidgetItem
                total_item.setFont(font)
                # Centrar el texto horizontal y verticalmente
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

                self.table2.setItem(fila, 11, total_item) # 11 porque tenemos 10 rondas + nombre
                i=0
            
       
      self.aplicar_bordes_rojos2( jugadorActivo)
    
    def aplicar_bordes_rojos(self, fila_JugadorActivo):
         
        fila_seleccionada = fila_JugadorActivo
      
        if fila_seleccionada >= 0:
            
            for col in range(self.table1.columnCount()):
                item = self.table1.item(fila_seleccionada-1, col)               
                
                if item:
                    item.setForeground(QColor("white")) # restablece el color del texto
                    item.setBackground(QColor("red")) 
                      
    def aplicar_bordes_rojos2(self, fila_JugadorActivo):
         
        fila_seleccionada = fila_JugadorActivo
      
        if fila_seleccionada >= 0:
            
            for col in range(self.table2.columnCount()):
                item = self.table2.item(fila_seleccionada-1, col)               
                
                if item:
                    item.setForeground(QColor("white")) # restablece el color del texto
                    item.setBackground(QColor("red"))                   