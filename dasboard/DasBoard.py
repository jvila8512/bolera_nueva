import sys
from PyQt6.QtWidgets import QMainWindow,  QListWidgetItem, QWidget, QMessageBox,QMenu
from PyQt6.QtCore import Qt, QSize,QDate,QDateTime,QTime,QTimer,QPoint
from PyQt6.QtGui import QIcon, QPixmap, QFont,QAction
from PyQt6 import  QtGui
# Import the UI class from the 'main_ui' module

from Crud.juegos.CrudJuegos import JuegosCrudADmin
from Crud.sesion.app_Crud_Sesion import SesionCRUD

import app_CambiarContrasena
from app_Perfil import PerfilDialog
from app_dialogoPrecio import CrudPrecio
from bd_modelos import Sesion
import recursos
import recuroAnimacion
from ConexionBD import M221_Bolera



from app_Crud_User import UserCRUD
from app_GestionarPistas import GestionPistas
from bd_modelos.usuario import Usuario
from dasboard.main2 import Principal




# Define a custom MainWindow class
class MainWindow(QMainWindow):
    def __init__(self,user: Usuario,sesion: Sesion):
        super().__init__()
        # Initialize the UI from the generated 'main_ui' class
        self.ui = Principal()
        self.ui.setupUi(self)
        # Set window properties
         # Mostrar el diálogo maximizado
        self.showMaximized()
        #self.showFullScreen()
        self.setWindowIcon(QIcon(":iconos/dasboard/icon/icono.jpg"))
        self.setWindowTitle("Control Automático de la Bolera")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Initialize UI elements
        self.title_label = self.ui.title_label
        self.title_label.setText("AppBolos")
        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap(":iconos/dasboard/icon/title_icon.png"))
        self.title_icon.setScaledContents(True)
        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only = self.ui.listWidget_icon_only
        self.side_menu_icon_only.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        #self.side_menu_icon_only.hide()
        # Quitar el botón de cerrar
        #self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        #Ventanas Secundarias para cerrarlas
        self.sub_window = None #CarruselFotos() # Inicializamos la sub-ventana del TV 1 como None
        self.sub_window1 = None # Inicializamos la sub-ventana del TV 2 como None 
        
             
        self.ventana_ResultadosPista1 = None # Inicializamos la sub-ventana de Pista1 Resltados como None
        self.ventana_ResultadosPista2 = None # Inicializamos la sub-ventana de Pista1 Resltados como None

        # Conectar la señal de cierre de la ventana principal
        self.aboutToClose = self.closeEvent
          #Mando a cerrar las pistas cdo levanta el juego
        ip_address1 = "192.168.0.2"  # Reemplaza con la IP de tu PLC
                    #ip_address = "localhost"  # Reemplaza con la IP de tu PLC
        self.m221cliente1 = M221_Bolera.M221(ip_address1)
        #ip_address = "192.168.0.1"  # Reemplaza con la IP de tu PLC
        ip_address = "localhost"  # Reemplaza con la IP de tu PLC
        self.m221cliente = M221_Bolera.M221(ip_address)
       
    
       # Configurar un QTimer para ejecutar código después de que la ventana esté visible
        QTimer.singleShot(0, self.codigo_despues_de_visible)

        
      







       
        
        self.menu_btn = self.ui.menu_btn
        self.menu_btn.setText("")
        self.menu_btn.setIcon(QIcon(":iconos/dasboard/icon/close.svg"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)
        self.main_content = self.ui.stackedWidget
          
        self.UserLogueado = user
        self.sesionActiva=sesion
       # print(self.sesionActiva.fecha)
        # La fecha y hora en formato de cadena"2025-01-15 12:33:25"
        fecha_hora_str = str(self.sesionActiva.fecha)

        # Dividir la cadena en fecha y hora
        fecha_str, hora_str = fecha_hora_str.split(' ')
        
        # Descomponer la fecha
        anio, mes, dia = map(int, fecha_str.split('-'))
        
        # Descomponer la hora
        horas, minutos, segundos = map(int, hora_str.split(':'))

        # Crear el objeto QDateTime
        fecha_hora = QDateTime(QDate(anio, mes, dia), QTime(horas, minutos))

        # Formatear el objeto QDateTime a "DD/MM/AAAA HH:MM"
        fecha_hora_formateada = fecha_hora.toString("dd/MM/yyyy HH:mm AP")
        
        self.ui.user_name.setText(f" {self.UserLogueado.usuario} ")
        self.ui.label_2.setText( fecha_hora_formateada)
     

        # Define a list of menu items with names and icons
   
        self.menu_list =[]
        if self.UserLogueado.rol=="Administrador":     
            
            self.menu_list = [
            {
                    "name": "Gestión de Pistas",
                      "icon": ":animacion/iconos/bolera.svg"
                },
                {
                    "name": "Usuarios",
                    "icon": ":iconos/dasboard/icon/customers.svg"
                },
                 {
                    "name": "Sesión",
                    "icon": ":iconos/iconos/list.svg"
                },
                 {
                    "name": "Juegos",
                    "icon": ":iconos/iconos/users.svg"
                }, 
                 
                {
                    "name": "Precio",
                    "icon": ":iconos/dasboard/icon/reports.svg"
                }
              
            
            ] 
        else:
            self.menu_list = [
            {
                    "name": "Gestión de Pistas",
                    "icon": ":animacion/iconos/bolera.svg"
                },
               
               
             
            ]
            
        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()
        
        style_str = """/* Define styles for the 'title_label' widget */
#title_label {
    font-size: 16px;
    font-family: Amazone BT;
}

/* Define styles for the 'title_icon' widget */
#title_icon {
    max-width: 35px;
    max-height: 35px;
}

/* Define styles for the 'menu_btn' widget */
#menu_btn {
    border: none;
}

/* Define styles for the 'QStackedWidget' */
QStackedWidget {
    background-color: #fff;
}

/* Define styles for 'QListWidget' and '#title_frame' */
QListWidget,
#title_frame {
    background-color:   rgb(165, 191, 218);
   
}


/* Define border styles for '#stackedWidget' and '#title_frame' */
#stackedWidget,
#title_frame {
    border: 1px solid #828790;
}

/* Additional border style for '#stackedWidget' */
#stackedWidget {
    border-left: none;
}

/* Additional border style for '#title_frame' */
#title_frame {
    border-bottom: none;
}

/* Define font styles for '#listWidget' */
#listWidget {
    font-size: 13px;
    font-family: Segoe UI Semibold;
}

/* Styles for list items in '#listWidget' and '#listWidget_icon_only' */
#listWidget::item,
#listWidget_icon_only::item {
    /* Ensure borders are set for proper styling */
    border: 0px;
    padding: 5px 10px;
    margin: 2px 0;
}

/* Border radius for '#listWidget' items */
#listWidget::item {
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
}

/* Border radius for '#listWidget_icon_only' items */
#listWidget_icon_only::item {
    border-top-right-radius: 18px;
    border-bottom-right-radius: 18px;
}

/* Padding adjustment for '#listWidget_icon_only' items */
#listWidget_icon_only::item {
    padding-top: 0px;
}

/* Hover effect for list items */
#listWidget::item:hover,
#listWidget_icon_only::item:hover {
    background-color: #fd0000;
}

/* Selected item styles for list items */
#listWidget::item:selected,
#listWidget_icon_only::item:selected {
    background-color: #00aaff;
}

/* Define icon dimensions for '#listWidget' items */
#listWidget::icon {
    width: 16px;
    height: 16px;
}

/* Define icon dimensions for '#listWidget_icon_only' items */
#listWidget_icon_only::icon {
    width: 23px;
    height: 23px;
}
"""
       
                   
        self.setStyleSheet(style_str) 
        #print(self.main_content.currentIndex())
        self.side_menu.setHidden(True)
        self.title_label.setVisible(False)
        self.side_menu_icon_only.setVisible(True)
        self.title_icon.setHidden(True)
      
        # Configuracion del menu contextual de la secion    
        self.ui.user_name.clicked.connect(self.mostrar_menu)
        self.ui.pushButton.clicked.connect(self.cerrarApp)

        # Crear el menú contextual
        self.menu_contextual = QMenu(self)

        # Añadir acciones al menú
        self.accion_cerrar_sesion = QAction("Perfil", self)
        self.accion_cerrar_sesion.setIcon(QIcon(":iconos/dasboard/icon/customers.svg"))      
        self.accion_cambiar_contrasena = QAction("Cambiar contraseña", self)
        self.accion_cambiar_contrasena.setIcon(QIcon(":iconos/dasboard/icon/settings.svg"))

        # Conectar las acciones a funciones (puedes definir las funciones según sea necesario)
        self.accion_cerrar_sesion.triggered.connect(self.cerrar_sesion)
        self.accion_cambiar_contrasena.triggered.connect(self.cambiar_contrasena)

        # Añadir acciones al menú
        self.menu_contextual.addAction(self.accion_cerrar_sesion)
        self.menu_contextual.addAction(self.accion_cambiar_contrasena)
        
        
      
        self.ui.maximixar.clicked.connect(self.maximize_window)
        self.ui.minimizar.clicked.connect(self.showMinimized)
         # Variables para manejar el arrastre
        self.dragging = False
        self.offset = QPoint()
        
        
        
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False    
    def codigo_despues_de_visible(self):
        print("La ventana ya está visible. Ejecutando código adicional...")
       
       
        try:       
                        resul=self.m221cliente.connectar()
                                                
                        #DesacActivamos en Juego por la pista 1
                        if resul :
                            #Desactivamos en Juego por la pista 1
                            self.m221cliente.escribir_bit_M(10,1, False)
                            #DEsactivamosActivamos en motor de las bolas
                            self.m221cliente.escribir_bit_M(12,1, False) 

                             #Desactivamos en Juego por la pista 2 esta en M210
                            self.m221cliente.escribir_bit_M(210,1, False) 

                            self.m221cliente.desconectar() 
                            print("Conexionnnnnnnnnnnnnnnn exitosaaaaaaaaa")
                        else:
                          print("Conexionnnnnnnnnnnnnnnn nooooooooooooo exitosaaaaaaaaa")    
        except Exception as e:
                    print(f"Programa Aqui algun mensaje de error de Comunicacion {e}") 
        # Aquí puedes poner el código que deseas ejecutar    
    def maximize_window(self):
        # Alternar entre maximizar y restaurar
        if self.isMaximized():
            self.showNormal()
           
        else:
            self.showMaximized()
    def mostrar_menu(self):
        # Mostrar el menú contextual en la posición del botón
        self.menu_contextual.exec(  self.ui.user_name.mapToGlobal(  self.ui.user_name.rect().bottomLeft()))

    def cerrar_sesion(self):
        print("Cerrar sesión")
        self.cambiar= PerfilDialog(self.UserLogueado,self.sesionActiva)
        self.cambiar.enviar_datosUser.connect(self.recibir_User)
        self.cambiar.exec()

    def cambiar_contrasena(self):
        print("Cambiar contraseña")
        cambiar= app_CambiarContrasena.CambiarContrasenaDialog(self.UserLogueado,self.sesionActiva)
        cambiar.exec()
    
    def recibir_User(self,userActualizado):
        print("Holaa")  
        self.UserLogueado=userActualizado
        print(self.UserLogueado)
    
      
        
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
           
             if self.sub_window is not None: # Validamos que no sea None
        # Cerrar el diálogo si está abierto
              if self.sub_window.isVisible():
                self.sub_window.close()
                self.sub_window=None
        # Cerrar el diálogo si está abierto
             if self.sub_window1 is not None: # Validamos que no sea None 
                if self.sub_window1.isVisible():
                   self.sub_window1.close()
                   self.sub_window1=None  

             if self.ventana_ResultadosPista1 is not None: # Validamos que no sea None:
                if  self.ventana_ResultadosPista1.isVisible():
                    self.ventana_ResultadosPista1.close()
                    self.ventana_ResultadosPista1 = None
            # self.label.setText("Tercera ventana cerrada.") 
             if self.ventana_ResultadosPista2 is not None: # Validamos que no sea None:
                if  self.ventana_ResultadosPista2.isVisible():
                    self.ventana_ResultadosPista2.close()
                    self.ventana_ResultadosPista2 = None
           
           
                                
             try:       
                                            
                                    resul=self.m221cliente.connectar()
                                                
                                #DesacActivamos en Juego por la pista 1
                                    if resul :
                                            #Desactivamos en Juego por la pista 1
                                            self.m221cliente.escribir_bit_M(10,1, False) 
                                            #DEsactivamosActivamos en motor de las bolas
                                            self.m221cliente.escribir_bit_M(12,1, False)
                                            #Desactivamos en Juego por la pista 2
                                            self.m221cliente.escribir_bit_M(210,1, False)
                                            self.m221cliente.desconectar()  
             except Exception as e:
                  print(f"Programa Aqui algun mensaje de error de Comunicacion {e}")  
             
             self.close()
        
          
             
    def init_single_slot(self):
        # Connect signals and slots for menu button and side menu
        self.menu_btn.toggled['bool'].connect(self.side_menu.setHidden)
        self.menu_btn.toggled['bool'].connect(self.title_label.setHidden)
        
        
        self.menu_btn.toggled['bool'].connect(self.side_menu_icon_only.setVisible)
        self.menu_btn.toggled['bool'].connect(self.title_icon.setHidden)

        # Connect signals and slots for switching between menu items
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_icon_only.setCurrentRow)
        
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.side_menu.setCurrentRow)
        
        self.menu_btn.toggled.connect(self.button_icon_change)
        
        
    def init_list_widget(self):
        # Initialize the side menu and side menu with icons only
        self.side_menu_icon_only.clear()
        self.side_menu.clear()
        self.icono_precio = ":iconos/dasboard/icon/reports.svg"
        
        
        for  menu in self.menu_list:
            # Set items for the side menu with icons only
          
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            item.setData(Qt.ItemDataRole.UserRole, menu.get("icon"))
            self.side_menu_icon_only.addItem(item)
            self.side_menu_icon_only.setCurrentRow(0)
            

            # Set items for the side menu with icons and text
            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)
            
                # Conecta la señal itemClicked *fuera* del bucle
        self.side_menu_icon_only.itemClicked.connect(self.handle_item_click_icon_only)
        self.side_menu.itemClicked.connect(self.handle_item_click)


        # Define una nueva función para manejar los clicks, comprobando el icono
    def handle_item_click_icon_only(self, item):
            icon_path = item.data(Qt.ItemDataRole.UserRole)
            print( icon_path)
            
            nombre=item.icon().name()
         
            if icon_path == ":iconos/dasboard/icon/reports.svg":  # Comprueba si el icono coincide
                self.precio()
           
    def handle_item_click(self, item):
         
            if item.text() == "Precio":  # Comprueba si el icono coincide
                self.precio()
              

        
            
    def precio(self):
    
        precio=CrudPrecio()
        precio.exec()
         
                 
    def init_stackwidget(self):
        
             
        
          # Initialize the stack widget with content pages
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
               self.main_content.removeWidget(widget)

                  
        nuevo_juego = GestionPistas(self,self.UserLogueado,self.sesionActiva)        
        self.main_content.addWidget( nuevo_juego) 
        
        if self.UserLogueado.rol=="Administrador":        
      
            nuevo_juego1 = UserCRUD(self.UserLogueado)        
            self.main_content.addWidget(nuevo_juego1)
            
            sesion= SesionCRUD(self.sesionActiva)
            self.main_content.addWidget(sesion)
            
            juegoscrud= JuegosCrudADmin(self.sesionActiva)
            self.main_content.addWidget(juegoscrud)
        
    
       
        
        
              
    
        """
        new_pag1 = QWidget()         
        nuevo_juego = Nuevo_Juego()
        nuevo_juego.setupUi(new_pag1) 
        self.main_content.addWidget(new_pag1)

      
        for index, menu in enumerate(self.menu_list):
            if index == 0:
             continue  # Omitir el primer elemento
           
            text = menu.get("name")
            layout = QGridLayout()
            label = QLabel(text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPixelSize(20)
            label.setFont(font)
            layout.addWidget(label)
            new_page1 = QWidget()
            new_page1.setLayout(layout)
            self.main_content.addWidget(new_page1)
        """
        
        
            
            
    def button_icon_change(self, status):
        # Change the menu button icon based on its status
        if status:
            self.menu_btn.setIcon(QIcon(":iconos/dasboard/icon/open.svg"))
        else:
            self.menu_btn.setIcon(QIcon(":iconos/dasboard/icon/close.svg"))
         
         


#if __name__ == '__main__':
 #app = QApplication(sys.argv)

    # Load style file
 #user=Usuario()
  

 #window = MainWindow(user)
 #window.show()

 #sys.exit(app.exec())
