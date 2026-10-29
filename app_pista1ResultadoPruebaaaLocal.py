import sys
from PyQt6.QtWidgets import QApplication,QDialog, QTableWidgetItem,QGridLayout, QVBoxLayout, QWidget, QHBoxLayout, QLabel,QHeaderView,QSizePolicy,QTableWidget,QAbstractItemView


from PyQt6.QtCore import Qt,QTimer, QTime,QMargins,QSize

from PyQt6.QtGui import QColor,QBrush, QPixmap

from PyQt6.QtGui import QFont
from ConexionBD import M221_Bolera
from UI.Strike import Strike
from UI.pista1Resultado import Pista1_Resultad
from ConexionBD.juego_Operaciones import JuegoBD_operaciones
from app_ResultadoJuego import ResultadoFinalWindow
from app_Spare import AnimacionSpare
from app_Strike import AnimacionStrike
from bd_modelos.juego_bolos import JuegoBolos



class Pista1Resultado(QDialog):
                                                  # ,segunda_pantalla
     def __init__(self, id_juego,segundos_iniciales):
        super().__init__()         
         # Initialize the UI from the generated 'main_ui' class
        self.ui = Pista1_Resultad()      
        self.ui.setupUi(self) 
          
        self.id_juego=id_juego
        #self.segunda_pantalla=segunda_pantalla
        # Operacones con la tabla juego     
        self.juegoBD_operaciones=JuegoBD_operaciones() 

       # Obtenemos del juego activo los ID y Nombre de los jugadores
        self.jugadoresJuego=self.juegoBD_operaciones.obtenerDeJuegoJugadores(self.id_juego)  
        #print(self.jugadoresJuego)
        #print(self.jugadoresJuego[0][0]) 

        # Configuracion del juego 
        # Inicializamos la bandera como un atributo de la clase
        self.bandera_ejecutado = False
        # Jugador Activo
        self.jugadorActivo=1
        # Valor de Ronda activa
        self.rondaActiva=1
        # Tiro activo
        self.tiroActivo=1

        # Variables para animaciones
        self.bolos=0
        self.bolosTiro1=0
        self.bolosTiro2=0


        self.table=self.ui.tabla_resultado     
        # Configurar el diálogo para que no tenga bordes
        # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Ajustar el tamaño de las columnas para ocupar todo el espacio disponible
        #self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
      
         # Ajustar la altura de la fila al contenido
         # Mostrar el diálogo maximizado
        self.showMaximized()
       
        # Actualizar la tabla cada 5 segundos
        #self.timer = QTimer(self)
        #self.timer.timeout.connect( self.abrir_AnimacionesStrike)
        #self.timer.start(5000)  # 5000 ms = 5 segundos
       
       #obtengo los datos de la BD
        self.jugadores=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego)
       #obtener de la clase Bolos la calificacion segun los datos
        # Inicializar el juego de bolos
        self.juego = JuegoBolos(self.jugadores)
        self.resultados = self.juego.calcular_puntuacion()  
        print(self.resultados)   
        self.configurar_tabla()
        self.llenar_tabla(self.jugadorActivo,self.rondaActiva)
        
         # Crear varios QLabel del 1 al 10
        self.bolo1 = QLabel("1")
         
        self.bolo1.setPixmap(QPixmap('./fotos/bolo1111.png'))
        self.bolo2 = QLabel("")
       
        self.bolo3 = QLabel("")
        self.bolo4 = QLabel("")
        self.bolo5 = QLabel("")
       
        self.bolo6 = QLabel("")
       
        self.bolo7 = QLabel("")
        self.bolo8 = QLabel("")
        self.bolo9 = QLabel("")
        self.bolo10 = QLabel("")
        self.bolo2.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo3.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo4.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo5.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo6.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo7.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo8.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo9.setPixmap(QPixmap('./fotos/bolo11.png'))
        self.bolo10.setPixmap(QPixmap('./fotos/bolo11.png'))
       
        
        
  
        #self.bolo1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
                    
       # self.mostrarDatosTabla()
        self.contar=0
        #Configuracion de el cronometro del juego
        # variable para iciar cronometro una vez que se para
        self.iniciarCro=0
        self.segundos_iniciales = segundos_iniciales
        self.tiempo_restante = segundos_iniciales
        self.tiempo = QTime(0, 0, 0).addSecs(segundos_iniciales)  #Creamos un objeto QTime a partir de los segundos
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.actualizar_cronometro)
        self.iniciar_cronometro()
        #ip_address = "192.168.0.1"  # Reemplaza con la IP de tu PLC
        ip_address = "localhost"  # Reemplaza con la IP de tu PLC
        port = 502
        self.m221cliente = M221_Bolera.M221(ip_address)
        try:       
            self.m221cliente.connectar()
           # Modifcar segun el
           # Escribimos en un registo %MW22 la cantidad de jugadores 4
            self.m221cliente.escribir_MW(22,len(self.jugadores))
           #Activamos en Juego por la pista 1
            self.m221cliente.escribir_bit_M(10,1, True)
            print("*************** Inicio *******************")
           #Leer jugador activo %MW24
           # self.jugadorActivo=self.m221cliente.leer_MW(24)
                # self.jugadorActivo=1
                # print('Lectura de Registro MW24 Jugador Activo= ',self.jugadorActivo)
                #Leer ronda activa  %MW26
            #self.rondaActiva=self.m221cliente.leer_MW(26)
                 #self.rondaActiva=1
                # print('Lectura de Registro MW2 Ronda Activa= ',self.rondaActiva)
            #self.tiroActivo=self.m221cliente.leer_MW(30)
                     

            print("***************")   
            print("Jugador Activo ",self.jugadorActivo)    
            print("Ronda Activa ",self.rondaActiva) 
            print("Tiro Activo ",self.tiroActivo)                
            print("***************") 
            print("---------- Fin de INicio -----------")
        except Exception as e:
          print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")
         
   
        self.timer = QTimer()
        self.timer.timeout.connect(self.comunicacion_plc)
        self.timer.start(1000)  # Ejecuta `comunicacion_plc` cada 1000 milisegundos (1 segundo)

        self.banderaBolos=True
         # Variables para animaciones
        self.bolosMostrar=[]
         
     def comunicacion_plc(self):
         
       try:
             if self.banderaBolos :
                 self.create_bowling_pins()
                 self.banderaBolos=False
                  
            # Lee información del PLC
            # Leo M10 bit 0 para saber si ya se activo la secuencia del juego
             leerM0=self.m221cliente.leer_bit(10,1)
             #si esta en 1  esta activado el juego Pista 1 y comenzamos a Jugar
             if leerM0==1 :
                #Leer jugador activo %MW24
                 self.jugadorActivo=self.m221cliente.leer_MW(24)
                # self.jugadorActivo=1
                # print('Lectura de Registro MW24 Jugador Activo= ',self.jugadorActivo)
                #Leer ronda activa  %MW26
                 self.rondaActiva=self.m221cliente.leer_MW(26)
                 #self.rondaActiva=1
                # print('Lectura de Registro MW2 Ronda Activa= ',self.rondaActiva)
                 self.tiroActivo=self.m221cliente.leer_MW(30)
                 #self.tiroActivo=self.tiroActivo
                     

                 #print("***************")   
                 #print("Jugador Activo ",self.jugadorActivo)    
                # print("Ronda Activa ",self.rondaActiva) 
                 #print("Tiro Activo ",self.tiroActivo)                
                 #print("***************") 

                
                # Leo M4 bit 0 para saber si el jugador puede tirar
                 leerM4=self.m221cliente.leer_bit(4,1)                 
                 # Aqui hacemos algo se el jugador puedo tirar!
                # print('Lectura de un bit de M3 Jugador puede tirar', leerM4)
                 # Falta codigo
                 if leerM4==False :
                    self.detener_cronometro() 
                    print("Detener cronometro")
                    self.iniciarCro=1  
                   

                 if  self.iniciarCro== 1  and    leerM4==True :
                     self.iniciar_cronometro()
                     self.iniciarCro=0
                     print("Iniciar cronometro")  
                     
                  
                     
                     
                     
                     


                # Leemos si el Jugador ya tiro
                # Leo M7 bit 0 para saber si se produjo el tiro y podemos leer
                 leerM7=self.m221cliente.leer_bit(7,1)
                
                 
                                
                  
                 if not leerM7 and self.bandera_ejecutado:
                    self.bandera_ejecutado = False # Reseteamos la bandera a False para la proxima ejecución
                    print("Bandera reseteada a false")

                 
                 if leerM7 and not self.bandera_ejecutado:
                     
                      print("************* Leer **************")
                      
                      #Leeeemmos los bolos
                    
                      bolo10=self.m221cliente.leer_bit(50,1)
                      if bolo10:
                          self.bolo10.setText("10")
                          print("El Bolo esta paradoooooooo")
                      else:
                           self.bolo10.setText("")  
                           print("El Bolo cayooooooooooooooooooooooo")  
                      
                      self.bandera_ejecutado = True
                      print("Bandera ahora es True")               
                  
                  
                                    
                      # debo actualizar el juego con jugador activo, tiro activo y ronda activa
                      ## codigo aqui para actualizar la BD
                      print("*************** Leer ****************")   
                      print("Jugador Activo ",self.jugadorActivo)    
                      print("Ronda Activa ",self.rondaActiva) 
                      print("Tiro Activo ",self.tiroActivo)                
                      print("***************")
                      e=self.juegoBD_operaciones.actualizarJuego(self.id_juego,self.jugadorActivo,self.rondaActiva,self.tiroActivo)
                      # Leo los bolos que se tumbaron
                      #Leer bolos %20
                      self.bolos=self.m221cliente.leer_MW(20)

                      if self.tiroActivo==1 :
                        self.bolosTiro1=self.bolos
                      else:
                        self.bolosTiro2=self.bolos

                       ## Actualizamos el jugador con los bolos que tumbo
                        # Codigo aqui para actualizar el jugador
                      self.juegoBD_operaciones.actualizarJuegoTiroJugadores( 
                                                                            
                            self.jugadoresJuego[self.jugadorActivo-1][0],                            
                            self.rondaActiva,
                            self.tiroActivo,
                            self.bolos
                            
                            )
                      #obtengo los datos de la BD
                      self.jugadores=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego)
                      # Inicializar el juego de bolos
                      self.juego = JuegoBolos(self.jugadores)
                      self.resultados = self.juego.calcular_puntuacion()  
                      self.llenar_tabla(self.jugadorActivo,self.rondaActiva)  

                      # como ya se produjo el Tiro y ya hici tod mando adesactivar esa opcion
                      # esto es para simulacion
                      print("Bolos tiro1 = ",self.bolosTiro1)
                      print("Bolos tiro2 = ",self.bolosTiro2)
                      # comprobamos si el tiro activo es el 1 y tumbo los 10 bolo ver animcacion
                      if self.tiroActivo==1 and self.bolos==10:
                          #ver animacion
                          print ("animacion Strike")
                          self.abrir_AnimacionesStrike()
                          self.bolos==0
                      
                        # comprobamos si el tiro activo es el 1 y tumbo los 10 bolo ver animcacion
                      if self.bolosTiro1+self.bolosTiro2==10:
                          #ver animacion
                          #print ("animacion Spare") 
                          self.abrir_AnimacionesSpare()
                          self.bolos=0
                          self.bolosTiro2=0
                      
                      #self.m221cliente.escribir_bit_M(7,1, False) 

                 self.llenar_tabla(self.jugadorActivo,self.rondaActiva)
                 self.ui.label_jugador.setText(f"Jugador={self.jugadorActivo} Ronda={self.rondaActiva} Tiro={self.tiroActivo}")
                 self.ui.label_jugador.setText(f"{self.jugadoresJuego[self.jugadorActivo-1][1]}")
                 if self.rondaActiva==11:
                     self.m221cliente.escribir_MW(26,10)
                    
                     #Activamos en Juego por la pista 1
                 
                    # self.m221cliente.escribir_bit_M(10,1, False)
                     self.abrirResultado(sorted(self.resultados, key=lambda x: x['puntuacion'], reverse=True))                    
                     
                    # self.nueva_ventana = ResultadoFinalWindow(self,sorted(self.resultados, key=lambda x: x['puntuacion'], reverse=True))
                     #self.nueva_ventana.show()
                     self.close()
                     
                     


       except Exception as e:
            print(f"Error en la comunicación con el PLC por que seraaaaaaaaaaaa: {e}")
            # Manejo de errores

     
     def abrirResultado(self,resultados):
          self.nueva_ventana = ResultadoFinalWindow(resultados)
          self.nueva_ventana.show()
          print("Cerrooooooooooooooooooooooooooo111")
           # Crear un temporizador para cerrar la nueva ventana después de 1 segundo
          QTimer.singleShot(10000, self.nueva_ventana.close)  # 1000 ms = 1 segundo
         
     def closeEvent(self, event):
        self.timer.stop() # Detener el timer al cerrar la ventana
        self.timer1.stop()
         #Desactivamos en Juego por la pista 1
        self.m221cliente.escribir_bit_M(10,1, False)
        super().closeEvent(event)

     def configurar_tabla(self):
        columnas = ['Jugador  ']
        columnas.extend([f'{i+1}' for i in range(10)])
        columnas.append("Total") #Agregamos la columna de puntuacion total
        self.table.setColumnCount(len(columnas))
        self.table.setHorizontalHeaderLabels(columnas)
        self.table.setRowCount(len(self.resultados))
        if len(self.resultados)<=  2:
           for _ in range(2):  # Agregar 2 filas
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

        #Aplicar estilos en los encabezados de la fila 
         # Personalización de cada encabezado de columna
        font = QFont("Arial", 18, QFont.Weight.Bold) #Fuente Arial, tamaño 12, negritacd.

        for i in range(len(columnas)):
            item = QTableWidgetItem(columnas[i])
            item.setFont(font) #Aplicando la fuente personalizada
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
            item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión
            item.setForeground(QColor(255, 255, 255)) 
            self.table.setHorizontalHeaderItem(i, item)


        self.table.setColumnWidth(0, 400) #  Ajusta el valor 150 a tu gusto.
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
          # Ocultar el encabezado vertical (numeración de filas)
        self.table.verticalHeader().setVisible(False)  # Cambia esto para ocultar el encabezado vertical
           
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
         # Ajustar el estilo del encabezado
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { height: 60px;  background-color: #0055ff; }")  # Aumentar la altura del encabezado
         # Quitar las líneas verticales
        #self.table.setStyleSheet(""" """)  # Sin bordes en la tabla
       # self.table.setShowGrid(False)  # Quitar la cuadrícula
        self.table.verticalHeader().setDefaultSectionSize(110)
         #Este es el truco para distribuir uniformemente las filas
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        
        
     def llenar_tabla(self,jugadorActivo,rondaActiva):
        #enumerate(self.resultados)
        
        for fila, resultado in enumerate(self.resultados):
           
                nombre_item = QTableWidgetItem(resultado['nombre'])
                nombre_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #Centrando el texto
                nombre_item.setBackground(QColor(90,170, 255)) #Color en RGB para mas precisión           
                fontNombre = QFont()
                fontNombre.setPointSize(21)  # Tamaño de letra
                fontNombre.setBold(True) #opcional si quieres negrita           
                nombre_item.setFont(fontNombre)
                self.table.setItem(fila, 0, nombre_item)            
                puntuacion_acumulada = 0
                for columna, puntuacion_ronda in enumerate(resultado['rondas']):
                    if columna<rondaActiva and fila<= len(self.resultados):
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
                            #Si todos los tiros fueron 10 escribir X #0000b9
                            if op1==10 and op2==10 and op3==10:
                                label1.setText("X")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px; ")  # Color de fondo para visualizar mejor                       
                                label2.setText("X")
                                label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor
                                tiro10_label3.setText("X")
                                tiro10_label3.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor
                                tiro10_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            else:
                            #si el primero es 10 ya tiene derecho a otro tiro adicional
                             if op1<10:
                                if op1!=0:
                                    label1.setText(f"{op1}")
                                    label1.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor                       
                                else:
                                    label1.setText("-")
                                    label1.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor    

                             else:
                                label1.setText("X")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")  # Color de fondo para visualizar mejor
                             if op2<10:
                                if op2!=0:
                                    label2.setText(f"{op2}")
                                    label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor
                                else:
                                    label2.setText("-")
                                    label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor
                             else:
                                    label2.setText("X")
                                    label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor  
                            
                             if op3<10: 
                                if op3!=0:
                                    tiro10_label3.setText(f"{op3}")
                                    tiro10_label3.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor
                                else:
                                    tiro10_label3.setText("-")
                                    tiro10_label3.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor
                            
                             else:
                                tiro10_label3.setText("X")
                                tiro10_label3.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visualizar mejor 
                    
                        else:
                          if op1 == 10:
                                label1.setText("")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")
                                label2.setText("X")
                                label2.setStyleSheet("background-color: #FFFFFF;font-size: 60px;")
                          elif op1 == 0 and op2 == 10:
                                label1.setText("0")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")
                                label2.setText("/")
                                label2.setStyleSheet("background-color: #FFFFFF;font-size: 60px;")
                          elif op1 == 0 and op2 == 0:
                                label1.setText("0")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")
                                label2.setText("0")
                                label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")
                          elif op1 + op2 == 10:
                                label1.setText(f"{op1}")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")
                                label2.setText("/")
                                label2.setStyleSheet("background-color: #FFFFFF;font-size: 60px;")
                          else:
                                label1.setText(f"{op1}")
                                label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")
                                label2.setText(f"{op2}")
                                label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")

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
                        label3.setStyleSheet("background-color: rgb(90, 170, 255); font-size: 40px;")  # Color de fondo para visualizar mejor
                        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)                
                        main_layout.addWidget(label3)
                            # Establecer el layout en el widget de la celda
                        cell_widget.setLayout(main_layout)                        
                            # Añadir el widget a la celda de la tabla
                        self.table.setCellWidget(fila, columna + 1, cell_widget)  
                                    
                    
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
                        tiro10_label3 = QLabel() 
                        label1.setText("")
                        label1.setStyleSheet("background-color: rgb(90, 170, 255);font-size: 40px;")  # Color de fondo para visualizar mejor
                        label2.setText("")
                        label2.setStyleSheet("background-color: #FFFFFF;font-size: 40px;")  # Color de fondo para visua
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
                        label3.setStyleSheet("background-color: rgb(90, 170, 255); font-size: 40px;")  # Color de fondo para visualizar mejor
                        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)                
                        main_layout.addWidget(label3)
                            # Establecer el layout en el widget de la celda
                        cell_widget.setLayout(main_layout)
                        # Añadir el widget a la celda de la tabla
                        self.table.setCellWidget(fila, columna + 1, cell_widget)
                        
                        
                        
                        
               
                # Agregar colunma 11 la puntuación total a la última columna
                total_item = QTableWidgetItem(str(puntuacion_acumulada))
                # Crear un objeto QFont para definir el estilo de la fuente
                font = QFont()
                font.setPointSize(32)  # Tamaño de letra
                font.setBold(True) #opcional si quieres negrita
                # Aplicar el estilo de fuente al QTableWidgetItem
                total_item.setFont(font)
                # Centrar el texto horizontal y verticalmente
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

                self.table.setItem(fila, 11, total_item) # 11 porque tenemos 10 rondas + nombre
                i=0
            
       
        self.aplicar_bordes_rojos( jugadorActivo)
            
     def aplicar_bordes_rojos(self, fila_JugadorActivo):
         
        fila_seleccionada = fila_JugadorActivo
      
        if fila_seleccionada >= 0:
            
            for col in range(self.table.columnCount()):
                item = self.table.item(fila_seleccionada-1, col)               
                
                if item:
                    item.setForeground(QColor("green")) # restablece el color del texto
                    item.setBackground(QColor("blue")) 
                  
                    self.table.setStyleSheet(f"""
                    QTableWidget::item:Select {{
                        border-top: 2px solid blue;
                        border-bottom: 2px solid red;
                       
                    }}
                    
                   
                    """)
                    
              
                   
                 
            #self.table.viewport().update()  # Forzar una actualización visual

     def mostrarDatosTabla(self):
         datos=self.juegoBD_operaciones.obtenerDeJuegoJugadoresTiros(self.id_juego)
         self.table.setRowCount(len(datos)) 
         #¶print(f"tamano = {len(datos)}")
         print(datos)
        
         if len(datos)>0:
           for i, jugador in enumerate(datos):
            # print(f"Jugador: {jugador['nombre']}")
            j=0
            for tiro in jugador['tiros']:
               #print(f"  Tiro {tiro['numero_tiro']}: Op1={tiro['op1']}, Op2={tiro['op2']}, Op3={tiro['op3']}")
               # Crear un widget para la celda
               cell_widget = QWidget()        
               
               # Crear el layout vertical
               main_layout = QVBoxLayout()
               main_layout.setContentsMargins(0, 0, 2, 0)  # (izquierda, arriba, derecha, abajo)
               main_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

               # Crear un layout horizontal para los dos labels de arriba
               top_layout = QHBoxLayout()
               top_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes en el top_layout
               top_layout.setSpacing(0)  # Sin espacio entre los widgets del top_layout

            # Crear los dos labels de arriba
               label1 = QLabel(f"{tiro['op1']}")
               label1.setStyleSheet("background-color: lightgray;font-size: 25px;")  # Color de fondo para visualizar mejor
               label2 = QLabel((f"{tiro['op2']}"))
            
               label2.setStyleSheet("background-color: #FFFFFF;font-size: 25px;")  # Color de fondo para visualizar mejor
               #label2.setStyleSheet("background-color: lightgray;")  # Color de fondo para visualizar mejor
               label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
               label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

               # Añadir un poco de espacio entre los labels
               top_layout.addWidget(label1)
               top_layout.addSpacing(0)  # Espacio de 20 píxeles
               top_layout.addWidget(label2)

               # Añadir el layout horizontal al layout principal
               main_layout.addLayout(top_layout)

               # Crear el label de abajo que ocupa el espacio de los dos de arriba
               label3 = QLabel("200")
               label3.setStyleSheet("background-color: lightgray; lightgray;font-size: 30px;")  # Color de fondo para visualizar mejor
               label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
               main_layout.addWidget(label3)  
               
               
            

               # Establecer el layout en el widget de la celda
               cell_widget.setLayout(main_layout)
               # Establecer un tamaño fijo para el widget de la celda
               cell_widget.setFixedSize(100, 132)  # Ancho 150, Alto 100

               # Añadir el widget a la celda de la tabla
               self.table.setCellWidget(i, j, cell_widget)
            
               # La columna 11 (índice 10) se deja vacía o se puede rellenar como desees
            # self.table.setItem(0, 10, QTableWidgetItem("Columna 11 vacía"))  # Columna 11
            # Ajustar el tamaño de las columnas al contenido
               self.table.horizontalHeader().setSectionResizeMode(j, QHeaderView.ResizeMode.ResizeToContents)
               # La columna 11 (índice 10) se deja vacía o se puede rellenar como desees 
               j=j+1
         
           self.table.setItem(i, 10, QTableWidgetItem("Columna 11 vacía"))  # Columna 11
       
            # self.table.verticalHeader().setSectionResizeMode(row, QHeaderView.ResizeMode.ResizeToContents)  # Opción para ajustar automáticamente
          # Ajusta este valor según necesites
           self.table.resizeRowToContents(i)        
            # Crear una lista de encabezados
           jugadores = [jugador['nombre'] for jugador in datos]
         
            # Cambiar el tipo de letra y el tamaño para los encabezados de la tabla
           font = QFont("Arial", 24)  # Cambia "Arial" y 16 por el tipo y tamaño que desees
           self.table.verticalHeader().setFont(font)
           self.table.setVerticalHeaderLabels(jugadores)
            
         
         #self.table.verticalHeader().setFixedSize(100, 120)
            # Establecer un tamaño fijo para el encabezado vertical
            # Esto establece la altura del encabezado vertical

         #self.table.verticalHeader().setDefaultSectionSize(97)  # Establecer la altura fija
         # Establecer los encabezados verticales
         
         
            # Aplicar estilo CSS al encabezado vertical
           self.table.verticalHeader().setStyleSheet("QHeaderView::section {"
                                                         "font-size: 24px;"  # Tamaño de fuente
                                                         "text-align: center;"  # Centrar texto
                                                         "background-color: lightgray;"  # Color de fondo (opcional)
                                                         " border: none; "
                                                         "}")
            
           i=0
           for jugador in datos:
                  
                  self.table.setRowHeight(i, 165)
                  self.table.verticalHeader().setDefaultSectionSize(135)
                  i=i+1
                  #self.table.verticalHeader().setSectionResizeMode(row, QHeaderView.ResizeMode.ResizeToContents)  # Opción para ajustar automáticamente
                  # Establecer un tamaño fijo para cada sección del encabezado vertical
         
         else:
          print("No se pudieron obtener los datos de los jugadores.")
          print(datos)
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
        grid_layout.setContentsMargins(QMargins(0,0,0,80))
        grid_layout.setSpacing(40)
       
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
                    pixmap = QPixmap(f"./fotos/bolo{bolo_numero}.png")
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(QSize(25, 48),
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
        self.ui.bolos.setLayout(grid_layout) 
     def abrir_AnimacionesStrike(self):
            self.nueva_ventana = AnimacionStrike()
       # self.nueva_ventana.show()
      # Obtener información sobre las pantallas
            screen_count = QApplication.screens()
            # Obtener la segunda pantalla
            #segunda_pantalla = screen_count[1]
           # self.sub_window22=VentanaVideo()
            # Calcular la posición de la segunda pantalla
            
            #screen_geometry = self.segunda_pantalla.geometry()
            #nueva_ventana.setGeometry(screen_geometry.x() + 100, screen_geometry.y() + 100, 300, 100)
            
            
            # Mostrar el diálogo
            self.nueva_ventana.showFullScreen()        

           # Crear un temporizador para cerrar la nueva ventana después de 1 segundo
            QTimer.singleShot(5000, self.nueva_ventana.close)  # 1000 ms = 1 segundo    
  #      Funciones para el cronometro de parada del juego
     def abrir_AnimacionesSpare(self):
            nueva_ventana1 = AnimacionSpare()
      
            screen_count = QApplication.screens()
           
            # Calcular la posición de la segunda pantalla
            #screen_geometry = self.segunda_pantalla.geometry()
            #self.nueva_ventana.setGeometry(screen_geometry.x() + 100, screen_geometry.y() + 100, 300, 100)
            # Mostrar el diálogo
            nueva_ventana1.showFullScreen()
        

           # Crear un temporizador para cerrar la nueva ventana después de 1 segundo
            QTimer.singleShot(5000, nueva_ventana1.close)  # 1000 ms = 1 segundo    
  #      Funciones para el cronometro de parada del juego
     def formato_tiempo(self):
                horas = self.tiempo.hour()
                minutos = self.tiempo.minute()
                segundos = self.tiempo.second()
                return f"{horas:02}:{minutos:02}:{segundos:02}"  #Formato HH:MM:SS

     def iniciar_cronometro(self):
                self.timer1.start(1000)  # 1000 milisegundos = 1 segundo
     def actualizar_cronometro(self):
                self.tiempo = self.tiempo.addSecs(-1)
                self.ui.label_tiempo_juego.setText(self.formato_tiempo())
                self.tiempo_restante -=1
                if self.tiempo_restante <=0:
                    self.timer1.stop()
                    #Desactivamos en Juego por la pista 1
                    self.m221cliente.escribir_bit_M(10,1, False)
                    self.close()

     def detener_cronometro(self):
            self.timer1.stop() 
            
     def ordenar_por_puntuacion(resultados):   
   
        """
        Ordena una lista de diccionarios por el campo 'puntuacion' de mayor a menor.

        :param datos: Lista de diccionarios con el campo 'puntuacion'.
        :return: Lista ordenada de mayor a menor por 'puntuacion'.
        """
        return sorted(resultados, key=lambda x: x['puntuacion'], reverse=True)       
       
if __name__ == "__main__":
     
    app = QApplication(sys.argv)
    window =Pista1Resultado(7,36000)
    window.show()
    sys.exit(app.exec())