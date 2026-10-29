import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication, QScreen

def obtener_info_pantallas():
    app = QApplication(sys.argv)  # Necesario para acceder a QGuiApplication
    screens = QGuiApplication.screens()

    pantallas_info = []

    for i, screen in enumerate(screens):
        nombre = screen.name()
        try:
            edid = screen.serialNumber()  # Intenta obtener el EDID
        except Exception as e:
            edid = "No disponible"
        
        pantallas_info.append({
            "indice": i,
            "nombre": nombre,
            "edid": edid,
            "geometria": screen.geometry(),
            "resolucion": screen.availableGeometry(),
            "pixel_ratio": screen.devicePixelRatio()
        })

    # Imprimir información de las pantallas
    for pantalla in pantallas_info:
        print(f"Pantalla {pantalla['indice']}:")
        print(f"  Nombre: {pantalla['nombre']}")
        print(f"  EDID: {pantalla['edid']}")
        print(f"  Geometría: {pantalla['geometria']}")
        print(f"  Resolución: {pantalla['resolucion']}")
        print(f"  Dispositivo pixel ratio: {pantalla['pixel_ratio']}")
        print()

    # Aquí puedes agregar lógica para asignar un orden específico basado en el EDID o nombre
    asignar_orden_pantallas(pantallas_info)

    app.quit()  # Cerrar la aplicación

def asignar_orden_pantallas(pantallas_info):
    # Ordenar las pantallas basado en el EDID o nombre
    pantallas_ordenadas = sorted(pantallas_info, key=lambda x: x['edid'] or x['nombre'])

    print("Pantallas ordenadas:")
    for pantalla in pantallas_ordenadas:
        print(f"Pantalla {pantalla['indice']} - EDID: {pantalla['edid']} - Nombre: {pantalla['nombre']}")

    # Aquí puedes aplicar la configuración de pantalla que desees
    # Por ejemplo, mover ventanas a pantallas específicas o cambiar la resolución

if __name__ == '__main__':
    obtener_info_pantallas()
    