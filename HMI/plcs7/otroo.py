
# Importar la clase PLC_S7_Communicator
from ConexionPLC import PLC_S7_Communicator  # Asegúrate de guardar la clase en un archivo llamado plc_communicator.py


# Crear una instancia de PLC_S7_Communicator
plc = PLC_S7_Communicator("192.168.1.188")  # Reemplaza con la IP de tu PLC

# Activar M0.0
#plc.write_marker(1, 0,0)  # Escribe 0x01 en M0.0


# Escribir el setpoint en VD100
setpoint = 50  # Ejemplo de setpoint
plc.write_variable_float(120, setpoint)


# Guardar el setpoint en la EEPROM
#plc.save_to_eeprom1(120)


# Activar Q0.2
#plc.write_output_bit(0, 6, 0)