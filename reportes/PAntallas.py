import sys
import pyudev
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget

class DeviceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestor de Dispositivos USB-HMI')

        # Crear un widget central y un layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Crear una lista para mostrar los dispositivos
        self.device_list = QListWidget()
        layout.addWidget(self.device_list)

        # Listar dispositivos USB
        self.list_usb_devices()

    def list_usb_devices(self):
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb'):
            if 'HMI' in device.get('ID_MODEL', ''):  # Cambia 'HMI' por el identificador de tus dispositivos
                self.device_list.addItem(f"{device.get('ID_MODEL')}: {device.device_node}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DeviceManager()
    window.show()
    sys.exit(app.exec())