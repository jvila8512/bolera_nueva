import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt, QSize

class VentanaVideo(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle('Reproductor de Video')
        self.setGeometry(100, 100, 800, 600)  # Tamaño inicial
        # Configuración de la ventana
        # Quitar el botón de cerrar
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Fondo transparente si necesitas
        #self.showFullScreen()  # Ventana maximizada


        # Creamos un layout vertical
        self.layout = QVBoxLayout()
        self.layout .setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        self.layout .setSpacing(0)  # Sin espacio
        self.setLayout(self.layout)
        

        # Video Widget
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Crear el reproductor de media
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()  # Crear objeto de salida de audio
        self.player.setAudioOutput(self.audio_output)  # Asignar salida de audio
        self.player.setVideoOutput(self.video_widget)
       


        # Conectar señal para reiniciar video
        self.player.mediaStatusChanged.connect(self.reiniciar_video)

        # Establecer la ruta de tu video (cambia por el archivo de video que deseas usar)
        video_path = 'fotos/strike.mp4'  # Cambia esto a tu archivo de video
        self.player.setSource(QUrl.fromLocalFile(video_path))  # Cargar el video
        self.audio_output.setVolume(1.0)  # Establecer el volumen entre 0.0 y 1.0
        #self.player.play()  # Reproducir el video
       
    def showEvent(self, event):
         self.player.play()  # Reproducir cuando la ventana es visible
         super().showEvent(event)

    def hideEvent(self, event):
        self.player.pause()  # Pausar cuando la ventana se oculta
        super().hideEvent(event)
    def reiniciar_video(self, state):
        if state == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.setPosition(0)  # Regresar al inicio
            self.player.play()  # Reproducir nuevamente
            
          

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaVideo()
    ventana.show()
    sys.exit(app.exec())